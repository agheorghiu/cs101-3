from interf import *
from helpers import *


# Note below that the value of numBits changes; make sure to account for this when you test your implementation

numBits = 3

# s = [True, False, True]
# g(s) = 1
def f1(x: BinStr, y: BinStr) -> bool:
    sVals = [0, 4, 0, 4, 4, 0, 6, 7]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)

# s = [True, True, True]
# g(s) = 0
def f2(x: BinStr, y: BinStr) -> bool:
    sVals = [7, 1, 6, 0, 6, 7, 0, 3]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)


numBits = 5

#s = [True, True, False, True, False]
# g(s) = 0
def f3(x: BinStr, y: BinStr) -> bool:
    sVals = [0, 25, 20, 3, 7, 14, 5, 12, 4, 9, 19, 0, 29, 8, 22, 14, 5, 18, 22, 22, 18, 5, 25, 11, 28, 0, 8, 3, 28, 7, 20, 3]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)

#s = [True, False, False, False, True]
# g(s) = 1
def f4(x: BinStr, y: BinStr) -> bool:
    sVals = [7, 24, 21, 4, 21, 1, 26, 15, 22, 2, 7, 27, 25, 4, 0, 23, 12, 26, 20, 14, 9, 22, 31, 14, 2, 11, 30, 19, 23, 14, 20, 14]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)

#s = [True, True, True, False, True]
# g(s) = 1
def f5(x: BinStr, y: BinStr) -> bool:
    sVals = [0, 18, 11, 5, 2, 7, 5, 25, 20, 0, 31, 7, 13, 8, 25, 17, 20, 28, 18, 13, 11, 1, 22, 30, 26, 5, 11, 3, 20, 25, 2, 0]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)



numBits = 6

#s = [False, True, True, True, False, True]
# g(s) = 1
def f6(x: BinStr, y: BinStr) -> bool:
    sVals = [41, 24, 0, 31, 47, 44, 32, 7, 54, 42, 10, 19, 13, 62, 52, 3, 20, 7, 33, 14, 11, 1, 41, 9, 52, 54, 28, 62,
             60, 7, 59, 37, 49, 4, 19, 30, 33, 38, 47, 37, 45, 41, 48, 49, 7, 43, 7, 55, 3, 13, 16, 63, 7, 27, 7, 20,
             37, 29, 21, 8, 3, 44, 29, 7]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)



numBits = 7

#s = [True, True, True, False, True, True, True]
# g(s) = 0
def f7(x: BinStr, y: BinStr) -> bool:
    sVals = [100, 31, 108, 73, 20, 13, 125, 55, 0, 127, 32, 74, 101, 69, 81, 29, 80, 100, 13, 60, 63, 27, 108, 112, 106,
             73, 123, 57, 49, 55, 24, 76, 55, 125, 100, 90, 0, 48, 18, 70, 118, 13, 69, 2, 67, 85, 16, 7, 111, 77, 61,
             112, 58, 112, 98, 39, 19, 71, 17, 21, 108, 82, 26, 68, 62, 98, 76, 47, 126, 118, 60, 63, 120, 22, 88, 33,
             123, 53, 66, 35, 52, 65, 90, 26, 57, 22, 119, 113, 13, 86, 127, 19, 91, 69, 70, 117, 97, 15, 3, 44, 120,
             42, 95, 122, 67, 79, 62, 82, 16, 104, 21, 124, 91, 98, 97, 6, 97, 79, 54, 82, 33, 126, 111, 91, 44, 9, 16,
             19]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)
