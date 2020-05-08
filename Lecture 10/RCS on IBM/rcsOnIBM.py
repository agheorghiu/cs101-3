import random
import math
import json
import matplotlib.pyplot as plt
from qiskit import(
  QuantumCircuit,
  execute,
  IBMQ)
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from typing import *

# Generate random circuit for T-shaped 5-qubit chip
def generateRandomTCircuit(seed: int, numQubits: int, cycles: int) -> (List[List[int]], List[Tuple[int, int]]):
    random.seed(seed)

    singleQubitGates = []
    twoQubitGates = []

    for _ in range(cycles):
        layer = []
        for _ in range(numQubits):
            gateIdx = random.randint(0, 2)
            layer += [gateIdx]
        singleQubitGates += [layer]

        idxes = random.choice([(0, 1), (1, 0), (1, 2), (2, 1), (1, 3), (3, 1), (3, 4), (4, 3)])
        twoQubitGates += [idxes]

        # qubit1Idx, qubit2Idx = 0, 0
        # while (qubit1Idx == qubit2Idx):
        #     qubit1Idx = random.randint(0, numQubits - 1)
        #     qubit2Idx = random.randint(0, numQubits - 1)
        #
        # twoQubitGates += [(qubit1Idx, qubit2Idx)]

    return (singleQubitGates, twoQubitGates)


# load IBM account
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_vigo')

# set circuit parameters
seed = 1337
numQubits = 5
numCycles = 20
numRuns = 1000
numCircuits = 500

# Create the circuits and run them
zeros = []
for seedVal in range(seed, seed + numCircuits):
    print(seedVal)
    (singleQGates, twoQGates) = generateRandomTCircuit(seedVal, numQubits, numCycles)
    circuit = QuantumCircuit(numQubits, numQubits)

    # Add gates to the circuit
    for i in range(numCycles):
        for j in range(numQubits):
            # apply single qubit gates first
            gate = singleQGates[i][j]
            if (gate == 0):
                # Z rotation
                circuit.u3(0., 0., math.pi / 8., j)
            if (gate == 1):
                # Y rotation
                circuit.u3(math.pi / 8., 0., 0., j)
            if (gate == 2):
                # X rotation
                circuit.u3(math.pi / 8., -math.pi / 2., math.pi / 2., j)

        # apply CNOT
        idx1, idx2 = twoQGates[i]
        circuit.cx(idx1, idx2)

    circuit.measure(list(range(numQubits)), list(range(numQubits)))

    #circuit.draw(output='latex', filename='test_circ.png')

    # And run the circuit on a device
    job = execute(circuit, backend=backend, optimization_level=0, shots=numRuns)
    job_monitor(job)
    result = job.result()

    # Save results to file
    counts = result.get_counts(circuit)
    with open('ibmq_vigo_withSeed=' + seedVal.__str__(), 'w') as dataFile:
        json.dump(counts, dataFile)

    # Get the number of zeros
    if ('00000' in counts):
        zeros += [counts['00000']]
    else:
        zeros += [0]


print(zeros)

plt.hist(zeros, bins=100)
plt.show()
