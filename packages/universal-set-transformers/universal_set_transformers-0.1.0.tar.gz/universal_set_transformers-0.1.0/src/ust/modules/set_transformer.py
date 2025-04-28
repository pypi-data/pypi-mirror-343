import abc
import copy
import itertools
import lightning as L
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint
from typing import Any, Callable, Generic, List, Literal, Iterable, Optional, Tuple, TypeVar, Union

from ..api.modules import SetPoolingLayer, SetTransformerEncoderLayer
from ..api.types import Minibatch, Minibatches
from . import CrossSetAttentionBlock, SelfSetAttentionBlock, Slots
from .scaled_dot_product_attention import ScaledDotProductSetAttention

class SetTransformerEncoder(nn.Module):
    """
    The Set Transformer encoder.
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
        self.layers = nn.ModuleList([copy.deepcopy(encoder_layer) for _ in range(num_layers)])
        self.norm = norm
        self.activation_checkpointing = activation_checkpointing
        self.use_reentrant_checkpointing = use_reentrant_checkpointing

    def forward(
        self,
        src: Union[torch.Tensor, Iterable[torch.Tensor]],
        multiplicities: Optional[torch.Tensor] = None,
    ):
        output = src
        for layer in self.layers:
            if self.activation_checkpointing:
                output = torch.utils.checkpoint.checkpoint(
                    layer,
                    output,
                    multiplicities,
                    use_reentrant=self.use_reentrant_checkpointing
                )
            else:
                output = layer(output, multiplicities)
        if self.norm is not None:
            output = self.norm(output)
        return output

PreprocessorType = TypeVar("PreprocessorType", bound=nn.Module)
PrepoolerType = TypeVar("PrepoolerType", bound=nn.Module)
EncoderType = TypeVar("EncoderType", bound=SetTransformerEncoder)
PoolerType = TypeVar("PoolerType", bound=nn.Module)
DecoderType = TypeVar("DecoderType", bound=nn.Module)

class SetTransformer(abc.ABC, L.LightningModule, Generic[PreprocessorType, PrepoolerType, EncoderType, PoolerType, DecoderType]):
    """
    A Set Transformer model comprised of an encoder and an optional decoder. This
    model guarantees correct unbiased gradient estimation computation.
    """
    def __init__(
        self,
        preprocessor: Optional[PreprocessorType] = None,
        prepooler: Optional[PrepoolerType] = None,
        encoder: Optional[EncoderType] = None,
        pooler: Optional[PoolerType] = None,
        decoder: Optional[DecoderType] = None
    ):
        super().__init__()
        self.preprocessor = preprocessor
        self.prepooler = prepooler
        self.encoder = encoder
        self.pooler = pooler
        self.decoder = decoder

    def forward(self, x):
        """
        Generic forward pass
        """
        if self.preprocessor is not None:
            x = self.preprocessor(x)
        if self.prepooler is not None:
            x = self.prepooler(x)
        if self.encoder is not None:
            x = self.encoder(x)
        if self.pooler is not None:
            x = self.pooler(x)
        if self.decoder is not None:
            x = self.decoder(x)
        return x

    @abc.abstractmethod
    def generic_step(self, mode: str, batch):
        ...

    def training_step(self, batch):
        return self.generic_step("train", batch)

    def validation_step(self, batch):
        return self.generic_step("val", batch)

    def test_step(self, batch):
        return self.generic_step("test", batch)

# Set Transformer Encoder Layers -------------------------------------------------------------------

class SetAttentionBlock(SetTransformerEncoderLayer, SelfSetAttentionBlock):
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

    def forward_immediate(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ):
        return SelfSetAttentionBlock.forward(self, src, src_multiplicities)


class InducedSetAttentionBlock(SetTransformerEncoderLayer):
    def __init__(
        self,
        d_model: int,
        nhead: int,
        num_slots: int,
        slot_type: Literal["random", "deterministic"] = "deterministic",
        dim_feedforward: Optional[int] = None,
        dropout: float = 0.1,
        activation: Union[str, Callable[[torch.Tensor], torch.Tensor]] = F.relu,
        attention_method: Optional[ScaledDotProductSetAttention] = None,
        slot_attention_method: Optional[ScaledDotProductSetAttention] = None,
        layer_norm: bool = True,
        layer_norm_eps: float = 1e-5,
        bias: bool = True,
        d_head: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None
    ):
        super().__init__()
        self.mab1 = CrossSetAttentionBlock(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation=activation,
            attention_method=slot_attention_method,
            layer_norm=layer_norm,
            layer_norm_eps=layer_norm_eps,
            bias=bias,
            d_head=d_head,
            device=device,
            dtype=dtype
        )
        self.mab2 = CrossSetAttentionBlock(
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
        self.slots = Slots(d_model, num_slots, slot_type=slot_type)

    def forward_immediate(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ):
        batch_size = src.shape[0]
        return self.mab2(
            src,
            self.mab1(
                self.slots(batch_size),
                src,
                src_multiplicities
            )
        )

    def forward_minibatch(
        self,
        src: Minibatches
    ) -> Minibatches:
        # We need to persist the multiplicities
        persisted_src = []

        # Peek at first minibatch to get batch size
        src = iter(src)
        first_minibatch = next(src)
        batch_size = first_minibatch["src"].shape[0] # type: ignore

        # Reinsert the first minibatch
        src = itertools.chain((first_minibatch,), src)
        first_minibatch = None # free

        # Compute induced attention while presisting src
        induced_attention = self.mab1(
            self.slots(batch_size),
            (self._minibatch_map_and_persist(mb, persisted_src) for mb in src),
        )

        return ({
            "src": self.mab2(
                mb["y"],
                induced_attention,
            ),
            "src_multiplicities": mb["y_multiplicities"]
        } for mb in persisted_src)

    def _minibatch_map_and_persist(self, src: Minibatch, persisted_src: List[Minibatch]):
        y = src.pop("src")
        y_multiplicities = src.pop("src_multiplicities", None)
        src = {
            "y": y,
            "y_multiplicities": y_multiplicities
        }
        persisted_src.append(src)
        return src

class PoolingByMultiheadSetAttention(SetPoolingLayer):

    def __init__(
        self,
        d_model: int,
        nhead: int,
        num_slots: int,
        slot_type: Literal["random", "deterministic"] = "deterministic",
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
        self.mab = CrossSetAttentionBlock(
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
        self.slots = Slots(d_model, num_slots, slot_type=slot_type)

        if isinstance(activation, str):
            self.activation = getattr(F, activation)
        else:
            self.activation = activation

        dim_feedforward = dim_feedforward or 4*d_model
        self.linear1 = nn.Linear(d_model, dim_feedforward, bias=bias, device=device, dtype=dtype)
        self.linear2 = nn.Linear(dim_feedforward, d_model, bias=bias, device=device, dtype=dtype)
        self.dropout = nn.Dropout(dropout)

    def _feedforward(self, src: torch.Tensor) -> torch.Tensor:
        return self.linear2(self.dropout(self.activation(self.linear1(src))))

    def forward_immediate(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ):
        batch_size = src.shape[0]
        return self.mab(
            self.slots(batch_size),
            self._feedforward(src),
            src_multiplicities
        )

    def forward_minibatch(
        self,
        src: Minibatches,
        state: Optional[Any]
    ) -> Tuple[torch.Tensor, Any]:
        # Peek at first minibatch to get batch size
        src = iter(src)
        first_minibatch = next(src)
        batch_size = first_minibatch["src"].shape[0] # type: ignore

        # Reinsert the first minibatch
        src = itertools.chain((first_minibatch,), src)
        first_minibatch = None # free

        # Compute attention
        return self.mab(
            self.slots(batch_size),
            ({
                "y": self._feedforward(mb["src"]), # type: ignore
                "y_multiplicities": mb.get("src_multiplicities", None)
            } for mb in src),
            state=state
        )
