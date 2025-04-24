from pycatchrs import pycatchrs
from typeguard import typechecked
import numpy as np

@typechecked
def compute(x: np.ndarray, n:int) -> float:
    return pycatchrs.compute(x, n)

@typechecked
def zscore(x: np.ndarray) -> np.ndarray:
    return pycatchrs.zscore(x)