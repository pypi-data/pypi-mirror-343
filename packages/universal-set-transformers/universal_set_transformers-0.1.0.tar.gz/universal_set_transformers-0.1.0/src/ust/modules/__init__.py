import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Any, Callable, Iterable, Literal, Optional, overload, Tuple, Union

from ..api.modules import ScaledDotProductSetAttention
from ..api.types import Minibatch, Minibatches, NoState
from ..utils import pipe
from .scaled_dot_product_attention import ScaledDotProductSoftmaxFlashSetAttention


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
            attention_method = ScaledDotProductSoftmaxFlashSetAttention()
        self.scaled_dot_product_attention: ScaledDotProductSetAttention = attention_method # type: ignore

        # Parameters
        self.wq = nn.Linear(self.embed_dim, self.num_heads*self.head_dim, bias=bias, **factory_kwargs)
        self.wk = nn.Linear(self.embed_dim, self.num_heads*self.head_dim, bias=bias, **factory_kwargs)
        self.wv = nn.Linear(self.embed_dim, self.num_heads*self.head_dim, bias=bias, **factory_kwargs)
        self.wo = nn.Linear(self.head_dim * num_heads, embed_dim, bias=bias, **factory_kwargs)

    @overload
    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Optional[torch.Tensor],
        value: Optional[torch.Tensor],
        key_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Stateless forward pass for immediate computation on tensors.
        """
        ...

    @overload
    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Optional[torch.Tensor],
        value: Optional[torch.Tensor],
        key_multiplicities: Optional[torch.Tensor] = None,
        *,
        state: Any
    ) -> torch.Tensor:
        """
        Stateful forward pass for minibatch-consistent computation on tensors.
        """
        ...

    @overload
    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Minibatches,
    ) -> torch.Tensor:
        """
        Stateless forward pass for minibatch processing.
        """
        ...

    @overload
    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Minibatches,
        *,
        state: Any
    ) -> Tuple[torch.Tensor, Any]:
        """
        Stateful forward pass for minibatch processing, returning the state.
        """
        ...

    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Optional[Union[torch.Tensor, Minibatches]] = None,
        value: Optional[torch.Tensor] = None,
        key_multiplicities: Optional[torch.Tensor] = None,
        *,
        state: Optional[Any] = NoState
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, Any]]:
        if key_or_minibatches is None:
            key_or_minibatches = query

        # If we're in a stateful context, we need to treat all input as a minibatches
        if state is not NoState and isinstance(key_or_minibatches, torch.Tensor):
            key_or_minibatches = ({
                "key": key_or_minibatches,
                "value": value,
                "key_multiplicities": key_multiplicities,
            },)

        # If a tensor was supplied, we're in immediate mode
        if isinstance(key_or_minibatches, torch.Tensor):
            key = key_or_minibatches
            output = self.forward_immediate(query, key, value, key_multiplicities)
        # Otherwise, we're in minibatch mode
        else:
            minibatches = key_or_minibatches
            output, new_state = self.forward_minibatch(
                query,
                minibatches,
                state if state is not NoState else None
            )
        if state is not NoState:
            return output, new_state
        return output

    def forward_immediate(
        self,
        query: torch.Tensor,
        key: Optional[torch.Tensor],
        value: Optional[torch.Tensor],
        key_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Compute multi-head attention in a single forward pass.
        """
        if key is None:
            key = query
        if value is None:
            value = key

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
        output = self.scaled_dot_product_attention(
            query=q,
            key_or_minibatches=k,
            value=v,
            key_multiplicities=key_multiplicities,
        )

        # Output projection
        output = output.transpose(-2, -3).reshape((b, n_q, self.num_heads*self.head_dim)) # type: ignore
        output = self.wo(output)

        return output

    def _minibatch_project_kv(self, minibatch: Minibatch) -> Minibatch:
        """
        Preprocess a minibatch for attention computation.
        """
        key = minibatch["key"]
        value = minibatch["value"]
        if value is None:
            value = key
        return {
            "key": self.wk(key).unflatten(-1, (self.num_heads, self.head_dim)).transpose(-2, -3),
            "value": self.wv(value).unflatten(-1, (self.num_heads, self.head_dim)).transpose(-2, -3),
            "key_multiplicities": minibatch.get("key_multiplicities", None)
        }

    def forward_minibatch(
        self,
        query: torch.Tensor,
        minibatches: Minibatches,
        state: Optional[Any]
    ) -> Tuple[torch.Tensor, Any]:
        """
        Compute multi-head attention over multiple minibatches.
        """
        b, n_q, _ = query.shape

        q = self.wq(query).view((b, n_q, self.num_heads, self.head_dim)).transpose(-2, -3)

        # Linear project k and v
        minibatches = map(self._minibatch_project_kv, minibatches)

        # Compute attention over minibatches under the context
        output, state = self.scaled_dot_product_attention(
            query=q,
            key_or_minibatches=minibatches,
            state=state
        )

        # Output projection
        output = output.transpose(-2, -3).reshape((b, n_q, self.num_heads*self.head_dim)) # type: ignore
        output = self.wo(output)

        return output, state


