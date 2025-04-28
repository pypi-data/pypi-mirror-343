"""
Scaled Dot Product Attention implementations for set and multiset processing.

This module provides concrete implementations of the ScaledDotProductSetAttention
abstract base class defined in ust.api.modules. These implementations support
both immediate computation on full tensors and minibatch-consistent processing
for memory efficiency.

The implementations in this module have been tested for:
1. Equivalence with PyTorch's F.scaled_dot_product_attention
2. Consistency between multiset representations (with duplicates vs. with multiplicities)
3. Minibatch consistency
4. Numerical stability with large values (1000-10000)

Available implementations:
- ScaledDotProductSoftmaxSetAttention: Standard softmax-based attention
- ScaledDotProductSoftmaxFlashSetAttention: Optimized implementation using PyTorch's flash attention
- ScaledDotProductSigmoidSetAttention: Alternative attention using sigmoid activation
"""

import math
import torch
import torch.nn.functional as F
from typing import Any, Optional
import warnings

from ..api.modules import ScaledDotProductSetAttention

class ScaledDotProductSoftmaxSetAttention(ScaledDotProductSetAttention):
    """
    Scaled dot product attention with softmax activation for set processing.

    This implementation applies the softmax function to the scaled dot product of query and key,
    and then multiplies the result by the value tensor. It supports key multiplicities by adding
    the log of multiplicities to the attention scores before softmax, which is equivalent to
    weighting the attention by the multiplicities.

    This class provides both immediate computation for full tensors and numerically stable
    aggregation for minibatch processing. The minibatch implementation maintains running statistics
    (max value, normalization term) to ensure numerical stability when combining results from
    different minibatches.

    Key Features:
    - Fully minibatch-consistent: Processing a set in chunks yields the same result as processing it at once
    - Numerically stable: Uses log-space computations to handle large attention scores
    - Multiset support: Properly handles elements with multiplicities
    - Equivalent to PyTorch's F.scaled_dot_product_attention when used with full tensors

    Example:
        ```python
        # Create the attention layer
        attention = ScaledDotProductSoftmaxSetAttention(dropout_p=0.1)

        # Immediate computation on full tensors
        output = attention(query, key, value, key_multiplicities)

        # Or process in minibatches
        state = attention.initial_state()
        for batch in minibatches:
            state = attention(query, batch, state=state)
        output = attention.get(state)
        ```
    """
    def compute_immediate_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        """
        Compute softmax attention in a single forward pass.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor of shape (..., L_k, d_k)
            value: Value tensor of shape (..., L_k, d_v)
            key_multiplicities: Optional tensor of shape (..., L_k, 1) representing
                               the multiplicity of each key-value pair

        Returns:
            Attention output tensor of shape (..., L_q, d_v)
        """
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])
        attention = query @ key.transpose(-2, -1) * scale
        if key_multiplicities is not None:
            attention = attention + torch.log(key_multiplicities)
        attention = F.softmax(attention, dim=-1)
        attention = torch.dropout(attention, self.dropout_p, self.training)
        return attention @ value

    def compute_aggregated_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor],
        state: Any
    ):
        """
        Compute numerically-stable softmax attention for minibatch processing.

        This method implements a numerically stable version of softmax attention that
        can be aggregated across multiple minibatches. It maintains running statistics
        (max value, normalization term) to ensure numerical stability when combining
        results from different minibatches.

        The implementation uses a log-space approach to handle large attention scores
        without numerical overflow. When combining results from different minibatches,
        it carefully rescales previous results based on the maximum attention score
        to maintain numerical stability.

        Technical details:
        1. Compute attention scores as scaled dot product: scores = (Q @ K.T) * scale
        2. Add log of multiplicities to scores if provided
        3. Find maximum score for numerical stability
        4. Compute exp(scores - max_score) to get normalized attention weights
        5. Compute weighted sum of values: output = attention_weights @ V
        6. When combining with previous state, rescale based on which max is larger
        7. Update state with new aggregated values, normalization term, and max value

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor for the current minibatch of shape (..., L_k, d_k)
            value: Value tensor for the current minibatch of shape (..., L_k, d_v)
            key_multiplicities: Optional tensor of shape (..., L_k) representing
                               the multiplicity of each key-value pair in the current minibatch
            state: Dictionary containing the current state of the computation
                  (aggregated_value, normalization_term, max_value)

        Note:
            This implementation has been tested for numerical stability with attention
            scores up to 10,000 and maintains minibatch consistency across arbitrary
            partitioning of the input set.
        """
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])
        attention = query @ key.transpose(-2, -1) * scale
        if key_multiplicities is not None:
            attention = attention + torch.log(key_multiplicities.float()).unsqueeze(-2)
        max_value = attention.amax(dim=-1, keepdim=True)
        attention = torch.exp(attention - max_value)
        sp = attention.sum(dim=-1, keepdim=True)
        op = torch.dropout(attention, self.dropout_p, self.training) @ value

        if state["max_value"] is not None:
            # Not the first batch, we need to rescale to maintain numerical stability
            delta1 = torch.exp(state["max_value"] - max_value)
            delta2 = 1.0 / delta1
            bigger = max_value > state["max_value"]

            # Combine current batch with previous state, rescaling appropriately
            sp = torch.where(bigger, sp + state["normalization_term"] * delta1, state["normalization_term"] + sp * delta2)
            op = torch.where(bigger, op + state["aggregated_value"] * delta1, state["aggregated_value"] + op * delta2)
            max_value = torch.where(bigger, max_value, state["max_value"])

        # Update state with new values
        state["aggregated_value"] = op
        state["normalization_term"] = sp
        state["max_value"] = max_value

    def initial_state(self):
        """
        Initialize the state for minibatch processing.

        For softmax attention, we need to track:
        - aggregated_value: The unnormalized weighted sum of values
        - normalization_term: The sum of attention weights for normalization
        - max_value: The maximum attention score for numerical stability

        Returns:
            A dictionary containing the initial state variables
        """
        return {
            "aggregated_value": 0.0,
            "normalization_term": 0.0,
            "max_value": None
        }

    def get(self, state: Any):
        """
        Get the final normalized attention output after processing all minibatches.

        This method normalizes the aggregated value by the normalization term to
        produce the final softmax attention output. It also handles potential NaN
        values by replacing them with zeros.

        Returns:
            The normalized attention output tensor of shape (..., L_q, d_v)
        """
        output = state["aggregated_value"] / state["normalization_term"]
        # Zero-out any NaNs that might occur if normalization_term is zero
        return output.masked_fill(output.isnan(), 0.0)


