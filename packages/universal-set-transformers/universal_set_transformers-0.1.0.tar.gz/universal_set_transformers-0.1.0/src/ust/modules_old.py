import abc
import itertools
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Any, Callable, Dict, Iterable, Literal, Optional, Tuple, Type, Union

# Scaled Dot Product Set Attention -----------------------------------------------------------------

class ScaledDotProductSetAttention(abc.ABC, nn.Module):
    def __init__(
        self,
        dropout_p: float = 0.0,
        scale: Optional[float] = None,
        enable_gqa: bool = False
    ):
        super().__init__()
        self.dropout_p = dropout_p
        self.scale = scale
        self.enable_gqa = enable_gqa

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor] = None
    ):
        if key is None:
            key = query
        if value is None:
            value = key

        if key_multiplicities is not None:
            key_multiplicities = key_multiplicities.float().unsqueeze(-2)

        return self.compute_attention(query, key, value, key_multiplicities)

    @abc.abstractmethod
    def compute_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        pass


class SoftmaxFlashSetAttention(ScaledDotProductSetAttention):
    def compute_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        # Use native scaled dot product attention with attention bias
        attn_bias = None
        if key_multiplicities is not None:
            attn_bias = torch.log(key_multiplicities)
        return F.scaled_dot_product_attention(
            query,
            key,
            value,
            attn_mask = attn_bias,
            dropout_p = self.dropout_p,
            is_causal = False,
            scale = self.scale,
            enable_gqa = self.enable_gqa
        )


class SoftmaxSetAttention(ScaledDotProductSetAttention):
    def compute_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])
        scores = query @ key.transpose(-2, -1) * scale
        if key_multiplicities is not None:
            scores = scores + torch.log(key_multiplicities)
        scores = F.softmax(scores, dim=-1)
        scores = torch.dropout(scores, self.dropout_p, self.training)
        return scores @ value


class SigmoidSetAttention(ScaledDotProductSetAttention):
    def compute_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])
        scores = F.sigmoid(query @ key.transpose(-2, -1) * scale)
        if key_multiplicities is not None:
            scores = scores * key_multiplicities
        scores = torch.dropout(scores, self.dropout_p, self.training)
        return scores @ value

# Scaled Dot Product Slot Set Attention ------------------------------------------------------------

