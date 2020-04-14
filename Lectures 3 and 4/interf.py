from typing import *
import numpy as np
import random as random
import math

def interf1(fun: Callable[[int], int], domain: List[Any], norm: int) -> bool:
    res = sum(map(fun, domain)) / norm
    if (abs(res) > 2/3):
        return True
    elif (abs(res) < 1/3):
        return False
    return random.choice([True, False])

BinStr = NewType('BinStr', List[bool])

def interf2(fun: Callable[[Any], int], transf: Callable[[Any, Any], float], domain: List[Any]) -> Any:
    probs = [abs(sum(map(lambda x: fun(x) * transf(x, y), domain))) for y in domain]
    probs = np.true_divide(np.array(probs), sum(probs))
    if (math.isclose(sum(probs), 1, rel_tol=1e-15)):
        choice = np.random.choice(range(len(domain)), p=probs)
    else:
        choice = np.random.choice(range(len(domain)))
    return domain[choice]