class ScaledDotProductSoftmaxFlashSetAttention(ScaledDotProductSoftmaxSetAttention):
    """
    Optimized scaled dot product attention using PyTorch's flash attention implementation.

    This implementation leverages PyTorch's optimized `scaled_dot_product_attention` function,
    which can use flash attention when available for improved performance. It supports key
    multiplicities by passing them as an attention mask (log of multiplicities).

    Flash attention provides significant performance improvements, especially for large sequence
    lengths, by optimizing memory access patterns and reducing the memory footprint of the
    attention computation. This implementation is particularly useful for processing large sets.

    Note that this implementation falls back to the standard implementation for minibatch
    aggregation, as flash attention does not directly support the required aggregation operations.
    This means that while immediate computation will be faster, minibatch processing will use
    the same algorithm as the parent class.

    Key Features:
    - Improved performance: Uses PyTorch's optimized implementation for faster computation
    - Memory efficient: Reduces memory usage for large sets
    - Hardware acceleration: Takes advantage of specialized hardware when available
    - Multiset support: Properly handles elements with multiplicities

    Limitations:
    - Falls back to standard implementation for minibatch processing
    - Requires PyTorch 2.0+ for full benefits
    - May not be available on all hardware

    Example:
        ```python
        # Create the attention layer
        attention = ScaledDotProductSoftmaxFlashSetAttention(dropout_p=0.1)

        # Immediate computation on full tensors (uses flash attention)
        output = attention(query, key, value, key_multiplicities)

        # Minibatch processing (falls back to standard implementation)
        state = attention.initial_state()
        for batch in minibatches:
            state = attention(query, batch, state=state)
        output = attention.get(state)
        ```
    """
    def compute_immediate_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        """
        Compute softmax attention using PyTorch's optimized scaled_dot_product_attention function.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor of shape (..., L_k, d_k)
            value: Value tensor of shape (..., L_k, d_v)
            key_multiplicities: Optional tensor of shape (..., L_k, 1) representing
                               the multiplicity of each key-value pair

        Returns:
            Attention output tensor of shape (..., L_q, d_v)
        """
        # Use native scaled dot product attention with attention bias
        attn_bias = None
        if key_multiplicities is not None:
            attn_bias = torch.log(key_multiplicities)
        output = F.scaled_dot_product_attention(
            query,
            key,
            value,
            attn_mask = attn_bias,
            dropout_p = self.dropout_p,
            is_causal = False,
            scale = self.scale,
            enable_gqa = self.enable_gqa
        )
        # Zero NaNs that might occur with empty sets or numerical issues
        return output.masked_fill(output.isnan(), 0.0)

    def compute_aggregated_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor],
        state: Any
    ):
        """
        Compute aggregated attention for minibatch processing.

        Flash attention does not directly support the operations needed for proper
        minibatch aggregation, so this method falls back to the parent class implementation.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor for the current minibatch
            value: Value tensor for the current minibatch
            key_multiplicities: Optional multiplicity tensor for the current minibatch
        """
        warnings.warn("Softmax flash attention does not support minibatch aggregation. Falling back to naive implementation.")
        return super().compute_aggregated_attention(query, key, value, key_multiplicities, state)


