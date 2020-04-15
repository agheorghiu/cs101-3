from interf import *
from helpers import *


numBits = 2

# Note the different values of k. We have 2 functions for each of the values k=2,3,4
# numBits is fixed at 2

# k = 2

# s = [False, True]
# g(s) = 1
def f1(xs: List[BinStr]) -> bool:
    sVals = [0, 2, 0, 2]
    x = xs[0]
    y = xs[1]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)

# s = [False, False]
# g(s) = 0
def f2(xs: List[BinStr]) -> bool:
    sVals = [0, 0, 0, 0]
    x = xs[0]
    y = xs[1]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)



# k = 3

# s = [True, False]
# g(s) = 1
def f3(xs: List[BinStr]) -> bool:
    sVals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 2, 3]
    x3 = xs[2]
    x1x2 = xs[0] + xs[1]
    sx = toBinary(sVals[toInt(x1x2)], numBits)
    return binaryDot(sx, x3)

# s = [True, True]
# g(s) = 1
def f4(xs: List[BinStr]) -> bool:
    sVals = [0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 2, 1, 0, 0, 0, 0]
    x3 = xs[2]
    x1x2 = xs[0] + xs[1]
    sx = toBinary(sVals[toInt(x1x2)], numBits)
    return binaryDot(sx, x3)



# k = 4

# s = [True, False]
# g(s) = 1
def f5(xs: List[BinStr]) -> bool:
    sVals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 2, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 0, 3]
    x4 = xs[3]
    x1x2x3 = xs[0] + xs[1] + xs[2]
    sx = toBinary(sVals[toInt(x1x2x3)], numBits)
    return binaryDot(sx, x4)


# s = [False, True]
# g(s) = 1
def f6(xs: List[BinStr]) -> bool:
    sVals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 2, 0, 2, 0, 0, 0, 0]
    x4 = xs[3]
    x1x2x3 = xs[0] + xs[1] + xs[2]
    sx = toBinary(sVals[toInt(x1x2x3)], numBits)
    return binaryDot(sx, x4)
