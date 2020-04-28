from typing import *
import numpy as np
import math as math
import qsharp
from orderFinding import orderFindingHelper

# Compute the continued fraction expansion of y/d
def continuedFraction(y: int, d: int) -> List[int]:
    contFrac = []
    a = y
    b = d

    while True:
        if a == 0 or (a / b) < 1/d**2:
            break
        intPart = math.floor(b / a)
        contFrac += [intPart]
        temp = a
        a = b - a * intPart
        b = temp

    return contFrac

# Find closest fraction to y/d in the mod d integers
def findClosestFraction(f: Callable[[Any], int], y: int, d: int) -> (int, int):
    contFrac = continuedFraction(y, d)
    n = len(contFrac)

    a = 0
    b = 1

    for i in range(n):
        if (f(0) == f(b)):
            break

        preva = a
        prevb = b
        a = 0
        b = 1

        for j in range(i, -1, -1):
            tempa = a
            a = b
            b = contFrac[j] * b + tempa

        if (a >= d or b >= d):
            a = preva
            b = prevb
            break

    return (a, b)

# Compute lowest common multiple of a and b
def lcm(a: int, b: int) -> int:
    return abs(a*b) // math.gcd(a, b)


# Find order of an element in the modular multiplicative group mod N
# using Q#
def quantumOrderFinder(g: int, N: int) -> int:
    n = math.ceil(math.log2(N)) # should be twice this but my laptop couldn't handle it
    kmin = N
    f = lambda x: pow(g, x, N)
    for _ in range(5):
        y1 = orderFindingHelper.simulate(g=g, N=N, n=n)
        y2 = orderFindingHelper.simulate(g=g, N=N, n=n)

        (_, b1) = findClosestFraction(f, y1, N)
        (_, b2) = findClosestFraction(f, y2, N)

        if (f(0) == f(b1) and b1 < kmin):
            kmin = b1

        if (f(0) == f(b2) and b2 < kmin):
            kmin = b2

        kCandidate = lcm(b1, b2)

        if (f(0) == f(kCandidate) and kCandidate < kmin):
            kmin = kCandidate

    return kmin


# Factoring using order finder
def factor(N: int) -> (int, int):
    numRuns = 3

    orders = []

    for i in range(numRuns):
        r = np.random.randint(2, N - 1)
        div = math.gcd(r, N)
        if (div > 1):
            return (div, N // div)

        order = quantumOrderFinder(r, N)

        # show the element we found and its order
        print(r.__str__() + " " + order.__str__() + "\n")

        if (order < N and order % 2 == 0):
            term1 = (pow(r, order // 2, N) - 1) % N
            term2 = (pow(r, order // 2, N) + 1) % N
            if (term1 > 0 and term2 > 0):
                return (math.gcd(term1, N), math.gcd(term2, N))

    return (1, N)


print(factor(15))
