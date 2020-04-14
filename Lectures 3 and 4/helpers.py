import functools
from interf import *
from scipy.linalg import null_space

numBits = 5

# Gaussian elimination (special thanks to Matty J. Hoban)

# Create reduced row-echelon form
def rregf2(lst: List[BinStr]) -> np.ndarray:
    # convert everything to int and make it a numpy array
    mat = np.array(list(map(lambda row: list(map(lambda elem: int(elem), row)), lst)))
    m, n = mat.shape
    i, j = 0, 0
    while i < m and j < n:
        # find value and index of largest element in remainder of column j
        k = np.argmax(mat[i:, j]) + i

        if (mat[k, j] == 0):
            mat[i:, j] = 0
            j += 1
        else:
            # Swap i-th and k-th rows.
            mat[[k, i], j:] = mat[[i, k], j:]

            # current row
            row = np.copy(mat[i, j:])

            # add pivot mod 2 to all rows
            mat[:, j:] = (mat[:, j:] + np.outer(mat[:, j], row)) % 2

            # restore row
            mat[i, j:] = row

            i += 1
            j += 1
    return mat

# check for linear independence
def isLinIndep(lst: BinStr) -> bool:
    reduced = rregf2(lst)
    return np.linalg.matrix_rank(reduced) == len(lst)

# solve system in Simon's problem
def simonSysSolver(lst: List[BinStr]) -> BinStr:
    rref = rregf2(lst)
    sol = null_space(rref)
    s = []
    n = len(sol)
    for i in range(n):
        if (math.fabs(sol[i]) < 10.**(-15)):
            s += [False]
        else:
            s += [True]
    return s

# binary arithmetic helper functions
def binaryDot(x: BinStr, y: BinStr) -> bool:
    return functools.reduce(lambda a, b: a ^ b, [(a & b) for (a, b) in zip(x, y)], False)

def binaryAdd(x: BinStr, y: BinStr) -> BinStr:
    return [(a ^ b) for (a, b) in zip(x, y)]

def isOrthToAll(x: BinStr, vects: List[BinStr]):
    return functools.reduce(lambda a, b: a & b, list(map(lambda c: binaryDot(x, c), vects)), True)

# converting between binary and int
def toBinary(num: int) -> BinStr:
    return list(reversed([(num & (2**i)) > 0 for i in range(numBits)]))

def toInt(x: BinStr) -> int:
    rx = list(reversed(x))
    return sum([rx[i]*(2**i) for i in range(len(rx))])

# rotate list
def rotate(l, n):
    return l[n:] + l[:n]

# wrapper function to be used for interf
def wrapperFun(f: Callable[[BinStr], bool]) -> Callable[[BinStr], int]:
    return (lambda x: (-1)**f(x))


