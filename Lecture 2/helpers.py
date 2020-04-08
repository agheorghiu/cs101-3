from typing import *
import functools

numBits = 5

# Binary string type
BinStr = NewType('BinStr', List[bool])

# some helper functions
def binaryDot(x: BinStr, y: BinStr) -> bool:
    return functools.reduce(lambda a, b: a ^ b, [(a & b) for (a, b) in zip(x, y)], False)

def toBinary(num: int) -> BinStr:
    return list(reversed([(num & (2**i)) > 0 for i in range(numBits)]))

def wrapperFun(f: Callable[[BinStr], bool]) -> Callable[[BinStr], int]:
    return (lambda x: (-1)**f(x))