class SelfSetAttentionBlock(nn.Module):
    """
    The Self Set Attention Block (SSAB) based on the SAB from the Set Transformer framework.
    Computes self attention over the full set. This block is not compatible with minibatch
    processing.
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        dim_feedforward: Optional[int] = None,
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        attention_method: Optional[ScaledDotProductSetAttention] = None,
        layer_norm: bool = True,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        d_head: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        factory_kwargs = {"device": device, "dtype": dtype}

        # Feedforward projection dimension
        if dim_feedforward is None:
            dim_feedforward = 4*d_model

        # Activation function
        if isinstance(activation, str):
            self.activation = getattr(F, activation)
        else:
            self.activation = activation

        # Scaled Dot Product Attention Method
        if attention_method is None:
            attention_method = ScaledDotProductSoftmaxFlashSetAttention()

        # Attention module
        self.attention = MultiheadSetAttention(
            embed_dim=d_model,
            num_heads=nhead,
            attention_method=attention_method,
            bias=bias,
            head_dim=d_head,
            **factory_kwargs
        )

        # Layer normalization
        if layer_norm:
            self.norm_x = nn.LayerNorm(d_model, eps=layer_norm_eps, **factory_kwargs)
            self.norm_ffn = nn.LayerNorm(d_model, eps=layer_norm_eps, **factory_kwargs)
        else:
            self.norm_x = nn.Identity()
            self.norm_ffn = nn.Identity()
        self.linear1 = nn.Linear(d_model, dim_feedforward, bias=bias, **factory_kwargs)
        self.linear2 = nn.Linear(dim_feedforward, d_model, bias=bias, **factory_kwargs)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout_ffn = nn.Dropout(dropout)

    def forward(
        self,
        x: torch.Tensor,
        multiplicities: Optional[torch.Tensor] = None,
    ):
        # MHA + residual
        x = x + self.dropout1(
            self.attention(
                self.norm_x(x),
                key_multiplicities=multiplicities,
            )
        )
        # FFN + residual
        x = x + self.dropout2(
            self.linear2(self.dropout_ffn(self.activation(self.linear1(self.norm_ffn(x)))))
        )
        return x


class CrossSetAttentionBlock(SelfSetAttentionBlock):
    """
    The Cross Set Attention Block (CSAB) based on the MAB from the Set Transformer framework.
    Computes attention over a cross set. This block is compatible with minibatch processing.
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        dim_feedforward: Optional[int] = None,
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        attention_method: Optional[ScaledDotProductSetAttention] = None,
        layer_norm: bool = True,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
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
            attention_method=attention_method,
            layer_norm=layer_norm,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            d_head=d_head,
            device=device,
            dtype=dtype
        )
        if layer_norm:
            self.norm_y = nn.LayerNorm(d_model, eps=layer_norm_eps, device=device, dtype=dtype)
        else:
            self.norm_y = nn.Identity()

    @overload
    def forward(
        self,
        x: torch.Tensor,
        y_or_minibatches: torch.Tensor,
        y_multiplicities: Optional[torch.Tensor] = None
    ):
        ...

    @overload
    def forward(
        self,
        x: torch.Tensor,
        y_or_minibatches: torch.Tensor,
        y_multiplicities: Optional[torch.Tensor] = None,
        *,
        state: Any
    ):
        ...

    @overload
    def forward(
        self,
        x: torch.Tensor,
        y_or_minibatches: Minibatches
    ):
        ...

    @overload
    def forward(
        self,
        x: torch.Tensor,
        y_or_minibatches: Minibatches,
        *,
        state: Any
    ):
        ...

    def forward(
        self,
        x: torch.Tensor,
        y_or_minibatches: Union[torch.Tensor, Minibatches],
        y_multiplicities: Optional[torch.Tensor] = None,
        *,
        state: Optional[Any] = NoState
    ):
        attention = self.attention(
            self.norm_x(x),
            pipe(y_or_minibatches, self.norm_y, self._minibatch_transform_norm_y),
            key_multiplicities=y_multiplicities,
            state=state
        )

        if state is not NoState:
            assert isinstance(attention, tuple)
            attention, new_state = attention

        # MHA + residual
        x = x + self.dropout1(attention)
        attention = None # free
        # FFN + residual
        x = x + self.dropout2(
            self.linear2(self.dropout_ffn(self.activation(self.linear1(self.norm_ffn(x)))))
        )
        if state is not NoState:
            return x, new_state
        return x

    def _minibatch_transform_norm_y(self, minibatch: Minibatch) -> Minibatch:
        y_norm = self.norm_y(minibatch["y"])
        y_multiplicities = minibatch.get("y_multiplicities", None)
        return {
            "key": y_norm,
            "value": y_norm,
            "key_multiplicities": y_multiplicities
        }

# Others -------------------------------------------------------------------------------------------

class Slots(nn.Module):
    def __init__(
        self,
        embed_dim: int,
        num_slots: int,
        slot_type: Literal["random", "deterministic"] = "deterministic",
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_slots = num_slots
        self.slot_type = slot_type

        if slot_type == "random":
            self.mu = nn.Parameter(torch.randn(1, self.num_slots, self.embed_dim, device=device, dtype=dtype), requires_grad=True)
            self.sigma = nn.Parameter(torch.randn(1, self.num_slots, self.embed_dim, device=device, dtype=dtype), requires_grad=True)

        elif slot_type == "deterministic":
            self.slots = nn.Parameter(torch.randn(1, self.num_slots, self.embed_dim, device=device, dtype=dtype), requires_grad=True)

    def forward(self, shape: Union[int, Iterable[int]]):
        shape = (shape,) if isinstance(shape, int) else tuple(shape)
        if self.slot_type == "random":
            return torch.normal(self.mu.expand(*shape, -1, -1), self.sigma.expand(*shape, -1, -1))
        else:
            return self.slots.expand(*shape, -1, -1)
