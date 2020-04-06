import matplotlib.pyplot as plt
import numpy as np

def wDiceProb(i, j):
    if i > j:
        return -1
    return 1

def diceProb(i, j):
    return 1/36

def distProb(d):
    prob = 0
    for i in range(1, 7):
        for j in range(1, 7):
            if i + j == d:
                prob += wDiceProb(i, j)
    return prob

vals = np.array(list(map(distProb, range(2, 13))))
vals = vals / sum(abs(vals))

y_pos = np.arange(len(vals))

plt.bar(y_pos, vals, align='center', alpha=0.5)
plt.xticks(y_pos, range(2, len(vals) + 2))
plt.ylabel('Probability')
plt.title('Probability of distance')

plt.show()
