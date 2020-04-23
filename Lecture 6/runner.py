import qsharp

from helpers import *
from MyAlgorithms import Main

# Uncomment this for DJ and BV
#while True:
#    s = Main.simulate()

#print(list(map(int, s)))

numBits = 4
orthVectors = []
while (True):
    sperp = Main.simulate()
    if (isLinIndep(orthVectors + [sperp])):
        orthVectors.append(sperp)
    if (len(orthVectors) == numBits - 1):
        break

orthVectors = list(map(lambda x: list(map(int, x)), orthVectors))

print(list(map(int, simonSysSolver(orthVectors))))