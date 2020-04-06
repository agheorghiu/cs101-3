from interf import *
from typing import *

# number of bits for input function
# Domain will be range(2^numBits)
numBits = 5

# examples of functions that are either constant or balanced
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

# implementing Deutsch-Jozsa

# wrapper function to turn the DJ function into a function that outputs -1, +1
def wrapperFun(f: Callable[[int], int]) -> Callable[[int], int]:
    return (lambda x: (-1)**f(x))

# setting the domain and the norm
domain = range(2**numBits)
norm = 2**numBits

# solving Deutsch-Jozsa; given f outputs True if f is constant and False if it's balanced
def djSolver(f: Callable[[int], int]) -> bool:
    return interf1(wrapperFun(f), domain, norm)


print(djSolver(constant0))
print(djSolver(constant1))
print(djSolver(balanced1))
print(djSolver(balanced2))
print(djSolver(balanced3))
print(djSolver(balanced4))
