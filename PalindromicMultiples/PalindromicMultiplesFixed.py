from collections import deque
import math
import multiprocessing
import resource
import sys

def reverseInt(n):
    return int(bin(n)[:1:-1], 2)

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

# DP Subset Sum
# Potentially unstable for even n (might return something when nothing should be valid)
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

# Do BFS over implicitly built DFA.
def algo4(n, output=None):
    # Setup tracking
    global pathTo
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
    result = output.get()
    algo1process.terminate()
    algo2process.terminate()
    algo3process.terminate()
    algo4process.terminate()
    return result

def memory_limit(systemMemFrac):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (get_memory() * 1024 * (systemMemFrac), hard))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory

if __name__ == "__main__":
    if True:
        memory_limit(0.4)
        n = 1
        with open("PalindromicMultiplesOutput.txt", "a") as outputFile:
            while n < 10000000:
                outputFile.write(" ".join([str(s) for s in multiAlgoSearch(n)]) + "\n")
                outputFile.flush()
                n += 2
    if False:
        n = 3054503
        #print(algo1(n))
        #print(algo2(n))
        #print(algo3(n))
        #print(algo4(n))
        print(multiAlgoSearch(n))
