from collections import deque
import math
import multiprocessing
import resource
import sys
import time

def reverseInt(n):
    return int(bin(n)[:1:-1], 2)

def isPalindrome(n):
    n = bin(n)[2:]
    return n == n[::-1]

invert = str.maketrans("01", "10") # This is used all over the place, seems like an efficient pythonic way of doing it
def isAntipalindrome(n):
    n = bin(n)[2:]
    return n[::-1] == n.translate(invert)

def isAntisquare(n):
    n = bin(n)[2:]
    return n[:len(n)//2] == n[len(n)//2:].translate(invert)

def antisquarecheck():
    for i in range(1, 10000):
        j = 1
        while True:
            if isAntisquare(i*j):
                print(i, "*", j, "=", i*j)
                break
            j += 1
            if j % 100000 == 0:
                print(i, "has no solution up to", j)

def findAntipalindromicMultiple(n):
    k = 1
    while True:
        if isAntipalindrome(k*n):
            print(n, "*", k, "=", n*k)
            break
        k += 1
        if k % 1000 == 0:
            print("No solution up to", k)

#https://stackoverflow.com/questions/15347174/python-finding-prime-factors
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

#findAntipalindromicMultiple(45)
#antipalindromecheck()

"""
# brute force
def algo1(n, output=None):
    k = 1
    while True:
        kn = bin(k * n)[2:]
        if kn == kn[::-1]:
            kn = int(kn, base=2)
            if output:
                output.put((n, kn//n, kn, "algo1"))
            return (n, kn//n, kn, "algo1")
        k += 2
"""

"""
# brute force antipalindrome
def algo1(n, output=None):
    k = 1
    while True:
        if isAntipalindrome(k*n):
            if output:
                output.put((n, k, n*k, "algo1"))
            return (n, k, n*k, "algo1")
        k += 1
"""

def algo1(n, output=None):
    k = 1
    while True:
        if isAntisquare(k*n):
            if output:
                output.put((n, k, n*k, "algo1"))
            return (n, k, n*k, "algo1")
        k += 1

"""
# Enumerate all palindromes k and check for the first one that is divisible by n.
def algo2(n, output=None):
    # Find kn = yay^R.
    lenkn = n.bit_length()
    odd = lenkn % 2
    a = 0
    y = 2 ** ((lenkn // 2) - 1)
    while True:
        kn = (y * (2 ** ((lenkn // 2) + odd))) + a + reverseInt(y)
        if kn % n == 0:
            if output:
                output.put((n, kn//n, kn, "algo2"))
            return (n, kn//n, kn, "algo2")
        if odd == 1 and a == 0:
            a = 2**(lenkn // 2)
        else:
            a = 0
            y += 1
            if y == 2 ** (lenkn // 2):
                if not odd:
                    y //= 2
                lenkn += 1
                odd = 1 - odd
"""

"""
# Enumerate all antipalindromes and check for the first one divisible by n
def algo2(n, output=None):
    if n == 1:
        return (1, 2, 2, "algo2")
    k = 2 ** ((n.bit_length() // 2) - 1)
    while True:
        bink = bin(k)[2:]
        apal = int(bink + bink.translate(invert)[::-1], 2)
        if apal % n == 0:
            if output:
                output.put((n, apal//n, apal, "algo2"))
            return (n, apal//n, apal, "algo2")
        k += 1
"""

"""
# DP Subset Sum
# Potentially unstable for even n (might return something when nothing should be valid)
# Palindrome
def algo3(n, output=None):
    lenkn = n.bit_length()
    odd = lenkn % 2
    while True:
        # Setup the problem set
        subsetSumSet = dict()
        for i in range(lenkn // 2):
            subsetSumSet[(lenkn - 1) - i] = ((2 ** i) + (2 ** ((lenkn - 1) - i))) % n
        if odd:
            subsetSumSet[lenkn // 2] = (2 ** (lenkn // 2)) % n
        # Setup the memoization and initial state
        precomputed = []
        subsetSumSolutions = dict()
        precomputed.append(2 ** (lenkn - 1))
        subsetSumSolutions[2 ** (lenkn - 1)] = subsetSumSet[lenkn - 1]
        if subsetSumSolutions[2 ** (lenkn - 1)] == 0:
            kn = (2 ** (lenkn - 1)) + reverseInt(2 ** (lenkn - 1))
            if output:
                output.put((n, kn//n, kn, "algo3"))
            return (n, kn//n, kn, "algo3")
        if odd:
            precomputed.append((2 ** (lenkn - 1)) + (2 ** (lenkn // 2)))
            subsetSumSolutions[(2 ** (lenkn - 1)) + (2 ** (lenkn // 2))] = (subsetSumSet[lenkn - 1] + subsetSumSet[lenkn // 2]) % n
            if subsetSumSolutions[(2 ** (lenkn - 1)) + (2 ** (lenkn // 2))] == 0:
                kn = ((2 ** (lenkn - 1)) + (2 ** (lenkn // 2))) + reverseInt((2 ** (lenkn - 1)) + (2 ** (lenkn // 2)))
                kn -= 2 ** (lenkn // 2)
                if output:
                    output.put((n, kn//n, kn, "algo3"))
                return (n, kn//n, kn, "algo3")
        # Run the problem
        for i in range(lenkn // 2 + odd, lenkn - 1):
            nextPrecomputed = []
            for j in precomputed:
                result = (subsetSumSolutions[j] + subsetSumSet[i]) % n
                resultIndex = j + (2 ** i)
                if result == 0:
                    kn = resultIndex + reverseInt(resultIndex)
                    if odd and ((2 ** (lenkn // 2)) & resultIndex):
                        kn -= 2 ** (lenkn // 2)
                    if output:
                        output.put((n, kn//n, kn, "algo3"))
                    return (n, kn//n, kn, "algo3")
                subsetSumSolutions[resultIndex] = result
                nextPrecomputed.append(resultIndex)
            precomputed = precomputed + nextPrecomputed
        # No solution found
        lenkn += 1
        odd = 1 - odd
"""

"""
# DP Subset Sum
# We build the subsets in a clever way to make it work as a subset sum problem
# For each index up to half way we have to add either 2^i or 2^{lenkn-i}, so we do subset sum with 2^i - 2^{lenkn-i} and adjust the goal by 2^{lenkn-i}
# O(nk) memory
def algo3(n, output=None):
    lenkn = (math.ceil(n.bit_length() / 2) * 2)
    while True:
        # Setup instance
        values = []
        goal = 0
        for i in range((lenkn // 2) - 1):
            values.append(((2 ** ((lenkn // 2) + i)) - (2 ** (((lenkn // 2) - 1) - i))) % n)
            goal = (goal - (2 ** (((lenkn // 2) - 1) - i))) % n
        goal = (goal - 1) % n
        if ((2 ** (lenkn - 1)) - 1) % n == goal:
            kn = "1" + ("0" * ((lenkn // 2) - 1))
            kn = int(kn + kn.translate(invert)[::-1], 2)
            if output:
                output.put((n, kn // n, kn, "algo3"))
            return (n, kn // n, kn, "algo3")
        pathTo = dict()
        orderedReached = [((2 ** (lenkn - 1)) - 1) % n]
        pathTo[((2 ** (lenkn - 1)) - 1) % n] = ""
        for i in range(len(values)):
            for j in range(len(orderedReached)):
                newValue = (orderedReached[j] + values[i]) % n
                if newValue in pathTo:
                    continue
                pathTo[newValue] = "1" + ("0" * (i - len(pathTo[orderedReached[j]]))) + pathTo[orderedReached[j]]
                orderedReached.append(newValue)
                if newValue == goal:
                    kn = "1" + ("0" * ((lenkn // 2) - len(pathTo[goal]) - 1)) + pathTo[goal]
                    kn = int(kn + kn.translate(invert)[::-1], 2)
                    if output:
                        output.put((n, kn // n, kn, "algo3"))
                    return (n, kn // n, kn, "algo3")
        lenkn += 2
"""

"""
# Do BFS over implicitly built DFA
# Palindrome
def algo4(n, output=None):
    # Setup tracking
    #global pathTo # Is this required? Why did I do this?
    pathTo = dict()
    bfsQueue = deque()
    # Setup initial states
    pathTo[(0, 2 % n, 0)] = ("", None, 0)
    bfsQueue.append((0, 2 % n, 0))
    pathTo[(0, 4 % n, 0)] = ("0", None, 1)
    bfsQueue.append((0, 4 % n, 0))
    pathTo[(1, 4 % n, 1)] = ("1", None, 1)
    bfsQueue.append((1, 4 % n, 1))
    # Loop
    while True:
        currentState = bfsQueue.popleft()
        nextStateZero = ((2 * currentState[0]) % n, (4 * currentState[1]) % n, currentState[2])
        if nextStateZero not in pathTo:
            pathTo[nextStateZero] = ("0", currentState, pathTo[currentState][2] + 2)
            bfsQueue.append(nextStateZero)
        elif (pathTo[nextStateZero][2] == pathTo[currentState][2] + 2) and (pathTo[nextStateZero][0] == "1"):
            pathTo[nextStateZero] = ("0", currentState, pathTo[currentState][2] + 2)
        nextStateOne = (((2 * currentState[0]) + 1 + currentState[1]) % n, (4 * currentState[1]) % n, 1)
        if nextStateOne not in pathTo:
            pathTo[nextStateOne] = ("1", currentState, pathTo[currentState][2] + 2)
            bfsQueue.append(nextStateOne)
        # Check for answer
        if nextStateOne[2] == 1 and nextStateOne[0] == 0:
            x = ""
            currentState = nextStateOne
            while True:
                path = pathTo[currentState]
                if path[1] == None:
                    x = x + path[0] + x[::-1]
                    kn = int(x, base=2)
                    if output:
                        output.put((n, kn//n, kn, "algo4"))
                    return (n, kn//n, kn, "algo4")
                else:
                    x += path[0]
                    currentState = path[1]
"""

"""
# Do BFS over implicitly built DFA
# Antipalindrome
# Simplified process
def algo4(n, output=None):
    # Hard coded small examples
    if n == 1:
        return (1, 2, 2, "algo4")
    if n == 2:
        return (2, 1, 2, "algo4")

    # Path to each state to recover solution later
    pathTo = dict()
    # List of integers reached (lexicographically ordered) (no duplicates reached)
    orderedReached = []
    # Setting up the problem (2 bit)
    orderedReached.append((1, 8 % n))
    pathTo[(1, 8 % n)] = (None, "0")
    orderedReached.append((2, 8 % n))
    pathTo[(2, 8 % n)] = (None, "1")

    # Main loop, each iteration adds two digits to attempted solutions
    while True:
        currentReached = [*orderedReached]
        orderedReached = []
        # adding 0 to front and 1 to back
        for x in currentReached:
            y = (((x[0] * 2) + 1) % n, (4 * x[1]) % n)
            if y not in pathTo:
                pathTo[y] = (x, "0")
                orderedReached.append(y)
        # adding 1 to front and 0 to back, these are valid antipalindromes so if they divide n we can accept them
        for x in currentReached:
            y = (((x[0] * 2) + x[1]) % n, (4 * x[1]) % n)
            if y not in pathTo:
                pathTo[y] = (x, "1")
                orderedReached.append(y)
            if y[0] == 0:
                kn = "1"
                previousState = x
                while previousState != None:
                    kn = kn + pathTo[previousState][1]
                    previousState = pathTo[previousState][0]
                kn = int(kn + kn.translate(invert)[::-1], 2)
                if output:
                    output.put((n, kn // n, kn, "algo4"))
                return (n, kn // n, kn, "algo4")
"""

"""
# Similar to algo4 but I think it uses more memory
# Antipalindrome
def algo5(n, output=None):
    # Hard coded small examples
    if n == 1:
        return (1, 2, 2, "algo5")
    if n == 2:
        return (2, 1, 2, "algo5")

    # List of integers reached (lexicographically ordered) (no duplicates reached)
    orderedReached = []
    # Set of all integers reached so we save redundant paths
    reached = set()
    # Setting up the problem (2 bit)
    orderedReached.append((1, "0"))
    reached.add(1)
    orderedReached.append((2, "1"))
    reached.add(2)

    # Main loop, each iteration adds two digits to attempted solutions
    while True:
        currentReached = [(2 * x[0] % n, x[1]) for x in orderedReached]
        orderedReached = []
        reached = set()
        # adding 0 to front and 1 to back
        for x in currentReached:
            y = (x[0] + 1) % n
            if y not in reached:
                reached.add(y)
                orderedReached.append((y, "0" + x[1]))
        # adding 1 to front and 0 to back, these are valid antipalindromes so if they divide n we can accept them
        for x in currentReached:
            y = (x[0] + (2 ** ((len(x[1]) * 2) + 1))) % n
            if y not in reached:
                reached.add(y)
                orderedReached.append((y, "1" + x[1]))
            if y == 0:
                kn = "1" + x[1]
                kn = kn + kn.translate(invert)[::-1]
                kn = int(kn, 2)
                if output:
                    output.put((n, kn // n, kn, "algo5"))
                return (n, kn // n, kn, "algo5")
"""

def multiAlgoSearch(n):
    output = multiprocessing.Queue()
    algo1process = multiprocessing.Process(target=algo1, args=(n, output))
    algo1process.start()
    algo2process = multiprocessing.Process(target=algo2, args=(n, output))
    algo2process.start()
    algo3process = multiprocessing.Process(target=algo3, args=(n, output))
    algo3process.start()
    algo4process = multiprocessing.Process(target=algo4, args=(n, output))
    algo4process.start()
    algo5process = multiprocessing.Process(target=algo5, args=(n, output))
    algo5process.start()
    result = output.get()
    algo1process.terminate()
    algo2process.terminate()
    algo3process.terminate()
    algo4process.terminate()
    algo5process.terminate()
    return result

def timerWrapper(func, n, output=None):
    start = time.process_time_ns()
    result = func(n)
    end = time.process_time_ns()
    if output:
        output.put((result, end - start))
    return (result, end - start)

def multiAlgoSearchNoHalt(n):
    output = multiprocessing.Queue()
    a1 = multiprocessing.Process(target=timerWrapper, args=(algo1, n, output))
    a2 = multiprocessing.Process(target=timerWrapper, args=(algo2, n, output))
    a3 = multiprocessing.Process(target=timerWrapper, args=(algo3, n, output))
    a4 = multiprocessing.Process(target=timerWrapper, args=(algo4, n, output))
    a5 = multiprocessing.Process(target=timerWrapper, args=(algo5, n, output))
    a1.start()
    a2.start()
    a3.start()
    a4.start()
    a5.start()

    r1 = output.get()
    r2 = output.get()
    r3 = output.get()
    r4 = output.get()
    r5 = output.get()

    if r2[0][0:3] != r1[0][0:3] or r3[0][0:3] != r1[0][0:3] or r4[0][0:3] != r1[0][0:3] or r5[0][0:3] != r1[0][0:3]:
        return (-1, "Something went wrong at " + str(n), r1, r2, r3, r4, r5)
    n, k, nk = r1[0][0:3]
    times = dict()
    times[r1[0][3]] = r1[1]
    times[r2[0][3]] = r2[1]
    times[r3[0][3]] = r3[1]
    times[r4[0][3]] = r4[1]
    times[r5[0][3]] = r5[1]
    return (n, k, nk, times["algo1"], times["algo2"], times["algo3"], times["algo4"], times["algo5"])

# Borrowed from stack overflow
def memory_limit(systemMemFrac):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (get_memory() * 1024 * (systemMemFrac), hard))

# Borrowed from stack overflow
def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory

if __name__ == "__main__":
    if False:
        print(multiAlgoSearchNoHalt(2))
    if False:
        memory_limit(0.4)
        n = 3
        with open("AntipalindromicMultiplesTimedOutput.txt", "a") as outputFile: # n k nk algo1time algo2time algo3time algo4time algo5time
            while n < 1000:
                result = multiAlgoSearchNoHalt(n)
                if result[0] == -1:
                    print(result)
                    break
                outputFile.write(" ".join([str(s) for s in result]) + "\n")
                outputFile.flush()
                n += 1
    if True:
        memory_limit(0.4)
        n = 3
        with open("AntisquareOutput.txt", "a") as outputFile: # n k nk algo
            while n < 10000000:
                result = algo1(n)
                if result[0] == -1:
                    print(result)
                    break
                outputFile.write(" ".join([str(s) for s in result]) + "\n")
                outputFile.flush()
                n += 1
    if False:
        n = 3054503
        #print(algo1(n))
        #print(algo2(n))
        #print(algo3(n))
        #print(algo4(n))
        print(multiAlgoSearch(n))
