from typing import *
import numpy as np
import math as math
import random as random
import matplotlib.pyplot as plt
import qsharp
from randomCircuit import runCircuit
from randomCircuit import runCircuitInt

# Generate a random quantum circuit
# The circuit consistes of cycles. Each cycle has a layer of single-qubit gates, followed by a CNOT
# We only consider 3 possible single-qubit gates
# Returns a tuple of 2 lists. First list is the single-qubit gates (their index) and the index of
# the qubit on which the gate acts. Second list is just the indices on which the CNOT acts
def generateRandomCircuit(seed: int, numQubits: int, cycles: int) -> (List[List[int]], List[Tuple[int, int]]):
    random.seed(seed)

    singleQubitGates = []
    twoQubitGates = []

    for i in range(cycles):
        layer = []
        for j in range(numQubits):
            gateIdx = random.randint(0, 2)
            layer += [gateIdx]
        singleQubitGates += [layer]

        qubit1Idx, qubit2Idx = 0, 0
        while (qubit1Idx == qubit2Idx):
            qubit1Idx = random.randint(0, numQubits - 1)
            qubit2Idx = random.randint(0, numQubits - 1)

        twoQubitGates += [(qubit1Idx, qubit2Idx)]

    return (singleQubitGates, twoQubitGates)


# Create a random circuit, with the given seed, on numQubits qubits with numCycles cycles
# and run it numRuns times. Return estimated probability for all 0's output
def createAndRunCircuit(seed: int, numQubits: int, numCycles: int, numRuns: int) -> float:
    (singleQGates, twoQGates) = generateRandomCircuit(seed, numQubits, numCycles)
    results = []

    for _ in range(numRuns):
        res = runCircuitInt.simulate(numQubits=numQubits, singleQubitGates=singleQGates, twoQubitGates=twoQGates)
        results += [res]

    #plt.hist(results, bins=32)
    #plt.show()

    return results.count(0) / (2 ** numQubits)


seed = 1337
numQubits = 5
numCycles = 20
numRuns = 200

#createAndRunCircuit(seed, numQubits, numCycles, numRuns)

# Run 100 random circuits and plot a histogram of the probabilities that they output 00..0
zeros = []
for seed in range(1337, 1438):
    print(seed)
    zeros += [createAndRunCircuit(seed, numQubits, numCycles, numRuns)]

plt.hist(zeros, bins=100)
plt.show()
