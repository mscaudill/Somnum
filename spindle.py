"""A collection of functions for working with spindle files."""

import csv

import numpy as np

from pathlib import Path
from typing import Union, Sequence


def read(fname: Union[str, Path], column: int, **kwargs):
    """Reads a SPINDLE sleep state CSV file into a 1-D numpy array


    Args:
        fname: 
            A path to a SPINDLE file.
        column:
            The column of the file containing the sleep state.
        kwargs:
            Any valid keyword argument for Python's CSV reader builtin.

    Returns:
        A 1-D array of the sleep classes.
    """

    with open(fname, 'r', newline='') as infile:
        row_reader = csv.reader(infile, **kwargs)

    return np.array([row[column] for row in row_reader])


def as_mask(arr, states, fs, unit):
    """Returns a 1-D boolean mask in samples from a 1-D array of spindle states
    in unit sized windows.
    
    Args:
        arr:
            A 1-D array of all SPINDLE states.
        states:
            A sequence of states that will survive masking.
        fs:
            The sampling rate of the system.
        unit:
            The amount of time between successive rows in the arr. This is the
            amount of time SPINDLE used to evaluate state.

    Returns:
        A 1-D boolean the same length as arr denoting which samples to keep
        (True) and which to ignore (False).
    """

    # build a mask in the window units
    submasks = [arr == state for state in states]
    window_mask = np.logical_or.reduce(submasks)

    # set boundaries to False always to ensure even num. of transitions
    window_mask[0] = False
    window_mask[-1] = False

    # compute indices of transitions and reshape into start, stop sections
    transitions = np.diff(window_mask)
    sections = np.flatnonzero(transitions).reshape(-1,2) + 1 #+1 for diff
    # be inclusive of last window
    sections[:, -1] += 1

    # build a mask in sample units
    mask = np.zeros(len(arr) * fs * unit)
    for section in sections:
        samples = section * fs * unit
        mask[slice(*samples)] = True

    return mask

            
        

