from interf import *
from helpers import *
import random as random


# Note below that the value of numBits changes; make sure to account for this when you test your implementation

numBits = 5

#s = [True, True, False, True, False]
# g(s) = 0
def f1(x: BinStr, y: BinStr) -> bool:
    sVals = [27, 30, 29, 20, 16, 0, 1, 6, 17, 4, 1, 9, 2, 16, 22, 31, 5, 4, 12, 21, 28, 13, 28, 25, 0, 13, 24, 21, 2,
             22, 0, 29]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)

#s = [True, False, False, False, True]
# g(s) = 1
def f2(x: BinStr, y: BinStr) -> bool:
    sVals = [14, 12, 29, 19, 2, 13, 31, 29, 0, 11, 31, 19, 30, 30, 23, 10, 2, 2, 12, 29, 22, 5, 20, 11, 5, 21, 5, 17,
             0, 20, 11, 12]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)

#s = [True, True, True, False, True]
# g(s) = 1
def f3(x: BinStr, y: BinStr) -> bool:
    sVals = [1, 20, 4, 12, 10, 0, 9, 5, 6, 4, 20, 23, 19, 30, 12, 12, 1, 21, 1, 29, 8, 5, 9, 5, 29, 17, 0, 0, 20,
             20, 25, 3]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)



numBits = 6

#s = [False, True, True, True, False, True]
# g(s) = 1
def f4(x: BinStr, y: BinStr) -> bool:
    sVals = [48, 52, 32, 16, 57, 21, 49, 61, 33, 6, 42, 14, 17, 32, 10, 32, 33, 23, 37, 25, 41, 40, 14, 46, 34, 23, 14,
             63, 56, 29, 0, 56, 14, 6, 46, 45, 3, 18, 15, 52, 23, 29, 40, 16, 36, 23, 52, 26, 8, 29, 60, 17, 23, 2, 37,
             34, 40, 61, 40, 62, 12, 48, 19, 51]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)



numBits = 7

#s = [True, True, True, False, True, True, True]
# g(s) = 0
def f4(x: BinStr, y: BinStr) -> bool:
    sVals =[119, 86, 32, 79, 10, 79, 63, 30, 21, 13, 75, 99, 111, 21, 11, 6, 39, 61, 108, 117, 22, 7, 102, 113, 68, 107,
            19, 36, 26, 52, 76, 73, 95, 49, 123, 68, 10, 5, 36, 63, 121, 106, 78, 78, 43, 9, 0, 19, 8, 33, 49, 75, 108,
            119, 14, 34, 50, 83, 10, 38, 14, 124, 55, 40, 52, 103, 126, 16, 34, 56, 9, 53, 121, 43, 66, 72, 116, 72,
            121, 72, 114, 124, 98, 91, 9, 78, 75, 14, 72, 34, 55, 93, 102, 99, 87, 80, 111, 10, 71, 70, 17, 81, 22,
            115, 18, 60, 17, 126, 108, 101, 23, 84, 8, 119, 61, 4, 116, 43, 102, 122, 97, 126, 53, 83, 119, 65, 6, 123]
    sx = toBinary(sVals[toInt(x)], numBits)
    return binaryDot(sx, y)