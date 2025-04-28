# Universal Set Transformers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.5+](https://img.shields.io/badge/pytorch-2.5+-red.svg)](https://pytorch.org/)

**Universal Set Transformers (UST)** is a PyTorch library for processing sets and multisets with transformer-based architectures. This library provides efficient implementations of set attention mechanisms that are permutation invariant and can handle sets of varying sizes.

## Features

- **Set and Multiset Processing**: Process sets and multisets with explicit multiplicity handling
- **Minibatch Consistency**: Process large sets in minibatches with guaranteed consistency
- **Efficient Attention Mechanisms**: Multiple attention implementations (softmax, sigmoid, flash attention)
- **State Management**: Explicit state handling for incremental processing
- **Numerical Stability**: Robust handling of large values and edge cases

## Installation

```bash
pip install universal-set-transformers
```

Or install from source:

```bash
git clone https://github.com/yourusername/universal-set-transformers.git
cd universal-set-transformers
pip install -e .
```

## Quick Start

### Basic Usage

```python
import torch
from ust.modules import SelfSetAttentionBlock, CrossSetAttentionBlock

# Create a self-attention block
self_attn = SelfSetAttentionBlock(
    d_model=32,
    nhead=4,
    dim_feedforward=64
)

# Process a set
x = torch.randn(2, 10, 32)  # batch_size=2, set_size=10, d_model=32
output = self_attn(x)

# Process a multiset with multiplicities
multiplicities = torch.randint(1, 5, (2, 10)).float()
output_with_mult = self_attn(x, multiplicities)
```

### Cross-Set Attention

```python
import torch
from ust.modules import CrossSetAttentionBlock

# Create a cross-attention block
cross_attn = CrossSetAttentionBlock(
    d_model=32,
    nhead=4,
    dim_feedforward=64
)

# Process two sets
x = torch.randn(2, 5, 32)   # batch_size=2, set_size=5, d_model=32
y = torch.randn(2, 10, 32)  # batch_size=2, set_size=10, d_model=32
output = cross_attn(x, y)

# Process with multiplicities
y_multiplicities = torch.randint(1, 5, (2, 10)).float()
output_with_mult = cross_attn(x, y, y_multiplicities)
```

### Minibatch Processing

```python
import torch
from ust.modules import CrossSetAttentionBlock

# Create a cross-attention block
cross_attn = CrossSetAttentionBlock(
    d_model=32,
    nhead=4,
    dim_feedforward=64
)

# Query set
x = torch.randn(2, 5, 32)  # batch_size=2, set_size=5, d_model=32

# Initialize state
state = cross_attn.attention.scaled_dot_product_attention.initial_state()

# Process first minibatch
y1 = torch.randn(2, 10, 32)
m1 = torch.randint(1, 5, (2, 10)).float()
output1, state = cross_attn(x, y1, m1, state=state)

# Process second minibatch
y2 = torch.randn(2, 8, 32)
m2 = torch.randint(1, 5, (2, 8)).float()
output2, state = cross_attn(x, y2, m2, state=state)

# Final output is output2
```

## Architecture

The library is organized into several modules:

- `ust.modules`: Core modules for set processing
  - `scaled_dot_product_attention.py`: Various attention mechanisms
  - `set_transformer.py`: Set Transformer implementation
- `ust.api`: Abstract interfaces and type definitions
- `ust.utils`: Utility functions

### Key Components

#### Attention Mechanisms

- `ScaledDotProductSoftmaxSetAttention`: Standard softmax attention for sets
- `ScaledDotProductSoftmaxFlashSetAttention`: Optimized flash attention for sets
- `ScaledDotProductSigmoidSetAttention`: Sigmoid attention for sets

#### Attention Blocks

- `MultiheadSetAttention`: Multi-head attention for sets
- `SelfSetAttentionBlock`: Self-attention block for sets
- `CrossSetAttentionBlock`: Cross-attention block for sets

#### Set Transformer Components

- `InducedSetAttentionBlock`: Induced set attention block
- `PoolingByMultiheadSetAttention`: Pooling mechanism for sets

## Advanced Features

### Explicit State Handling

```python
import torch
from ust.modules.scaled_dot_product_attention import ScaledDotProductSoftmaxSetAttention

# Create attention mechanism
attention = ScaledDotProductSoftmaxSetAttention()

# Initialize state
state = attention.initial_state()

# Process query and key-value pairs
query = torch.randn(2, 5, 32)
key = torch.randn(2, 10, 32)
value = torch.randn(2, 10, 32)

# Update state with first batch
state = attention.compute_aggregated_attention(query, key, value, None, state)

# Update state with second batch
key2 = torch.randn(2, 8, 32)
value2 = torch.randn(2, 8, 32)
state = attention.compute_aggregated_attention(query, key2, value2, None, state)

# Get final result
output = attention.get(state)
```

### Multiset Processing

```python
import torch
from ust.modules import SelfSetAttentionBlock

# Create a self-attention block
self_attn = SelfSetAttentionBlock(
    d_model=32,
    nhead=4,
    dim_feedforward=64
)

# Process a set with duplicates
x = torch.randn(2, 10, 32)
multiplicities = torch.tensor([
    [1, 2, 1, 3, 1, 1, 2, 1, 1, 1],
    [2, 1, 1, 1, 3, 2, 1, 1, 1, 2]
]).float()

# Process with multiplicities
output = self_attn(x, multiplicities)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
