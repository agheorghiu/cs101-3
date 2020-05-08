import json
import matplotlib.pyplot as plt

seed = 1337
numCircuits = 364
component = '00000'

probs = []
for seedValue in range(seed, seed + numCircuits):
    with open('results/ibmq_vigo_withSeed=' + seedValue.__str__()) as dataFile:
        counts = json.load(dataFile)

    # Get estimate for scaled probability
    if (component in counts):
        probs += [counts[component] / sum(counts.values())]
    else:
        probs += [0]

plt.hist(probs, bins=50)
plt.show()
