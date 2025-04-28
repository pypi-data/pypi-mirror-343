import torch
from typing import Callable, Dict, Iterable, overload, TypeVar, Union
from typing import TYPE_CHECKING

from .api.types import Minibatch, Minibatches, MinibatchTransform

T = TypeVar("T")

@overload
def pipe(
    tensor_or_minibatches: "torch.Tensor",
    immediate_call: Callable[["torch.Tensor"], T],
    minibatch_call: MinibatchTransform
) -> T:
    ...
@overload
def pipe(
    tensor_or_minibatches: Minibatches,
    immediate_call: Callable[["torch.Tensor"], T],
    minibatch_call: MinibatchTransform
) -> Minibatches:
    ...
@overload
def pipe(
    tensor_or_minibatches: Union["torch.Tensor", Minibatches],
    immediate_call: Callable[["torch.Tensor"], T],
    minibatch_call: MinibatchTransform
) -> Union[T, Minibatches]:
    ...
def pipe(
    tensor_or_minibatches: Union["torch.Tensor", Minibatches],
    immediate_call: Callable[["torch.Tensor"], T],
    minibatch_call: MinibatchTransform
) -> Union[T, Minibatches]:
    if isinstance(tensor_or_minibatches, torch.Tensor):
        return immediate_call(tensor_or_minibatches)
    return map(minibatch_call, tensor_or_minibatches)
