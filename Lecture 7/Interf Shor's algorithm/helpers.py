from interf import *
import functools

# binary dot product between binary vectors
def binaryDot(x: BinStr, y: BinStr) -> bool:
    return functools.reduce(lambda a, b: a ^ b, [(a & b) for (a, b) in zip(x, y)], False)

# xor two binary vectors
def binaryAdd(x: BinStr, y: BinStr) -> bool:
    return [(a ^ b) for (a, b) in zip(x, y)]

# hamming weight of binary vector
def hammingWeight(x: BinStr) -> int:
    return sum(x)

# convert int to binary on numBits bits
def toBinary(num: int, numBits: int) -> BinStr:
    return list(reversed([(num & (2**i)) > 0 for i in range(numBits)]))

# convert binary to int
def toInt(x: BinStr) -> int:
    rx = list(reversed(x))
    return sum([rx[i]*(2**i) for i in range(len(rx))])

# rotate list by n elements
def rotate(l, n):
    return l[n:] + l[:n]

# wrapper to make Boolean function output +1, -1
def wrapperFun(f: Callable[[BinStr], bool]) -> Callable[[BinStr], int]:
    return (lambda x: (-1)**f(x))