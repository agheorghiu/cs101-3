from interf import *
from helpers import *

# note that changing this d will change the periods of some of the functions below
d = 43

# has period 1
def f0(x: int) -> int:
    return 1

# has period 2
def f1(x: int) -> int:
    return (x % 2) + 1

# has period 5
def f2(x: int) -> int:
    return (x % 5) + 1

# has period 14
def f3(x: int) -> int:
    return (2**x) % d

# has period 42
def f4(x: int) -> int:
    return (3**x) % d

# has period 6
def f5(x: int) -> int:
    return (3**(x**2)) % d