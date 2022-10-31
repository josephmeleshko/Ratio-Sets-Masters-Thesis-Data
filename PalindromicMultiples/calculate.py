import math
import sys

# stack overflow
# https://stackoverflow.com/questions/18114138/computing-eulers-totient-function
def totient(n):
    phi = int(n > 1 and n)
    for p in range(2, int(n ** .5) + 1):
        if not n % p:
            phi -= phi // p
            while not n % p:
                n //= p
    #if n is > 1 it means it is prime
    if n > 1: phi -= phi // n 
    return phi

def worstCaseAntipalindrome(n):
    i = 0
    while n % 2 == 0:
        i += 1
        n //= 2
    s = n
    k = math.ceil(i / totient(s))
    u = (2**(k * totient(s)) - 1) * (2**(k * totient(s)))
    t = (2**(2 * k * s * totient(s)) - 1) // (2**(2 * k * totient(s)) - 1)
    print(s, i, k, u, bin(u), t, bin(t))
    return u*t

if __name__ == "__main__":
    f = open(sys.argv[1], "r")
    data = f.readlines()
    f.close()

    kDict = dict()
    nkDict = dict()
    algoDict = dict()

    count = dict()
    firstFewAlgo1 = []
    firstFewAlgo2 = []
    firstFewAlgo3 = []
    firstFewAlgo4 = []

    for line in data:
        n, k, nk, algo = line.split()
        kDict[int(n)] = int(k)
        nkDict[int(n)] = int(nk)
        algoDict[int(n)] = algo
        if algo not in count:
            count[algo] = 0
        count[algo] = count[algo] + 1
        if algo == 'algo1' and len(firstFewAlgo1) < 20:
            firstFewAlgo1.append(int(n))
        if algo == 'algo2' and len(firstFewAlgo2) < 20:
            firstFewAlgo2.append(int(n))
        if algo == 'algo3' and len(firstFewAlgo3) < 20:
            firstFewAlgo3.append(int(n))
        if (algo == 'algo4' or algo == 'algo5') and len(firstFewAlgo4) < 20:
            firstFewAlgo4.append(int(n))
    
    print(count)
    print(firstFewAlgo1)
    print(firstFewAlgo2)
    print(firstFewAlgo3)
    print(firstFewAlgo4)
