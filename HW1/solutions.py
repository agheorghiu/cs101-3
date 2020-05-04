from interf import *
from helpers import *
import itertools
import dj

numBits = 2
domain = list(map(lambda x: toBinary(x, numBits), range(2 ** numBits)))


### Task 1 - interf1from2

# We're assuming norm is such that S = 1/norm | \sum_x f(x) | is normalized
def interf1from2(fun: Callable[[Any], int], domain: List[Any], norm: int) -> bool:
    n = len(domain)

    # if domain has only one element, we're done (sum has to be normalized)
    if (n == 1):
        return True

    # otherwise, fix 2 elements from the domain one for the > 2/3 result and one for the < 1/3 result
    y0 = domain[0]
    y1 = domain[1]

    # we're going to make our probabilities be proportional to S^2 and 1 - S^2
    # start by "squaring" the domain
    newDomain = [(x, y) for x in domain for y in domain]

    # next, choose T such that P(y0, y0) = S^2, P(y1, y1) = 1 - S^2
    def T(x, y):
        x0 = x[0]
        x1 = x[1]

        # for the y0 element, we make the probability be S^2
        if (y[0] == y[1] and y[0] == y0):
            return fun(x0) * fun(x1) / (norm ** 2)

        # for the y1 element, we make the probability be 1 - S^2
        if (y[0] == y[1] and y[0] == y1):
            return (norm/n - fun(x0)) * (norm/n + fun(x1)) / (norm ** 2)

        return 0

    # sample a constant number of times using interf2 and estimate S^2 as the number of times we see y0
    num0 = 0
    numRuns = 10
    for i in range(numRuns):
         if ((y0, y0) == interf2(lambda x: 1, T, newDomain)):
             num0 += 1

    # num0/numRuns is now an estimate for S^2; check whether this is greater than 4/9 or less than 1/9
    if (num0/numRuns >= 4/9):
        return True

    if (num0/numRuns <= 1/9):
        return False

    return random.choice([True, False])


### Task 2 - k-query interference

def interf2k(funList: List[Callable[[Any], int]], transfList: List[Callable[[Any, Any], float]], domain: List[Any]) -> Any:
    k = len(funList)
    n = len(domain)
    probs = []

    # create cartesian product of domain with itself k times
    newDomain = list(itertools.product(domain, repeat=k))

    # traverse all y values and compute probabilities
    for i in range(0, n):
        y = domain[i]
        probs += [0]
        for x in newDomain:
            # compute product for each term in the sum
            prod = 1
            for j in range(k - 1):
                prod *= funList[j](x[j]) * transfList[j](x[j], x[j + 1])
            prod *= funList[k - 1](x[k - 1]) * transfList[k - 1](x[k - 1], y)

            # add to probabilities
            probs[i] += prod

        # make positive
        probs[i] = abs(probs[i])

    # normalize probabilities
    probs = np.true_divide(np.array(probs), sum(probs))

    # perform the random sampling
    if (math.isclose(sum(probs), 1, rel_tol=1e-15)):
        choice = np.random.choice(range(len(domain)), p=probs)
    else:
        choice = np.random.choice(range(len(domain)))
    return domain[choice]


### Task 3 - Forrelation

# compute the forrelation sum using interf1
def forrelation(f: Callable[[BinStr], int], g: Callable[[BinStr], int]) -> bool:
    newDomain = [(x, y) for x in domain for y in domain]
    norm = 2 ** (3 * numBits / 2)
    fun = lambda x: f(x[0]) * g(x[1]) * (-1) ** binaryDot(x[0], x[1])
    return interf1(fun, newDomain, norm)


### Task 4A - Bernstein-Vazirani recursed twice

def g(x: BinStr) -> int:
    return int((hammingWeight(x) % 3) != 0)

# view problem as 2^n instances of regular BV, solve each one and then combine them to get one instance of BV
def bv2(f: Callable[[BinStr, BinStr], bool]) -> int:
    newDomain = [(x, y) for x in domain for y in domain]
    fun = lambda x: (-1)**f(x[0], x[1])
    const1 = lambda _: 1

    # First transformation is Hadamard on each 2^n-size block, this will make each block, x, be non-zero on the s_x entry
    # T1 = lambda u, v: int(u[0] == v[0]) * (-1)**(binaryDot(u[1], v[1]))

    # Make the non-zero entries be (-1)^g(s_x)
    # T2 = lambda u, v: int(u == v) * (-1)**g(u[1])

    # Combine previous 2 into one operation to improve performance
    T12 = lambda u, v: int(u[0] == v[0]) * (-1)**(binaryDot(u[1], v[1])) * (-1)**g(v[1])

    # Hadamard the x entries
    T3 = lambda u, v: (-1)**(binaryDot(u[0], v[0]))

    # output should be 1 only for entry s
    res = interf2k([fun, const1], [T12, T3], newDomain)

    # print it
    print(res[0])

    return g(res[0])

