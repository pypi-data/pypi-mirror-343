import abc
import torch
import torch.nn as nn
from typing import Any, Dict, Iterable, Optional, overload, Tuple, Union
import warnings

from ust.api.types import Minibatches, NoState

class ScaledDotProductSetAttention(abc.ABC, nn.Module):
    """
    Abstract base class for scaled dot product attention mechanisms that operate on sets.

    This class provides a framework for implementing various attention mechanisms that can
    handle sets with potential duplicates represented as multiplicities. It supports both
    immediate computation on tensors and minibatch processing for memory efficiency.

    The class implements the context manager protocol to allow for stateful processing
    of minibatches, maintaining an internal state across multiple forward passes.

    Subclasses must implement the `compute_immediate_attention` method to define the
    specific attention mechanism (e.g., softmax, sigmoid).

    Concrete implementations of this class are available in ust.modules.scaled_dot_product_attention:

    - ScaledDotProductSoftmaxSetAttention: Uses softmax activation for attention weights
    - ScaledDotProductSoftmaxFlashSetAttention: Uses PyTorch's optimized flash attention
    - ScaledDotProductSigmoidSetAttention: Uses sigmoid activation for attention weights

    These implementations have been tested for:
    1. Equivalence with PyTorch's F.scaled_dot_product_attention
    2. Consistency between multiset representations (with duplicates vs. with multiplicities)
    3. Minibatch consistency
    4. Numerical stability with large values (1000-10000)
    """
    def __init__(
        self,
        dropout_p: float = 0.0,
        scale: Optional[float] = None,
        enable_gqa: bool = False
    ):
        """
        Initialize the scaled dot product set attention module.

        Args:
            dropout_p: Dropout probability applied to the attention weights. Default: 0.0
            scale: Custom scale factor for the attention scores. If None, uses 1/sqrt(d_k)
                   where d_k is the dimension of the query vectors. Default: None
            enable_gqa: Whether to enable grouped query attention, where multiple queries
                       can share the same key-value pairs. Default: False
        """
        super().__init__()
        self.dropout_p = dropout_p
        self.scale = scale
        self.enable_gqa = enable_gqa

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
    ) -> Tuple[torch.Tensor, Any]:
        """
        Statelful forward pass for minibatch-consistent computation on tensors.
        """
        ...

    @overload
    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Iterable[Dict[str, torch.Tensor]]
    ) -> torch.Tensor:
        """
        Stateless forward pass for minibatch processing.
        """
        ...

    @overload
    def forward(
        self,
        query: torch.Tensor,
        key_or_minibatches: Iterable[Dict[str, torch.Tensor]],
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
        key_or_minibatches: Union[Optional[torch.Tensor], Iterable[Dict[str, torch.Tensor]]] = None,
        value: Optional[torch.Tensor] = None,
        key_multiplicities: Optional[torch.Tensor] = None,
        *,
        state: Optional[Any] = NoState
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, Any]]:
        """
        Compute attention between query and key-value pairs, with optional multiplicities.

        This method handles two modes of operation:
        1. Immediate computation: When key is a tensor or None, computes attention directly
        2. Minibatch processing: When key is an iterable of tensors, processes in minibatches

        The method automatically selects the appropriate computation mode based on the input types
        and the context state.

        Args:
            query: Query tensor of shape (..., L_q, d_k) where L_q is the query sequence length
                  and d_k is the query dimension
            key: Key tensor of shape (..., L_k, d_k) where L_k is the key sequence length,
                 or an iterable of such tensors for minibatch processing
            value: Value tensor of shape (..., L_k, d_v) where d_v is the value dimension,
                   or an iterable of such tensors for minibatch processing. If None, uses key as value.
            key_multiplicities: Optional tensor of shape (..., L_k, 1) or iterable of such tensors
                               representing the multiplicity (abundance) of each key-value pair

        Returns:
            Attention output tensor of shape (..., L_q, d_v)

        Raises:
            AssertionError: If the input types are incompatible
        """
        # If no key is provided, use query as the key
        if key_or_minibatches is None:
            key_or_minibatches = query

        # If we're in a stateful context, we need to treat all input as a minibatches
        if state is not NoState and isinstance(key_or_minibatches, torch.Tensor):
            key_or_minibatches = ({
                "key": key_or_minibatches,
                "value": value,
                "key_multiplicities": key_multiplicities,
            },)

        # Immediate path
        if isinstance(key_or_minibatches, torch.Tensor):
            key = key_or_minibatches
            output = self.forward_immediate(query, key, value, key_multiplicities)

        # Minibatch path
        else:
            minibatches = key_or_minibatches
            new_state = self.forward_minibatch(query, minibatches, state)
            output = self.get(new_state)

        if state is not NoState:
            return output, new_state
        return output

    def forward_immediate(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: Optional[torch.Tensor],
        key_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Compute attention immediately on the provided tensors.

        This method handles the case when all inputs are tensors and can be processed
        in a single forward pass.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor of shape (..., L_k, d_k). If None, uses query as key.
            value: Value tensor of shape (..., L_k, d_v). If None, uses key as value.
            key_multiplicities: Optional tensor of shape (..., L_k) representing the
                               multiplicity of each key-value pair

        Returns:
            Attention output tensor of shape (..., L_q, d_v)
        """
        if value is None:
            value = key
        if key_multiplicities is not None:
            key_multiplicities = key_multiplicities.float().unsqueeze(-2)
        return self.compute_immediate_attention(query, key, value, key_multiplicities)

    def forward_minibatch(
        self,
        query: torch.Tensor,
        minibatches: Iterable[Dict[str, torch.Tensor]],
        state: Optional[Any]
    ) -> Any:
        """
        Compute attention over minibatches of key-value pairs.

        This method processes key-value pairs in minibatches, which is useful for memory-efficient
        processing of large sets. It maintains an internal state that accumulates the attention
        results across minibatches.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Iterable of key tensors, each of shape (..., L_k_i, d_k)
            value: Optional iterable of value tensors, each of shape (..., L_k_i, d_v).
                   If None, uses key as value.
            key_multiplicities: Optional iterable of multiplicity tensors, each of shape (..., L_k_i)

        Returns:
            The new state
        """
        # Construct or copy the state
        if state is None or state is NoState:
            state = self.initial_state()
        else:
            state = state.copy()

        # Compute attention over minibatches under the context
        for minibatch in minibatches:
            k = minibatch["key"]
            v = minibatch["value"]
            m = minibatch["key_multiplicities"]

            if v is None:
                v = k

            # Grouped query attention
            if self.enable_gqa:
                k = k.repeat_interleave(query.size(-3)//k.size(-3), -3)
                v = v.repeat_interleave(query.size(-3)//v.size(-3), -3)

            # Compute attention
            self.compute_aggregated_attention(
                query,
                k,
                v,
                m,
                state
            )

        return state

    @abc.abstractmethod
    def compute_immediate_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ) -> torch.Tensor:
        """
        Compute the attention mechanism on the full tensors.

        This abstract method must be implemented by subclasses to define the specific
        attention mechanism (e.g., softmax, sigmoid).

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor of shape (..., L_k, d_k)
            value: Value tensor of shape (..., L_k, d_v)
            key_multiplicities: Optional tensor of shape (..., L_k, 1) representing
                               the multiplicity of each key-value pair

        Returns:
            Attention output tensor of shape (..., L_q, d_v)
        """
        pass

    def compute_aggregated_attention(
        self,
        query: torch.Tensor,
        key: Optional[Iterable[torch.Tensor]],
        value: Optional[Iterable[torch.Tensor]],
        key_multiplicities: Optional[Iterable[torch.Tensor]],
        state: Any
    ):
        """
        Compute aggregated attention given the current minibatch.

        This method is called for each minibatch during minibatch processing. It updates
        the internal state with the attention results for the current minibatch.

        The default implementation simply adds the result of compute_immediate_attention
        to the aggregated value in the state. Subclasses may override this method to
        implement more sophisticated aggregation strategies.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor for the current minibatch
            value: Value tensor for the current minibatch
            key_multiplicities: Optional multiplicity tensor for the current minibatch
        """
        state["aggregated_value"] = state["aggregated_value"] \
            + self.compute_immediate_attention(query, key, value, key_multiplicities) # type: ignore

    def get(self, state: Any) -> torch.Tensor:
        """
        Get the computed aggregated attention result.

        This method is called after all minibatches have been processed to retrieve
        the final attention result.

        Returns:
            The aggregated attention output tensor
        """
        return state["aggregated_value"]

    def initial_state(self):
        """
        Initialize the state for minibatch processing.

        This method is called at the beginning of minibatch processing to initialize
        the internal state. Subclasses may override this method to initialize
        additional state variables.

        Returns:
            A dictionary containing the initial state
        """
        return {"aggregated_value": 0.0}


class SetTransformerEncoderLayer(abc.ABC, nn.Module):
    """
    The Set Transformer encoder layer interface.
    """

    @abc.abstractmethod
    def forward_immediate(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        pass

    def forward_minibatch(
        self,
        src: Minibatches
    ) -> Union[torch.Tensor, Minibatches]:
        """
        Default implementation
        """
        warnings.warn(f"Layer '{self.__class__.__name__}' is not minibatch consistent.")
        return (
            {
                "src": self.forward_immediate(
                    minibatch["src"], # type: ignore
                    minibatch.get("src_multiplicities", None)
                )
            }
            for minibatch in src
        )

    @overload
    def forward(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        ...

    @overload
    def forward(
        self,
        src: Minibatches,
    ) -> Minibatches:
        ...

    def forward(
        self,
        src: Union[torch.Tensor, Minibatches],
        src_multiplicities: Optional[torch.Tensor] = None,
    ) -> Union[torch.Tensor, Minibatches]:
        if isinstance(src, torch.Tensor):
            return self.forward_immediate(src, src_multiplicities)
        else:
            return self.forward_minibatch(src)


class SetPoolingLayer(abc.ABC, nn.Module):
    """
    Abstract base class for set pooling operations.

    Set pooling layers aggregate information from a set of elements into a fixed-size
    representation, regardless of the number of elements in the set. These layers are
    essential components in set-based neural networks, as they enable processing sets
    of varying sizes.

    This class provides a framework for implementing various pooling mechanisms that can
    handle sets with potential duplicates represented as multiplicities. It supports both
    immediate computation on tensors and minibatch processing for memory efficiency.

    Common implementations include:
    - Mean pooling: Computes the element-wise mean across the set
    - Max pooling: Takes the element-wise maximum across the set
    - Sum pooling: Computes the element-wise sum across the set
    - Attention-based pooling: Uses attention mechanisms to compute weighted aggregations

    Subclasses must implement the `forward_immediate` method to define the specific
    pooling operation. The default `forward_minibatch` implementation is not minibatch
    consistent and should be overridden by subclasses that require this property.
    """

    @abc.abstractmethod
    def forward_immediate(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        pass

    def forward_minibatch(
        self,
        src: Minibatches,
        state: Optional[Any]
    ) -> Union[torch.Tensor, Any]:
        """
        Default implementation for processing minibatches.

        This default implementation is NOT minibatch consistent. It simply processes
        each minibatch independently and accumulates the results, which may not yield
        the same result as processing the entire set at once.

        Subclasses that require minibatch consistency should override this method with
        an implementation that properly maintains state between minibatches to ensure
        the final result is equivalent to processing the entire set at once.

        Args:
            src: An iterable of minibatches to process
            state: Optional state from previous minibatch processing

        Returns:
            A tuple of (output, new_state) where output is the result of processing
            the minibatches and new_state is the updated state for future processing
        """
        warnings.warn(f"Layer '{self.__class__.__name__}' is not minibatch consistent.")
        result = 0.0
        for minibatch in src:
            result = result + self.forward_immediate(
                minibatch["src"], # type: ignore
                minibatch.get("src_multiplicities", None)
            )
        return result

    @overload
    def forward(
        self,
        src: torch.Tensor,
        src_multiplicities: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        ...

    @overload
    def forward(
        self,
        src: Minibatches,
    ) -> torch.Tensor:
        ...

    @overload
    def forward(
        self,
        src: Minibatches,
        *,
        state: Any
    ) -> Tuple[torch.Tensor, Any]:
        ...

    def forward(
        self,
        src: Union[torch.Tensor, Minibatches],
        src_multiplicities: Optional[torch.Tensor] = None,
        *,
        state: Optional[Any] = NoState
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, Any]]:
        # If we're in a stateful context, we need to treat all input as a minibatches
        if state is not NoState and isinstance(src, torch.Tensor):
            src = ({
                "src": src,
                "src_multiplicities": src_multiplicities,
            },)

        if isinstance(src, torch.Tensor):
            output = self.forward_immediate(src, src_multiplicities)
        else:
            initial_state = state if state is not NoState else None
            output, new_state = self.forward_minibatch(src, initial_state)
        if state is not NoState:
            return output, new_state
        return output
