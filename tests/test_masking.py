import numpy as np
import pytest

from somnum import spindle

@pytest.fixture
def data():
    """Returns a 100 element spindle class array with 3 classes occupying random
    sections of the data."""

    arr = np.array(['w'] * 100)
    sections = [('r', slice(11,16)), 
                ('r', slice(30, 44)),
                ('n', slice(66, 67)),
                ('n', slice(90, 94))]

    for state, section in sections:
        arr[section] = state

    return sections, arr


def test_mask(data):
    """"Test that the as_mask function correctly constructs a mask from
    a simulated spindle class array."""

    sections, spindle_classes = data

    # set the sampling rate and spindle_class resolution 
    fs = 10
    unit = 4

    # test combinations of maskable (token) states
    for token_state in [['r'], ['n'], ['r', 'n']]:

        # build the mask
        mask = spindle.as_mask(spindle_classes, states=token_state, fs=fs, 
                               unit=unit)

        # build the expected mask
        expected = np.zeros(len(spindle_classes) * fs * unit)
        for state, sl in sections:
            if state in token_state:
                samples = [sl.start * fs * unit, (sl.stop + 1) * fs * unit]
                expected[samples[0]:samples[-1]] = True


        assert np.allclose(mask, expected)