class ScaledDotProductSlotSetAttention(ScaledDotProductSetAttention):
    """
    Base class for minibatch-consistent slot set attention.
    """
    def __init__(
        self,
        dropout_p: float = 0.0,
        scale: Optional[float] = None,
        enable_gqa: bool = False
    ):
        super().__init__(
            dropout_p=dropout_p,
            scale=scale,
            enable_gqa=enable_gqa
        )
        self.in_context = False
        self.state: Any = None

    def forward(
        self,
        query: torch.Tensor,
        key: Union[torch.Tensor, Iterable[torch.Tensor]],
        value: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None,
        key_multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None
    ):
        if value is None:
            value = key

        if isinstance(key_multiplicities, torch.Tensor):
            key_multiplicities = key_multiplicities.float().unsqueeze(-2)
        elif key_multiplicities is not None:
            key_multiplicities = (x.float().unsqueeze(-2) for x in key_multiplicities)

        return self.compute_attention(query, key, value, key_multiplicities)

    def compute_attention(
        self,
        query: torch.Tensor,
        key: Union[torch.Tensor, Iterable[torch.Tensor]],
        value: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None,
        key_multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None
    ) -> torch.Tensor:
        # Prepare input for iteration
        key_iter = (key,) if isinstance(key, torch.Tensor) else key
        if value is not None:
            value_iter = (value,) if isinstance(value, torch.Tensor) else value
        else:
            value_iter = None
        if isinstance(key_multiplicities, torch.Tensor):
            key_multiplicities_iter = (key_multiplicities,)
        else:
            key_multiplicities_iter = key_multiplicities or None

        # Compute the scale factor
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])

        # Setup the context
        if not self.in_context:
            self.state = self.initial_state()

        # Setup the iterator
        kvm_iter = zip(*[x for x in [key_iter, value_iter, key_multiplicities_iter] if x is not None], strict=True)

        # Compute attention over slots in a minibatch-consistent manner
        for k, *vm in kvm_iter:
            # Unpack value and multiplicities, reusing key if value is not provided
            vm = iter(vm)
            v = next(vm) if value_iter is not None else k
            m = next(vm) if key_multiplicities_iter is not None else None

            if self.enable_gqa:
                k = k.repeat_interleave(query.size(-3)//k.size(-3), -3)
                v = v.repeat_interleave(query.size(-3)//v.size(-3), -3)

            self.compute_aggregated_attention(
                query @ k.transpose(-2, -1) * scale,
                v,
                m
            )

        # If we're in a context, return and keep the state
        if self.in_context:
            return # type: ignore
        output = self.get()
        self.state = None
        return output

    @abc.abstractmethod
    def compute_aggregated_attention(self, attention, value, multiplicities):
        """
        Compute aggregated attention given the current minibatch
        """
        pass

    @abc.abstractmethod
    def get(self) -> torch.Tensor:
        """
        Get the computed attention
        """
        pass

    # @abc.abstractmethod
    def initial_state(self):
        pass

    def __enter__(self):
        self.state = self.initial_state()
        self.in_context = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.state = None
        self.in_context = False


class SoftmaxSlotSetAttention(ScaledDotProductSlotSetAttention):
    def initial_state(self):
        return {
            "aggregated_value": 0.0,
            "normalization_term": 0.0,
            "max_value": None
        }

    def compute_aggregated_attention(self, attention, value, multiplicities):
        """
        Numerically-stable, true softmax attention
        """
        if multiplicities is not None:
            attention = attention + torch.log(multiplicities.float()).unsqueeze(-2)
        max_value = attention.amax(dim=-1, keepdim=True)
        scores = torch.exp(attention - max_value)
        scores = torch.dropout(scores, self.dropout_p, self.training)
        sp = scores.sum(dim=-1, keepdim=True)
        op = torch.dropout(scores, self.dropout_p, self.training) @ value

        if self.state["max_value"] is not None:
            # Not the first batch, we need to rescale
            delta1 = torch.exp(self.state["max_value"] - max_value)
            delta2 = 1.0 / delta1
            bigger = max_value > self.state["max_value"]

            sp = torch.where(bigger, sp + self.state["normalization_term"] * delta1, self.state["normalization_term"] + sp * delta2)
            op = torch.where(bigger, op + self.state["aggregated_value"] * delta1, self.state["aggregated_value"] + op * delta2)
            max_value = torch.where(bigger, max_value, self.state["max_value"])

        self.state["aggregated_value"] = op
        self.state["normalization_term"] = sp
        self.state["max_value"] = max_value

    def get(self):
        return self.state["aggregated_value"] / self.state["normalization_term"]


class SigmoidSlotSetAttention(ScaledDotProductSlotSetAttention):
    def initial_state(self):
        return {"aggregated_value": 0.0}

    def compute_aggregated_attention(
        self,
        attention: torch.Tensor,
        value: torch.Tensor,
        multiplicities: torch.Tensor
    ):
        attention = torch.sigmoid(attention)
        if multiplicities is not None:
            attention = attention * multiplicities
        attention = torch.dropout(attention, self.dropout_p, self.training)
        self.state["aggregated_value"] = self.state["aggregated_value"] + attention @ value

    def get(self):
        return self.state["aggregated_value"]

# Multihead Set Attention --------------------------------------------------------------------------

class MultiheadSetAttention(nn.Module):
    """
    An implementation of Multi-head attention that replaces masking with the ability to supply
    multiplicities information.
    """
    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        attention_method: Union[ScaledDotProductSetAttention, None] = None,
        bias: bool = True,
        head_dim: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        factory_kwargs = {"device": device, "dtype": dtype}
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.bias = bias

        if head_dim is None:
            assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads if head_dim is not provided"
            head_dim = embed_dim // num_heads
        self.head_dim = head_dim

        # Scaled Dot Product Attention Method
        if attention_method is None:
            attention_method = SoftmaxFlashSetAttention()
        self.scaled_dot_product_attention = attention_method

        # Parameters
        self.wq = nn.Linear(self.embed_dim, self.num_heads*self.head_dim, bias=bias, **factory_kwargs)
        self.wk = nn.Linear(self.embed_dim, self.num_heads*self.head_dim, bias=bias, **factory_kwargs)
        self.wv = nn.Linear(self.embed_dim, self.num_heads*self.head_dim, bias=bias, **factory_kwargs)
        self.wo = nn.Linear(self.head_dim * num_heads, embed_dim, bias=bias, **factory_kwargs)

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:

        b, n_q, _ = query.shape
        _, n_k, _ = key.shape

        # Unsqueeze multiplicities for other attention heads
        if key_multiplicities is not None:
            key_multiplicities = key_multiplicities.unsqueeze(-2)

        # Compute linear projections
        q = self.wq(query).view((b, n_q, self.num_heads, self.head_dim)).transpose(-2, -3)
        k = self.wk(key).view((b, n_k, self.num_heads, self.head_dim)).transpose(-2, -3)
        v = self.wv(value).view((b, n_k, self.num_heads, self.head_dim)).transpose(-2, -3)

        # Compute attention
        attention = self.scaled_dot_product_attention(
            query=q,
            key=k,
            value=v,
            key_multiplicities=key_multiplicities,
        )

        # Output projection
        attention = attention.transpose(-2, -3).reshape((b, n_q, self.num_heads*self.head_dim)) # type: ignore
        output = self.wo(attention)

        return output


class MultiheadSlotSetAttention(MultiheadSetAttention):
    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        attention_method: Optional[ScaledDotProductSlotSetAttention] = None,
        bias: bool = True,
        head_dim: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        if attention_method is None:
            attention_method = SoftmaxSlotSetAttention()
        super().__init__(
            embed_dim=embed_dim,
            num_heads=num_heads,
            attention_method=attention_method,
            bias=bias,
            head_dim=head_dim,
            device=device,
            dtype=dtype
        )
        assert isinstance(self.scaled_dot_product_attention, ScaledDotProductSlotSetAttention)
        self.scaled_dot_product_attention: ScaledDotProductSlotSetAttention

    def forward(
        self,
        query: torch.Tensor,
        key: Union[torch.Tensor, Iterable[torch.Tensor]],
        value: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None,
        key_multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None
    ) -> torch.Tensor:

        # Prepare input for iteration
        key_iter = (key,) if isinstance(key, torch.Tensor) else key
        if value is not None:
            value_iter = (value,) if isinstance(value, torch.Tensor) else value
        else:
            value_iter = None
        if isinstance(key_multiplicities, torch.Tensor):
            key_multiplicities_iter = (key_multiplicities,)
        else:
            key_multiplicities_iter = key_multiplicities or None

        # Setup the strict iterator
        kvm_iter = zip(*[x for x in [key_iter, value_iter, key_multiplicities_iter] if x is not None], strict=True)

        # Compute the query projection
        b, n_q, _ = query.shape
        q = self.wq(query).view((b, n_q, self.num_heads, self.head_dim)).transpose(-2, -3)

        with self.scaled_dot_product_attention as scaled_dot_product_attention:
            for k, *vm in kvm_iter:
                # Unpack value and multiplicities, reusing key if value is not provided
                vm = iter(vm)
                v = next(vm) if value_iter is not None else k
                m = next(vm) if key_multiplicities_iter is not None else None

                # Compute the key and value projections
                _, n_k, _ = k.shape
                k = self.wk(k).view((b, n_k, self.num_heads, self.head_dim)).transpose(-2, -3)
                v = self.wv(v).view((b, n_k, self.num_heads, self.head_dim)).transpose(-2, -3)

                # Compute scaled dot product slot set attention
                scaled_dot_product_attention(
                    query=q,
                    key=k,
                    value=v,
                    key_multiplicities=m
                )
            attention = scaled_dot_product_attention.get()

        # Output projection
        attention = attention.transpose(-2, -3).reshape((b, n_q, self.num_heads*self.head_dim)) # type: ignore
        output = self.wo(attention)
        return output


class Slots(nn.Module):
    def __init__(
        self,
        embed_dim: int,
        num_slots: int,
        slot_type: Literal["random", "deterministic"] = "deterministic"
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_slots = num_slots
        self.slot_type = slot_type

        if slot_type == "random":
            self.mu = nn.Parameter(torch.randn(1, self.num_slots, self.embed_dim), requires_grad=True)
            self.sigma = nn.Parameter(torch.randn(1, self.num_slots, self.embed_dim), requires_grad=True)

        elif slot_type == "deterministic":
            self.slots = nn.Parameter(torch.randn(1, self.num_slots, self.embed_dim), requires_grad=True)

    def forward(self, shape: Union[int, Iterable[int]]):
        shape = (shape,) if isinstance(shape, int) else tuple(shape)
        if self.slot_type == "random":
            return torch.normal(self.mu.expand(*shape, -1, -1), self.sigma.expand(*shape, -1, -1))
        else:
            return self.slots.expand(*shape, -1, -1)

# Attention Blocks ---------------------------------------------------------------------------------

class MultiheadSetAttentionBlock(nn.Module):
    """
    The Multihead Set Attention Block (MSAB) based on the Set Transformer framework.
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        dim_feedforward: Optional[int] = None,
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        layer_norm: bool = True,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        attention_method: Optional[ScaledDotProductSetAttention] = None,
        d_head: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        factory_kwargs = {"device": device, "dtype": dtype}

        if isinstance(activation, str):
            self.activation = getattr(F, activation)
        else:
            self.activation = activation

        if dim_feedforward is None:
            dim_feedforward = 4*d_model

        self.attention = MultiheadSetAttention(
            embed_dim=d_model,
            num_heads=nhead,
            bias=bias,
            attention_method=attention_method,
            head_dim=d_head,
            **factory_kwargs
        )
        if layer_norm:
            self.norm_x = nn.LayerNorm(d_model, eps=layer_norm_eps, **factory_kwargs)
            self.norm_y = nn.LayerNorm(d_model, eps=layer_norm_eps, **factory_kwargs)
            self.norm_ffn = nn.LayerNorm(d_model, eps=layer_norm_eps, **factory_kwargs)
        else:
            self.norm_x = nn.Identity()
            self.norm_y = nn.Identity()
            self.norm_ffn = nn.Identity()
        self.linear1 = nn.Linear(d_model, dim_feedforward, bias=bias, **factory_kwargs)
        self.linear2 = nn.Linear(dim_feedforward, d_model, bias=bias, **factory_kwargs)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout_ffn = nn.Dropout(dropout)

    def forward(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor] = None,
    ):
        # MHA + residual
        x = x + self.dropout1(
            self.attention(
                self.norm_x(x),
                self.norm_y(y),
                key_multiplicities=key_multiplicities,
            )[0]
        )

        # FFN + residual
        x = x + self.dropout2(
            self.linear2(self.dropout_ffn(self.activation(self.linear1(self.norm_ffn(x)))))
        )

        return x


class MultiheadSlotSetAttentionBlock(MultiheadSetAttentionBlock):
    """
    The Multiset Slot Set Attention Block (MSSAB) based on the Set Transformer framework.
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        dim_feedforward: Optional[int] = None,
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        attention_method: Optional[ScaledDotProductSlotSetAttention] = None,
        d_head: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            attention_method=attention_method,
            d_head=d_head,
            device=device,
            dtype=dtype
        )
        factory_kwargs = {"device": device, "dtype": dtype}

        self.attention = MultiheadSlotSetAttention(
            embed_dim=d_model,
            num_heads=nhead,
            bias=bias,
            attention_method=attention_method,
            head_dim=d_head,
            **factory_kwargs
        )

    def forward(
        self,
        x: torch.Tensor,
        y: Union[torch.Tensor, Iterable[torch.Tensor]],
        key_multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None,
    ):
        if isinstance(y, torch.Tensor):
            y = self.norm_y(y)
        else:
            y = tuple(self.norm_y(yi) for yi in y)

        # MHA + residual
        x = x + self.dropout1(
            self.attention(
                self.norm_x(x),
                y,
                key_multiplicities=key_multiplicities,
            )[0]
        )

        # FFN + residual
        x = x + self.dropout2(
            self.linear2(self.dropout_ffn(self.activation(self.linear1(self.norm_ffn(x)))))
        )

        return x
