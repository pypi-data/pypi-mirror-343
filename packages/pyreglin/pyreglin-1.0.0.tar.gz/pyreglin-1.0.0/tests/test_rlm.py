import numpy as np
import pandas as pd
import pytest
from pyreglin import rlm

def test_rlm_basic():
    data = pd.DataFrame({
        'x': range(100),
        'group': ['A', 'B'] * 50
    })
    
    y = rlm(
        formula='x + group',
        beta=[1, 2, 3],
        sigma=1.0,
        data=data
    )
    
    assert isinstance(y, np.ndarray)
    assert len(y) == len(data)

def test_rlm_invalid_data():
    with pytest.raises(ValueError, match="data must be provided"):
        rlm(formula='x + 1', beta=[1, 2], sigma=1.0, data=None)

def test_rlm_invalid_sigma():
    data = pd.DataFrame({'x': range(10)})
    with pytest.raises(ValueError):
        rlm(formula='x + 1', beta=[1, 2], sigma=[1, 2, 3], data=data)

def test_rlm_invalid_beta():
    data = pd.DataFrame({'x': range(10)})
    with pytest.raises(ValueError):
        rlm(formula='x + 1', beta=[1, 2, 3], sigma=1.0, data=data)