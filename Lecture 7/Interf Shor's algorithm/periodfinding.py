from interf import *
from helpers import *
import math as math

# has period 1
def f0(x: int) -> int:
    return 1

# has period 2
def f1(x: int) -> int:
    return (x % 2) + 1

# has period 10
def f2(x: int) -> int:
    return (x % 10) + 1

# has period 14
def f3(x: int) -> int:
    return (2**x) % 43

# has period 42
def f4(x: int) -> int:
    return (3**x) % 43

# has period 16
def f5(x: int) -> int:
    return (3**x) % 64

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

# Plot Fourier transform of function
def prettyPlot(d: int, f: Callable[[Any], int]) -> None:
    newDomain = [(x, f(x)) for x in range(d)]
    T = lambda x, y: (x[1] == y[1]) * np.e**(2j * np.pi * (x[0] * y[0]) / d)
    fun = lambda x: 1
    interf2p(fun, T, newDomain)

# Find period of a function with domain range(d)
def periodFinder(f: Callable[[Any], int], d: int) -> int:
    if (f(0) == f(1)):
        return 1

    domain = range(d)
    newDomain = [(x, f(x)) for x in domain]

    T = lambda x, y: (x[1] == y[1]) * np.e**(-2j * np.pi * (x[0] * y[0]) / d)
    fun = lambda x: 1

    kmin = d
    for i in range(10):
        y1 = interf2(fun, T, newDomain)[0]
        y2 = interf2(fun, T, newDomain)[0]

        (a1, b1) = findClosestFraction(f, y1, d)
        (a2, b2) = findClosestFraction(f, y2, d)

        if (f(0) == f(b1) and b1 < kmin):
            kmin = b1

        if (f(0) == f(b2) and b2 < kmin):
            kmin = b2

        kCandidate = lcm(b1, b2)

        if (f(0) == f(kCandidate) and kCandidate < kmin):
            kmin = kCandidate

    return kmin

# Find order of an element in the modular multiplicative group mod N
def orderFinder(g: int, N: int) -> int:
    f = lambda x: pow(g, x, N)
    return periodFinder(f, N)

# Factoring using order finder
def factor(N: int) -> (int, int):
    numRuns = 10

    for i in range(numRuns):
        r = np.random.randint(2, N - 1)
        div = math.gcd(r, N)
        if (div > 1):
            return (div, N // div)

        order = orderFinder(r, N)
        if (order < N and order % 2 == 0):
            term1 = (pow(r, order // 2, N) - 1) % N
            term2 = (pow(r, order // 2, N) + 1) % N
            if (term1 > 0 and term2 > 0):
                return (math.gcd(term1, N), math.gcd(term2, N))

    return (1, N)