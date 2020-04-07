from interf import *

numBits = 5

def constant0(x: int) -> int:
    return 0

def constant1(x: int) -> int:
    return 1

def balanced1(x: int) -> int:
    return x % 2

def balanced2(x: int) -> int:
    if (x < (2**numBits)/2):
        return 0
    return 1

def balanced3(x: int) -> int:
    return 1 - balanced2(x)

def balanced4(x: int) -> int:
    if (x < (2**numBits) / 4):
        return 0
    elif (x < (2**numBits) / 2):
        return 1
    elif (x < 3*(2**numBits) / 4):
        return 0
    return 1