class ScaledDotProductSigmoidSetAttention(ScaledDotProductSetAttention):
    """
    Scaled dot product attention with sigmoid activation for set processing.

    This implementation applies the sigmoid function to the scaled dot product of query and key,
    and then multiplies the result by the value tensor. Unlike softmax attention, sigmoid
    attention does not normalize across the key dimension, allowing each query to attend
    independently to each key.

    With sigmoid activation, key multiplicities are applied as a direct multiplication after
    the sigmoid, rather than in log space before normalization as in softmax attention.
    This makes the implementation more intuitive for certain applications.

    Sigmoid attention is simpler to aggregate across minibatches compared to softmax attention,
    as it doesn't require maintaining normalization terms or max values for numerical stability.
    This makes it particularly well-suited for distributed or streaming applications where
    simplicity and robustness are important.

    Key Features:
    - Independent attention: Each query-key pair is processed independently
    - Simpler minibatch aggregation: No need for complex normalization or stability measures
    - Multiset support: Properly handles elements with multiplicities
    - Different attention pattern: May be more suitable for certain tasks than softmax attention

    When to use:
    - When you want each query to independently attend to keys
    - When processing very large sets that require simple aggregation
    - When softmax attention produces too sparse attention patterns
    - When numerical stability is a concern with softmax attention

    Example:
        ```python
        # Create the attention layer
        attention = ScaledDotProductSigmoidSetAttention(dropout_p=0.1)

        # Immediate computation on full tensors
        output = attention(query, key, value, key_multiplicities)

        # Or process in minibatches
        state = attention.initial_state()
        for batch in minibatches:
            state = attention(query, batch, state=state)
        output = attention.get(state)
        ```
    """
    def compute_immediate_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor]
    ):
        """
        Compute sigmoid attention in a single forward pass.

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor of shape (..., L_k, d_k)
            value: Value tensor of shape (..., L_k, d_v)
            key_multiplicities: Optional tensor of shape (..., L_k, 1) representing
                               the multiplicity of each key-value pair

        Returns:
            Attention output tensor of shape (..., L_q, d_v)
        """
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])
        attention = query @ key.transpose(-2, -1) * scale
        attention = torch.sigmoid(attention)
        if key_multiplicities is not None:
            attention = attention * key_multiplicities
        attention = torch.dropout(attention, self.dropout_p, self.training)
        return attention @ value

    def compute_aggregated_attention(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_multiplicities: Optional[torch.Tensor],
        state: Any
    ):
        """
        Compute aggregated sigmoid attention for minibatch processing.

        For sigmoid attention, aggregation is straightforward as it simply accumulates
        the weighted values across minibatches without needing normalization. This makes
        the implementation simpler and more robust than softmax attention for minibatch
        processing.

        The sigmoid function maps each attention score independently to a value between
        0 and 1, which represents how much each query attends to each key. Since these
        values are independent, we can simply accumulate the weighted values across
        minibatches.

        Technical details:
        1. Compute attention scores as scaled dot product: scores = (Q @ K.T) * scale
        2. Apply sigmoid to get attention weights: weights = sigmoid(scores)
        3. Multiply by multiplicities if provided: weights = weights * multiplicities
        4. Apply dropout to attention weights
        5. Compute weighted sum of values: output = weights @ V
        6. Add to accumulated output in state: state["aggregated_value"] += output

        Args:
            query: Query tensor of shape (..., L_q, d_k)
            key: Key tensor for the current minibatch of shape (..., L_k, d_k)
            value: Value tensor for the current minibatch of shape (..., L_k, d_v)
            key_multiplicities: Optional tensor of shape (..., L_k) representing
                               the multiplicity of each key-value pair in the current minibatch
            state: Dictionary containing the current state of the computation
                  (aggregated_value)

        Note:
            This implementation is particularly useful for distributed or streaming
            applications where simplicity and robustness are important. It has been
            tested for minibatch consistency across arbitrary partitioning of the input set.
        """
        scale = self.scale or 1.0/math.sqrt(query.shape[-1])
        attention = query @ key.transpose(-2, -1) * scale
        attention = torch.sigmoid(attention)
        if key_multiplicities is not None:
            attention = attention * key_multiplicities.float().unsqueeze(-2)
        attention = torch.dropout(attention, self.dropout_p, self.training)
        state["aggregated_value"] = state["aggregated_value"] + attention @ value

    def initial_state(self):
        """
        Initialize the state for minibatch processing.

        For sigmoid attention, we only need to track the aggregated value.

        Returns:
            A dictionary containing the initial state
        """
        return {"aggregated_value": 0.0}

    def get(self, state: Any):
        """
        Get the final attention output after processing all minibatches.

        For sigmoid attention, no normalization is needed as each query-key pair
        is processed independently.

        Returns:
            The aggregated attention output tensor of shape (..., L_q, d_v)
        """
        return state["aggregated_value"]
