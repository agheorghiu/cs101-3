from interf import *
from helpers import *


# BV functions
def bvFun1(x: BinStr) -> bool:
    s = [True, True, False, True, True]
    return binaryDot(x, s)

def bvFun2(x: BinStr) -> bool:
    s = [True, True, True, True, True]
    return binaryDot(x, s)

def bvFun3(x: BinStr) -> bool:
    s = list(map(lambda x: x % 2 == 0, range(numBits)))
    return binaryDot(x, s)



def bernsteinVazirani(f: Callable[[BinStr], bool]) -> BinStr:
    domain = list(map(toBinary, range(2**numBits)))
    fun = wrapperFun(f)
    T = (lambda x, y: (-1)**binaryDot(x, y))
    return interf2(fun, T, domain)

print(bernsteinVazirani(bvFun3))