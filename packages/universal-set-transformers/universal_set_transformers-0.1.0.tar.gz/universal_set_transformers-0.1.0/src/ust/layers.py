import abc
import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint
from typing import Callable, Iterable, Literal, Optional, Union

from .modules import MultiheadSetAttentionBlock, Slots

class SetTransformerEncoderLayer(nn.Module, abc.ABC):
    """
    A generic transformer encoder layer interface.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_last = False

    @abc.abstractmethod
    def forward(
        self,
        src: Union[torch.Tensor, Iterable[torch.Tensor]],
        multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None,
    ):
        raise NotImplementedError()


class SetTransformerEncoder(nn.Module):
    """
    An implementation of a set transformer encoder
    """
    def __init__(
        self,
        encoder_layer: SetTransformerEncoderLayer,
        num_layers: int,
        norm: Optional[nn.Module] = None,
        activation_checkpointing: bool = False,
        use_reentrant_checkpointing: bool = False
    ):
        super().__init__()
        self.layers: nn.ModuleList = nn.ModuleList([copy.deepcopy(encoder_layer) for i in range(num_layers)])
        self.num_layers = num_layers
        self.norm = norm
        self.activation_checkpointing = activation_checkpointing
        self.use_reentrant_checkpointing = use_reentrant_checkpointing

        for layer in self.layers[:-1]:
            layer.is_last = False # type: ignore
        self.layers[-1].is_last = True # type: ignore

    def forward(
        self,
        src: Union[torch.Tensor, Iterable[torch.Tensor]],
        multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None
    ):
        output = src
        mod: SetTransformerEncoderLayer
        for mod in self.layers: # type: ignore
            if self.activation_checkpointing and not mod.is_last: # type: ignore
                output = torch.utils.checkpoint.checkpoint(
                    mod,
                    output,
                    multiplicities,
                    use_reentrant=self.use_reentrant_checkpointing
                )
            else:
                output = mod(output, multiplicities)
        if self.norm is not None:
            output = self.norm(output)
        return output

# Transformer Encoder Layers -----------------------------------------------------------------------

class SetAttentionBlock(SetTransformerEncoderLayer, MultiheadSetAttentionBlock):
    """
    The Set Attention Block (SAB) based on the Set Transformer framework. Computes attention
    over the full set with minibatch consistency.
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
        attention_activation: Literal["softmax", "sigmoid"] = "softmax",
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
            attention_activation=attention_activation,
            d_head=d_head,
            device=device,
            dtype=dtype
        )

    def forward(
        self,
        src: Union[torch.Tensor, Iterable[torch.Tensor]],
        multiplicities: Optional[Union[torch.Tensor, Iterable[torch.Tensor]]] = None,
        minibatch_size: Optional[int] = None
    ):
        if minibatch_size is not None:
            raise ValueError()
        return MultiheadSetAttentionBlock.forward(
            self,
            src,
            src,
            key_multiplicities=multiplicities
        )


class InducedSetAttentionBlock(SetTransformerEncoderLayer):
    """
    The Induced Set Attention Block (ISAB) based on the Set Transformer framework. Approximates
    full set attention by using a set of inducing points/slots.
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        num_slots: int,
        dim_feedforward: Optional[int] = None,
        slot_type: Literal["random", "deterministic"] = "deterministic",
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        attention_activation: Literal["softmax", "sigmoid"] = "softmax",
        slot_attention_activation: Optional[Literal["softmax", "sigmoid"]] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        self.num_slots = num_slots
        self.slot_type = slot_type
        slot_attention_activation = slot_attention_activation or attention_activation

        self.slots = Slots(d_model, num_slots, slot_type=self.slot_type)

        self.mab1 = MultiheadSetAttentionBlock(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            attention_activation=slot_attention_activation,
            device=device,
            dtype=dtype
        )
        self.mab2 = MultiheadSetAttentionBlock(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            attention_activation=attention_activation,
            device=device,
            dtype=dtype
        )

    def forward(
        self,
        src: torch.Tensor,
        multiplicities: Optional[torch.Tensor] = None,
        minibatch_size: Optional[int] = None
    ) -> torch.Tensor:
        batch_size = src.shape[0]

        # Get slots
        slots = self.slots(batch_size)

        # Compute slot attention
        slot_attention = self.mab1(
            slots,
            src,
            key_multiplicities=multiplicities,
            key_minibatch_size=minibatch_size
        )

        # Compute attention on slots
        return self.mab2(src, slot_attention, query_minibatch_size=minibatch_size)


class SlotSetEncoderBlock(SetTransformerEncoderLayer):
    """
    The Slot Set Encoder (SSE) block based on the MBC/UMBC frameworks. Computes attention
    over a set of slots in a minibatch consistent manner.
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        num_slots: int,
        dim_feedforward: Optional[int] = None,
        slot_type: Literal["random", "deterministic"] = "deterministic",
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        attention_activation: Literal["softmax", "sigmoid"] = "softmax",
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        self.num_slots = num_slots
        self.slot_type = slot_type

        self.slots = Slots(d_model, num_slots, slot_type=self.slot_type)
        self.mhsa = MultiheadSetAttentionBlock(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            attention_activation=attention_activation,
            device=device,
            dtype=dtype
        )

    def forward(
        self,
        src: torch.Tensor,
        multiplicities: Optional[torch.Tensor] = None,
        minibatch_size: Optional[int] = None
    ) -> torch.Tensor:
        batch_size = src.shape[0]

        # Get slots
        slots = self.slots(batch_size)

        # Compute slot attention
        return self.mhsa(
            slots,
            src,
            key_multiplicities=multiplicities,
            key_minibatch_size=minibatch_size
        )


class PoolingByMultiheadSetAttention(nn.Module):
    """
    Pooling by Multihead Attention (PMA)
    """
    def __init__(
        self,
        d_model: int,
        nhead: int,
        num_slots: int,
        slot_type: Literal["random", "deterministic"] = "deterministic",
        dim_feedforward: Optional[int] = None,
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        attention_activation: Literal["softmax", "sigmoid"] = "softmax",
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        if isinstance(activation, str):
            self.activation = getattr(F, activation)
        else:
            self.activation = activation
        self.slots = Slots(d_model, num_slots, slot_type=slot_type)
        self.mab = MultiheadSetAttentionBlock(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            attention_activation=attention_activation,
            device=device,
            dtype=dtype
        )

        dim_feedforward = dim_feedforward or 4*d_model

        self.linear1 = nn.Linear(d_model, dim_feedforward, bias=bias, device=device, dtype=dtype)
        self.linear2 = nn.Linear(dim_feedforward, d_model, bias=bias, device=device, dtype=dtype)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        src: torch.Tensor,
        multiplicities: Optional[torch.Tensor] = None,
        minibatch_size: Optional[int] = None
    ) -> torch.Tensor:
        batch_size = src.shape[0]

        # Get slots
        slots = self.slots(batch_size)

        # Compute slot attention
        ffn_out = self.linear2(self.dropout(self.activation(self.linear1(src))))
        return self.mab(
            slots,
            ffn_out,
            key_multiplicities=multiplicities,
            key_minibatch_size=minibatch_size,
        )
