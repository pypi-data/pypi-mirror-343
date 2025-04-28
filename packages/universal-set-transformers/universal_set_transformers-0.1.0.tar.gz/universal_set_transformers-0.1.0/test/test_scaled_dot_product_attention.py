import abc
import math
import torch
import torch.nn.functional as F
from typing import Callable, Type
import unittest
import warnings

from ust.api.modules import ScaledDotProductSetAttention

from ust.modules.scaled_dot_product_attention import (
    ScaledDotProductSoftmaxSetAttention,
    ScaledDotProductSoftmaxFlashSetAttention,
    ScaledDotProductSigmoidSetAttention
)


def scaled_dot_product_sigmoid_attention(q, k, v, scale=None):
    """Reference implementation of sigmoid attention for testing."""
    scale = scale or 1.0 / math.sqrt(q.shape[-1])
    return torch.sigmoid(q @ k.transpose(-2, -1) * scale) @ v


class TestScaledDotProductSetAttention:
    """Base test class for all ScaledDotProductSetAttention implementations."""

    class Mixin(unittest.TestCase, abc.ABC):
        """Mixin class with common tests for all attention implementations."""
        attention_cls: Type[ScaledDotProductSetAttention]
        reference_fn: Callable

        # Use setUpClass to suppress warnings for all tests in this class
        @classmethod
        def setUpClass(cls):
            # Store the original showwarning function
            cls._original_showwarning = warnings.showwarning
            # Replace it with a no-op function
            warnings.showwarning = lambda *args, **kwargs: None

        @classmethod
        def tearDownClass(cls):
            # Restore the original showwarning function
            if hasattr(cls, '_original_showwarning'):
                warnings.showwarning = cls._original_showwarning # type: ignore

        def setUp(self):
            """Set up common test data."""
            self.dropout_p = 0.0  # Disable dropout for deterministic testing
            self.attention = self.attention_cls(dropout_p=self.dropout_p)

            # Common test tensors
            torch.manual_seed(42)  # For reproducibility
            self.batch_size = 2
            self.q_len = 4
            self.k_len = 6
            self.d_k = 8
            self.d_v = 10

            # Create test tensors
            self.q = torch.randn(self.batch_size, self.q_len, self.d_k)
            self.k = torch.randn(self.batch_size, self.k_len, self.d_k)
            self.v = torch.randn(self.batch_size, self.k_len, self.d_v)
            # Multiplicities should be of shape (..., L_k) for the API
            self.multiplicities = torch.randint(1, 4, (self.batch_size, self.k_len)).float()

            # Create duplicated versions for multiset testing
            # Process each batch separately to handle different multiplicities
            self.k_dup = torch.zeros_like(self.k)
            self.v_dup = torch.zeros_like(self.v)

            # We'll create a version with duplicates for each test separately
            # This is because the duplicated tensors will have different lengths
            # depending on the multiplicities

        def test_reference_implementation(self):
            """Test that the implementation matches the reference implementation."""
            if self.reference_fn is None:
                self.skipTest("No reference function provided")

            # Test without multiplicities
            output = self.attention(self.q, self.k, self.v)

            # Call reference function with appropriate parameters
            if self.reference_fn == F.scaled_dot_product_attention:
                reference_output = self.reference_fn(
                    self.q, self.k, self.v,
                    dropout_p=self.dropout_p,
                    is_causal=False
                )
            else:
                reference_output = self.reference_fn(self.q, self.k, self.v)

            self.assertTrue(torch.allclose(output, reference_output, rtol=1e-5, atol=1e-5),
                           f"Max difference: {(output - reference_output).abs().max().item()}")

            # Test with multiplicities
            output_with_mult = self.attention(self.q, self.k, self.v, self.multiplicities)

            # Create duplicated version for this test
            k_dup_list = []
            v_dup_list = []
            for b in range(self.batch_size):
                k_dup_batch = torch.repeat_interleave(
                    self.k[b:b+1], self.multiplicities[b].long(), dim=1)
                v_dup_batch = torch.repeat_interleave(
                    self.v[b:b+1], self.multiplicities[b].long(), dim=1)
                k_dup_list.append(k_dup_batch)
                v_dup_list.append(v_dup_batch)

            # Process each batch separately
            reference_outputs = []
            for b in range(self.batch_size):
                if self.reference_fn == F.scaled_dot_product_attention:
                    batch_output = self.reference_fn(
                        self.q[b:b+1], k_dup_list[b], v_dup_list[b],
                        dropout_p=self.dropout_p,
                        is_causal=False
                    )
                else:
                    batch_output = self.reference_fn(self.q[b:b+1], k_dup_list[b], v_dup_list[b])
                reference_outputs.append(batch_output)

            reference_output_with_mult = torch.cat(reference_outputs, dim=0)

            self.assertTrue(torch.allclose(output_with_mult, reference_output_with_mult, rtol=1e-5, atol=1e-5),
                           f"Max difference: {(output_with_mult - reference_output_with_mult).abs().max().item()}")

        def test_multiset_consistency(self):
            """Test that the implementation is consistent between multiset representations."""
            # Test with explicit multiplicities
            output_with_mult = self.attention(self.q, self.k, self.v, self.multiplicities)

            # Create duplicated version for this test
            outputs_with_dup = []
            for b in range(self.batch_size):
                # Create duplicated tensors for this batch
                k_dup = torch.repeat_interleave(
                    self.k[b:b+1], self.multiplicities[b].long(), dim=1)
                v_dup = torch.repeat_interleave(
                    self.v[b:b+1], self.multiplicities[b].long(), dim=1)

                # Process this batch
                batch_output = self.attention(self.q[b:b+1], k_dup, v_dup)
                outputs_with_dup.append(batch_output)

            # Combine batch outputs
            output_with_dup = torch.cat(outputs_with_dup, dim=0)

            # They should be the same
            self.assertTrue(torch.allclose(output_with_mult, output_with_dup, rtol=1e-5, atol=1e-5),
                           f"Max difference: {(output_with_mult - output_with_dup).abs().max().item()}")

        def test_minibatch_consistency(self):
            """Test that processing in minibatches gives the same result as processing all at once."""
            # Process all at once
            full_output = self.attention(self.q, self.k, self.v, self.multiplicities)

            # Process in minibatches
            # Split keys and values into two minibatches
            split_idx = self.k_len // 2
            k1, k2 = self.k[:, :split_idx], self.k[:, split_idx:]
            v1, v2 = self.v[:, :split_idx], self.v[:, split_idx:]
            m1, m2 = self.multiplicities[:, :split_idx], self.multiplicities[:, split_idx:]

            # Initialize state
            state = self.attention.initial_state()

            # Process first minibatch
            self.attention.compute_aggregated_attention(self.q, k1, v1, m1, state)

            # Process second minibatch
            self.attention.compute_aggregated_attention(self.q, k2, v2, m2, state)

            # Get final result
            minibatch_output = self.attention.get(state)

            # They should be the same
            self.assertTrue(torch.allclose(full_output, minibatch_output, rtol=1e-5, atol=1e-5),
                           f"Max difference: {(full_output - minibatch_output).abs().max().item()}")

        def test_explicit_state_handling(self):
            """Test that explicit state handling works correctly."""
            # Process with implicit state handling
            output_implicit, _ = self.attention(self.q, self.k, self.v, self.multiplicities, state=self.attention.initial_state())

            # Process with explicit state handling
            state_explicit = self.attention.initial_state()
            self.attention.compute_aggregated_attention(self.q, self.k, self.v, self.multiplicities, state_explicit)
            output_explicit = self.attention.get(state_explicit)

            # They should be the same
            self.assertTrue(torch.allclose(output_implicit, output_explicit, rtol=1e-5, atol=1e-5),
                           f"Max difference: {(output_implicit - output_explicit).abs().max().item()}")

        def test_numerical_stability(self):
            """Test numerical stability with large values."""
            # Create test tensors with large values
            large_q = torch.randn(self.batch_size, self.q_len, self.d_k) * 10.0
            large_k = torch.randn(self.batch_size, self.k_len, self.d_k) * 10.0
            large_v = torch.randn(self.batch_size, self.k_len, self.d_v)

            # Process with large values
            output = self.attention(large_q, large_k, large_v)

            # Check that output doesn't contain NaNs or infinities
            self.assertFalse(torch.isnan(output).any(), "Output contains NaNs")
            self.assertFalse(torch.isinf(output).any(), "Output contains infinities")

        def test_extreme_numerical_stability(self):
            """Test numerical stability with extremely large values."""
            # Create test tensors with extremely large values
            extreme_q = torch.randn(self.batch_size, self.q_len, self.d_k) * 2000.0
            extreme_k = torch.randn(self.batch_size, self.k_len, self.d_k) * 2000.0
            extreme_v = torch.randn(self.batch_size, self.k_len, self.d_v)

            # Process with extremely large values
            output = self.attention(extreme_q, extreme_k, extreme_v)

            # Check that output doesn't contain NaNs or infinities
            self.assertFalse(torch.isnan(output).any(), "Output contains NaNs with extreme values")
            self.assertFalse(torch.isinf(output).any(), "Output contains infinities with extreme values")

            # Test with minibatch processing for numerical stability
            state = self.attention.initial_state()
            split_idx = self.k_len // 2
            k1, k2 = extreme_k[:, :split_idx], extreme_k[:, split_idx:]
            v1, v2 = extreme_v[:, :split_idx], extreme_v[:, split_idx:]

            # Process first minibatch
            self.attention.compute_aggregated_attention(extreme_q, k1, v1, None, state)

            # Process second minibatch
            self.attention.compute_aggregated_attention(extreme_q, k2, v2, None, state)

            # Get final result
            minibatch_output = self.attention.get(state)

            # Check that output doesn't contain NaNs or infinities
            self.assertFalse(torch.isnan(minibatch_output).any(),
                            "Minibatch output contains NaNs with extreme values")
            self.assertFalse(torch.isinf(minibatch_output).any(),
                            "Minibatch output contains infinities with extreme values")