### Task 4B - Recursive Fourier Sampling (RFS)

# generalize the approach from BV2
def rfs(f: Callable[[List[BinStr]], bool], k: int) -> int:
    newDomain = list(itertools.product(domain, repeat=k))
    fun = wrapperFun(f)
    const1 = lambda _: 1

    # create list of functions
    funList = [fun] + list(itertools.repeat(const1, 2*k - 2))

    transfList = []

    # note that lambda functions use lazy evaluation and would just store currentK symbolically
    # for this reason we need to make the lambdas have 3 arguments, the first being currentK
    # and then invoke the function so that it uses the value of currentK in the for loop
    for currentK in range(k, 0, -1):
        # start by Hadamarding all blocks
        T1 = lambda inK=currentK: lambda u, v: \
            int(u[0:(inK - 1)] == v[0:(inK - 1)]) * (-1)**(binaryDot(u[inK - 1], v[inK - 1]))

        transfList += [T1(currentK)]

        # Make the non-zero entries be (-1)^g(s_{x_1, ... x_k-1})
        if (currentK > 1):
            T2 = lambda inK=currentK: lambda u, v: int(u == v) * (-1) ** g(u[inK - 1])
            transfList += [T2(currentK)]

    res = interf2k(funList, transfList, newDomain)
    print(res[0])

    # The above code will take a very long time to run for k = 3 and beyond
    # So another way to see that it's working is to convert everything to matrices and see what the output vector is
    # uncomment the code below for that

    # def toVector(f, domain):
    #     return np.array(list(map(f, domain)))
    #
    # def toMatrix(T, domain):
    #     mat = []
    #     for u in domain:
    #         line = []
    #         for v in domain:
    #             line += [T(u, v)]
    #         mat += [line]
    #     return np.array(mat)
    #
    # vec = toVector(fun, newDomain)
    # matList = list(map(lambda x: toMatrix(x, newDomain), transfList))
    #
    # for m in matList:
    #     vec = vec.dot(m)
    #
    # print(vec)
    #
    # in the vector vec, only the entries whose index starts with s will have non-zero entries
    # for instance, for k = 3, numBits = 2 and s =[1, 0] the indices of elements in vec are from
    # [0, 0, 0, 0, 0, 0] to [1, 1, 1, 1, 1, 1] (or 2**(n * k) = 64 components)
    # the entries that start with [1, 0, *, *, *, *] will be non-zero
    # this is what happens for instance with f3 from rfs.py

    return g(res[0])


### Task 5 - Period finding

# Compute the continued fraction expansion of y/d
def continuedFraction(y: int, d: int) -> List[int]:
    contFrac = []
    a = y
    b = d

    while True:
        if a == 0 or (a / b) < 1/d**2:
            break
        intPart = math.floor(b / a)
        contFrac += [intPart]
        temp = a
        a = b - a * intPart
        b = temp

    return contFrac

# Find closest fraction to y/d in the mod d integers
def findClosestFraction(f: Callable[[Any], int], y: int, d: int) -> (int, int):
    contFrac = continuedFraction(y, d)
    n = len(contFrac)

    a = 0
    b = 1

    for i in range(n):
        if (f(0) == f(b)):
            break

        preva = a
        prevb = b
        a = 0
        b = 1

        for j in range(i, -1, -1):
            tempa = a
            a = b
            b = contFrac[j] * b + tempa

        if (a >= d or b >= d):
            a = preva
            b = prevb
            break

    return (a, b)

# Compute lowest common multiple of a and b
def lcm(a: int, b: int) -> int:
    return abs(a*b) // math.gcd(a, b)

# Find period of a function with domain range(d)
def periodFinder(f: Callable[[Any], int], d: int) -> int:
    if (f(0) == f(1)):
        return 1

    domain = range(d)
    newDomain = [(x, f(x)) for x in domain]

    T = lambda x, y: (x[1] == y[1]) * np.e**(-2j * np.pi * (x[0] * y[0]) / d)
    fun = lambda x: 1

    kmin = d
    for i in range(10):
        y1 = interf2(fun, T, newDomain)[0]
        y2 = interf2(fun, T, newDomain)[0]

        (a1, b1) = findClosestFraction(f, y1, d)
        (a2, b2) = findClosestFraction(f, y2, d)

        if (f(0) == f(b1) and b1 < kmin):
            kmin = b1

        if (f(0) == f(b2) and b2 < kmin):
            kmin = b2

        kCandidate = lcm(b1, b2)

        if (f(0) == f(kCandidate) and kCandidate < kmin):
            kmin = kCandidate

    return kmin

