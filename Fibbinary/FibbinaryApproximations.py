import math
import re
import sys
import types

def roundUp(a):
    s = a.index("11") - 1
    while a[s-1:s+1] == "10" and s >= 1:
            s -= 2
    if s == -1:
        rounded = "1" + ("0" * len(a))
    else:
        rounded = a[:s] + "1" + ("0" * (len(a) - (s + 1)))
    return rounded

def roundDown(a):
    s = a.index("11") + 1
    rounded = a[:s] + "0" + ("10" * len(a))
    return rounded[:len(a)]

# All addIndex matches should be like (?=(...)) to not miss anything
# (nType, (addIndex, offset))
# nType and addIndex are compiled regular expressions
# offset is integer, list, or function that will receive n as input
# expressionList.append((re.compile(""), (re.compile("(?=())"), offsetFunction)))

KevinHareExpressions = []
# Kevin Hare Case 11...
KevinHareExpressions.append((re.compile("11[01]*"), (re.compile("(?=(11((00)|(0$)|$)))"), 2)))
KevinHareExpressions.append((re.compile("11[01]*"), (re.compile("(?=(101))"), 1)))
# Kevin Hare Case 10...
KevinHareExpressions.append((re.compile("10(10)*((0[01]*)|1)"), (re.compile("(?=(11(0|$)))"), 1)))
KevinHareExpressions.append((re.compile("10(10)*((0[01]*)|1)"), (re.compile("(?=(10(10)*11))"), 1)))

def approx(n, epsilon=10**-5, verbose=False, iterations=math.inf, expressionList=KevinHareExpressions, orderedRules=False):
    if verbose:
        print()
        print("Started trying to approximate n =", n, "=", bin(n)[2:])
        print()
    if not isinstance(n, int):
        print("Deal with this case externally")
        exit(1)

    # Get the valid locations to add
    expressions = []
    for nType, addLocation in expressionList:
        if re.fullmatch(nType, bin(n)[2:]):
            if isinstance(addLocation[1], types.FunctionType):
                offsets = addLocation[1](n)
            else:
                offsets = addLocation[1]
            if isinstance(offsets, int):
                expressions.append((addLocation[0], offsets))
            elif isinstance(offsets, list):
                for offset in offsets:
                    expressions.append((addLocation[0], offset))
            else:
                print("Rules loading failed")
                exit(1)

    b = 1
    i = 0 # The last index where we added b, to ensure that b remains fibbinary
    iteration = 0
    if verbose:
        print("Executing rules on:")
        print("n =", n, "=", bin(n)[2:])
        print("b =", b, "=", bin(b)[2:])
        print("n * b =", n * b, "=", bin(n * b)[2:])
    while iteration <= iterations:
        current = bin(n * b)[2:]
        # Check if we're overflowing, it affects the calculations for b
        overflow = 0
        if len(current) > (len(bin(b)[2:]) - 1) + len(bin(n)[2:]):
            overflow = 1

        # Check b for exact solution
        if "11" not in current:
            if verbose:
                print("Exact solution found:", n, "=", b * n, "/", b)
            return (n, b, n * b)

        # Check b for approximate solution
        if epsilon > 0:
            rounded = int(roundUp(current), 2)
            delta = abs((rounded / b) - n)
            down = int(roundDown(current), 2)
            if abs((down / b) - n) < delta:
                delta = abs((down / b) - n)
                rounded = down
            if delta < epsilon:
                if verbose:
                    print("Approximate solution found:", n, "=", rounded * n, "/", rounded)
                return (n, rounded, rounded * n)
        
        # Find all valid locations to add n
        if verbose:
            print("Running through rules")
        locations = []
        for rule in expressions:
            if verbose:
                print("Executing rule", rule[0].pattern)
            newLocations = [location.start() + rule[1] for location in re.finditer(rule[0], current)]
            if verbose:
                print("New valid add locations:", newLocations)
            locations.extend(newLocations)
        # Get the correct location
        if not orderedRules:
            if verbose:
                print("Sorting locations")
            locations.sort()
        if verbose:
            print("All valid add locations:", locations)
        for location in locations:
            if location > i + overflow + 1:
                if verbose:
                    print("Chosen location:", location)
                b = (b * (2 ** ((location - overflow) - i))) + 1
                i = location - overflow
                if verbose:
                    print("New b =", b, "=", bin(b)[2:])
                    print("Addition of n:")
                    line1 = current
                    line2 = (" " * location) + bin(n)[2:]
                    line4 = bin(n * b)[2:]
                    line3 = "-" * len(line4)
                    if len(line4) > len(line2):
                        line1 = " " + line1
                        line2 = " " + line2
                    print(line1)
                    print(line2)
                    print(line3)
                    print(line4)
                    print()
                break
        else:
            print("Failed to find valid rule")
            exit(1)

        iteration += 1
    if verbose:
        print("Ran out of iterations")
    return (n, b, n*b)

if __name__ == "__main__":
    if 1:
        # KevinHareExpressions.append((re.compile("11[01]*"), (re.compile("(?=(11((00)|(0$)|$)))"), 2)))
        # KevinHareExpressions.append((re.compile("11[01]*"), (re.compile("(?=(101))"), 1)))
        testExpressions1 = [*KevinHareExpressions]
        #testExpressions1.append((re.compile("111[01]*"), (re.compile("(?=(1101))"), 1))) # fixes 61
        #testExpressions1.append((re.compile("110[01]*"), (re.compile("(?=(111(0|$)))"), 1)))
        #testExpressions1.append((re.compile("1100[01]*"), (re.compile("(?=(11(00|((0$)|$))))"), 1))) # fixes 201

        testExpressions2 = []
        #testExpressions2.append((re.compile("11[01]*"), (re.compile("(?=(11((00)|(0$)|$)))"), lambda x: 2)))
        #testExpressions2.append((re.compile("11[01]*"), (re.compile("(?=(101))"), lambda x: 1)))
        #testExpressions2.append((re.compile("11[01]*010*"), (re.compile("(?=(101))"), lambda x: 1)))

        print(approx(125, epsilon=0, verbose=True, iterations=10, expressionList=testExpressions1))
        if 1:
            data = dict()
            lines = open("output.txt", "r").readlines()
            for line in lines:
                n, b, _ = map(int, line.split())
                data[n] = b
            for i in range(10000):
                if bin(i)[2:4] == "11":
                    result = approx(i, epsilon=0, iterations=20, expressionList=testExpressions1)
                    if "11" in bin(result[2])[2:] and data[i] != -1:
                        print("Didn't find at", i)
                        break
                    if "11" not in bin(result[2])[2:] and data[i] == -1:
                        print("Data wrong at", i)
                        break
    if 0:
        print(approx(201, epsilon=0, verbose=True, iterations=10))
    if 0:
        data = dict()
        lines = open("output.txt", "r").readlines()
        for line in lines:
            n, b, _ = map(int, line.split())
            data[n] = b
        for i in range(10000):
            if bin(i)[2:5] == "110":
                result = approx(i, epsilon=0, iterations=20)
                if "11" in bin(result[2])[2:] and data[i] != -1:
                    print("Didn't find at", i)
                    break
                if "11" not in bin(result[2])[2:] and data[i] == -1:
                    print("Data wrong at", i)