class TestScaledDotProductSoftmaxSetAttention(TestScaledDotProductSetAttention.Mixin):
    """Tests for ScaledDotProductSoftmaxSetAttention."""

    def setUp(self):
        self.attention_cls = ScaledDotProductSoftmaxSetAttention
        self.reference_fn = F.scaled_dot_product_attention
        super().setUp()


class TestScaledDotProductSoftmaxFlashSetAttention(TestScaledDotProductSetAttention.Mixin):
    """Tests for ScaledDotProductSoftmaxFlashSetAttention."""

    def setUp(self):
        self.attention_cls = ScaledDotProductSoftmaxFlashSetAttention
        self.reference_fn = F.scaled_dot_product_attention
        super().setUp()

    def test_minibatch_consistency(self):
        """Override to check warning about fallback to naive implementation without printing it."""
        # Filter the expected warning
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Softmax flash attention does not support minibatch aggregation")
            super().test_minibatch_consistency()

        # Still verify that the warning is raised (but don't print it)
        with self.assertWarns(UserWarning):
            # Create a new state for this test
            state = self.attention.initial_state()
            # Just call once to trigger the warning
            self.attention.compute_aggregated_attention(
                self.q, self.k[:, :1], self.v[:, :1], self.multiplicities[:, :1], state
            )


class TestScaledDotProductSigmoidSetAttention(TestScaledDotProductSetAttention.Mixin):
    """Tests for ScaledDotProductSigmoidSetAttention."""

    def setUp(self):
        self.attention_cls = ScaledDotProductSigmoidSetAttention
        self.reference_fn = scaled_dot_product_sigmoid_attention
        super().setUp()


# Create a test runner that suppresses warnings
class SuppressWarningTextTestRunner(unittest.TextTestRunner):
    def run(self, test):
        # Suppress all warnings during test execution
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return super().run(test)


if __name__ == "__main__":
    # Use the custom test runner
    unittest.main(testRunner=SuppressWarningTextTestRunner())
