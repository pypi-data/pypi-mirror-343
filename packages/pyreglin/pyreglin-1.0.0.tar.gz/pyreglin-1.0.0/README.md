# PYTHON REGLIN

A Python package for generating response variables with linear regression structure.

## Installation

```bash
pip install pyreglin
```

## Usage

```python
import pandas as pd
from pyreglin import rlm

# Create sample data
data = pd.DataFrame({
    'x': range(100),
    'group': ['A', 'B'] * 50
})

# Generate response variable
y = rlm(
    formula='x + group',
    beta=[1, 2, 3],
    sigma=1.0,
    data=data
)
```

## Features

- Generate response variables using linear regression structure
- Support for complex formulas using patsy syntax
- Support for categorical variables with custom contrasts