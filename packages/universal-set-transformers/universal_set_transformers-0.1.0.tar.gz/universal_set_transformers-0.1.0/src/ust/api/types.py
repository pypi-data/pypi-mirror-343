from typing import Callable, Dict, Generic, Iterable, Optional, Tuple, TypeVar, Union
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import torch

# A minibatch is represented as a dictionary mapping from tensor names to tensor values
Minibatch = Dict[str, Optional["torch.Tensor"]]

# An iterable of minibatches, used for minibatch-consistent processing
Minibatches = Iterable[Minibatch]

# A function that transforms one minibatch into another
MinibatchTransform = Callable[[Minibatch], Minibatch]

# Sentinel object used to indicate that no state is provided in stateful operations
NoState = object()
