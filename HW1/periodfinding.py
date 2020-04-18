from interf import *
from helpers import *

d = 1024

# has period 1
def f0(x: int) -> int:
    return 1

# has period 2
def f1(x: int) -> int:
    return (x % 2) + 1

# has period 4
def f2(x: int) -> int:
    return (x % 4) + 1

# has period 14
def f3(x: int) -> int:
    return (2**x) % 43

# has period 42
def f4(x: int) -> int:
    return (3**x) % 43

# has period 16
def f5(x: int) -> int:
    return (3**x) % 64
