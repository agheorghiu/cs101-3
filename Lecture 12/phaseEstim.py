from typing import *
import numpy as np
import math as math
import matplotlib.pyplot as plt
import qsharp
from phaseEstimation import runPhaseEstimation

# convert binary to fraction
def binToFrac(x: List[int]) -> float:
    rx = list(reversed(x))
    return sum([rx[i]*(0.5 ** (i + 1)) for i in range(len(rx))])

res = runPhaseEstimation.simulate(n=5)
print(binToFrac(res))