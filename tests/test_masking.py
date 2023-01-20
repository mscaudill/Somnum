import numpy as np
import pytest

from somnum import spindle

@pytest.fixture(scope="module")
def data():
    """Returns a 100 element 1-D array with 3 unique states ['w', 'r', 'n']."""

    arr = np.array(['w'] *100)
    states = [('r', slice(11,16)), 
              ('r', slice(30, 44)),
              ('n', slice(66, 67)),
              ('n', slice(90, 94))]

    for state, section in states:
        arr[sl] = state
    
    return arr

def test_onestate_mask(data):
    """" """

    mask = spindle_mask(data, states=['r'], fs=10, unit=4)
    expected = 
