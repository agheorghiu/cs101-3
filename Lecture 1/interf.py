from typing import *
import numpy as np
import random as random

# Function performing interference
# fun : D -> {-1, +1}
# domain is a subset of D
# norm is a positive integer
# Computes S = 1/norm |sum_{x \in domain} fun(x)|
# returns True if S > 2/3 and False if S < 1/3
def interf1(fun: Callable[[int], int], domain: List[Any], norm: int) -> bool:
    res = sum(map(fun, domain)) / norm
    if (abs(res) >= 2/3):
        return True
    elif (abs(res) <= 1/3):
        return False
    return random.choice([True, False])



