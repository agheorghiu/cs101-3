from typing import *
import numpy as np
import math as math
import matplotlib.pyplot as plt
import qsharp
from qsimExample import hamSim

y0 = []
y1 = []

tme = np.linspace(0, 4 * math.pi, 200)

for t in tme:
    a, b = hamSim.simulate(time=t)
    y0 += [a]
    y1 += [b]

plt.plot(tme, y0, 'r')
plt.plot(tme, y1, 'b')
plt.show()