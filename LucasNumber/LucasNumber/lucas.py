"""Lucas Number Generator.(EE7:65)."""
from collections import deque
import numpy as np


def golden_ratio_calc(sequence):
    """
    Compute the golden ration based on the current sequence points.

    Parameters
    ----------
    sequence: list[int]
        Two most recent values from Lucas Number sequence.

    Return: float
        Calculated golden ratio
    """
    if np.max(sequence[0]) > np.max(sequence[1]):
        max_value = sequence[0]
    else:
        max_value = sequence[1]
    return (sequence[0] + sequence[1]) / max_value


def lucas_number_generator(seed):
    """
    Lucas number generator.

    Parameters
    ----------
    seed: list[int]
        Starting point for Lucas number generator. Two valid values required (e.g. [2,1])

    Return: list[int, float]
        Yields next Lucas number in sequence with current golden ratio
    """
    sequence = deque(seed)
    while True:
        lucas_number = sequence[0] + sequence[1]
        golden_ratio = golden_ratio_calc(sequence)
        next_ln = yield [lucas_number, golden_ratio]
        if next_ln is not None:
            sequence.append(next_ln)
            sequence.popleft()
