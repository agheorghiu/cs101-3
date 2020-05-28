from typing import *
import numpy as np
import math as math
import random as random
from scipy.linalg import expm
import qsharp
from linearSysSolver import testHHL

# bound on condition number
cond = 2.

# precision to within which we want the solution
eps = 1/10.

# log(cond / eps)
lke = math.log(cond / eps)

# the functions below compute the Fourier series for 1/x for matrices and numbers respectively
J = math.ceil(cond / eps * lke)
K = 2 * math.ceil(cond * lke)

dely = eps / math.sqrt(lke)
delz = 1. / (cond * math.sqrt(lke))

def approxInvMat(x: List[List[complex]]) -> List[List[complex]]:
    mat = np.array(x)
    (m, n) = np.shape(mat)
    myApprox = np.zeros([m, n])

    for j in range(J):
        for k in range(-K, K):
            yj = j * dely
            zk = k * delz
            myApprox = np.add(myApprox, dely * delz * zk * np.exp(-zk * zk / 2.) * expm(-complex(0, 1) * mat * yj * zk))

    myApprox *= complex(0, 1) / math.sqrt(2 * math.pi)
    return myApprox

def approxInv(x: complex) -> complex:
    return approxInvMat([[x]])[0][0]


# generate the list of coefficients for the series expansion of 1/x
# as well as the list of coefficients in the exponents
def genSeriesCoeffs() -> (List[float], List[float]):
    seriesCoeffs = []
    expCoeffs = []

    for j in range(J):
        for k in range(-K, K):
            yj = j * dely
            zk = k * delz

            seriesCoeffs += [dely * delz * zk * np.exp(-zk * zk / 2.)]
            expCoeffs += [-yj * zk]

    return (seriesCoeffs, expCoeffs)

# pad list of coefficients with trailing 0's to the closest power of 2
def padWithZerosPow2(coeffs: List[float]) -> List[float]:
    n = len(coeffs)
    pow2 = 2 ** (math.ceil(math.log2(n)))
    newCoeffs = coeffs.copy() + ([0] * (pow2 - n))
    return newCoeffs

# test HHL solver; run it numRuns times and get results
# here we're testing with a 2x2 unitary
(l1, l2) = genSeriesCoeffs()

numRuns = 200
results = []
for i in range(numRuns):
    print(i)
    results += [testHHL.simulate(seriesCoeffs=padWithZerosPow2(l1), expCoeffs=padWithZerosPow2(l2))]

results = list(map(lambda pair: pair[1][0], filter(lambda pair: pair[0] == 0, results)))

print(results)
print([results.count(0) / len(results), results.count(1) / len(results)])
