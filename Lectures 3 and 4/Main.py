from helpers import *

def simon1(x: BinStr) -> BinStr:
    # [0, 1, 0, 0, 0]
    s = [False, True, False, False, False]
    x1 = toInt(x)
    x2 = toInt(binaryAdd(s, x))
    smallx = toBinary(min(x1, x2))
    return smallx

def simon2(x: BinStr) -> BinStr:
    # [0, 1, 0, 1, 1]
    s = [False, True, False, True, True]
    x1 = toInt(x)
    x2 = toInt(binaryAdd(s, x))
    smallx = toBinary(min(x1, x2))
    return binaryAdd(rotate(binaryAdd(smallx, toBinary(23)), 3), toBinary(17))

def simon3(x: BinStr) -> BinStr:
    # [1, 0, 1, 1, 1]
    s = [True, False, True, True, True]
    x1 = toInt(x)
    x2 = toInt(binaryAdd(s, x))
    smallx = toBinary(min(x1, x2))
    return smallx


domain = list(map(toBinary, range(2**numBits)))


def simonSolver(f: Callable[[BinStr], BinStr]) -> BinStr:
    newDomain = [(x, f(x)) for x in domain]

    T = lambda x, y: int(x[1] == y[1]) * (-1)**(binaryDot(x[0], y[0]))
    fun = lambda x: 1

    # collect orthogonal vectors
    ok = False
    orthVectors = []
    while (not ok):
        so = interf2(fun, T, newDomain)
        sperp = so[0]
        if (isLinIndep(orthVectors + [sperp])):
            orthVectors.append(sperp)
        if (len(orthVectors) == numBits - 1):
            ok = True

    # convert to true binary matrix
    orthVectors = list(map(lambda x: list(map(int, x)), orthVectors))

    # uncomment this to see the vectors it found
    # print(orthVectors)

    return simonSysSolver(orthVectors)


print(simonSolver(simon1))
print(simonSolver(simon2))
print(simonSolver(simon3))
