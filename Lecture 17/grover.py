from typing import *
import qsharp
from groverSearch import runGrover

def toInt(x: List[bool]) -> int:
    return sum([x[i]*(2**i) for i in range(len(x))])

numQubits = 6
n = 31

print('Grover result: ' + repr(toInt(runGrover.simulate(n=n, numQubits=numQubits))))