from typing import *
import numpy as np
import random as random
import math
import matplotlib.pyplot as plt


BinStr = NewType('BinStr', List[bool])

def interf1(fun: Callable[[Any], int], domain: List[Any], norm: int) -> bool:
    res = sum(map(fun, domain)) / norm
    if (abs(res) > 2/3):
        return True
    elif (abs(res) < 1/3):
        return False
    return random.choice([True, False])

def interf2(fun: Callable[[Any], complex], transf: Callable[[Any, Any], complex], domain: List[Any]) -> Any:
    probs = [abs(sum(map(lambda x: fun(x) * transf(x, y), domain)))**2 for y in domain]
    probs = np.true_divide(np.array(probs), sum(probs))
    if (math.isclose(sum(probs), 1, rel_tol=1e-15)):
        choice = np.random.choice(range(len(domain)), p=probs)
    else:
        choice = np.random.choice(range(len(domain)))
    return domain[choice]

def interf2p(fun: Callable[[Any], complex], transf: Callable[[Any, Any], complex], domain: List[Any]) -> Any:
    probs = [abs(sum(map(lambda x: fun(x) * transf(x, y), domain)))**2 for y in domain]
    probs = np.true_divide(np.array(probs), sum(probs))

    vals = probs
    y_pos = np.arange(len(vals))

    plt.bar(y_pos, vals, align='center', alpha=0.5)
    plt.xticks(y_pos, range(len(vals)))
    plt.ylabel('Probabilities')
    plt.title('QFT')

    plt.show()

    if (math.isclose(sum(probs), 1, rel_tol=1e-15)):
        choice = np.random.choice(range(len(domain)), p=probs)
    else:
        choice = np.random.choice(range(len(domain)))
    return domain[choice]


def interf22(f: Callable[[Any], int], g: Callable[[Any], int], transf: Callable[[Any, Any], float], domain: List[Any]) -> Any:
    probs = np.zeros(len(domain))
    N = len(domain)
    dom = zip(range(N), domain)
    for z in dom:
        for x in domain:
            for y in domain:
                probs[z[0]] += f(x) * transf(x, y) * g(y) * transf(y, z[1])
    probs = np.square(probs)
    print(probs)
    probs = np.true_divide(probs, sum(probs))
    print(probs)
    if (math.isclose(sum(probs), 1, rel_tol=1e-15)):
        choice = np.random.choice(range(len(domain)), p=probs)
    else:
        choice = np.random.choice(range(len(domain)))
    return domain[choice]

# Note that for Task 5 you can change the type signature of the functions so that fun and transf return complex instead of int
