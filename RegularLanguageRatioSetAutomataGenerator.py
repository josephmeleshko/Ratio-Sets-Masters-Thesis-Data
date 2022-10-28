from collections import deque
import math
from sys import argv

"""
Builds M(k, R(A,B), p/q).
Assumes A and B are read in MSD first.
Assumes start state of each machine M is state 0 and delta functions return some hashable value to designate a state.
Note that it doesn't include completely unreachable states

States are of the form (carry, q_A, q_b)
    carry: implicit difference between current carries
    q_A: current state of M_L(A)
    q_B: current state of M_L(B)

Arguments:
    p/q: rational p/q
    base: integer base
    delta_A(q_A, sigma_A) = q_A': transition function for machine M_A, takes state q_A and input sigma_A and returns q_A'
    delta_B(q_B, sigma_B) = q_B': transition function for machine M_B, takes state q_B and input sigma_B and returns q_B'
    runAll: builds the entire automata if true, otherwise stops early
    F_A(q_A) = bool: returns true if q is an accepting state of M_A, only required if runAll is true
    F_B(q_B) = bool: returns true if q is an accepting state of M_B, only required if runAll is true
"""
def generateAutomata(p, q, base, delta_A, delta_B, runAll=True, F_A=None, F_B=None):
    states = {}
    start = (0, 0, 0)
    states[start] = []
    queue = deque()
    queue.append(start)
    while queue:
        state = queue.popleft()
        for i in range(base): # sigma_A
            for j in range(base): # sigma_B
                newCarry = (q * i) - (p * j) + (base * state[0]) # rational carry equation
                if newCarry >= p or newCarry <= -q: # bound on carries
                    continue
                AState = delta_A(state[1], i)
                BState = delta_B(state[2], j)
                if AState == None or BState == None: # skip transition if M_A or M_B
                    continue
                newState = (newCarry, AState, BState)
                if newState not in states:
                    states[newState] = []
                    queue.append(newState)
                states[state].append((i, j, newState))
                if not runAll:
                    if newState[0] == 0 and F_A(newState[1]) and F_B(newState[2]):
                        return states
    return states

"""
Runs a BFS from the start state.
Saves the parent of each state in the parent dictionary.
Returns the parent dictionary as well as the first accepting state encountered.

Arguments:
    states: machine from generateAutomata
    F_A(q) = bool: returns true if q is an accepting state for machine M_A
    F_B(q) = bool: returns true if q is an accepting state for machine M_B
    runAll: computes the parent dictionary for all reachable states if True
"""
def findShortestPaths(states, F_A, F_B, runAll=False):
    queue = deque()
    start = (0, 0, 0)
    queue.append(start)
    parent = {}
    parent[start] = None
    firstAccept = None
    while queue:
        state = queue.popleft()
        for nextState in sorted(states[state]):
            if nextState[2] not in parent:
                parent[nextState[2]] = (nextState[0], nextState[1], state)
                if not firstAccept:
                    if nextState[2][0] == 0 and F_A(nextState[2][1]) and F_B(nextState[2][2]):
                        firstAccept = nextState[2]
                        if not runAll:
                            return (parent, nextState[2])
                queue.append(nextState[2])
    return (parent, firstAccept)

"""
Finds the shortest input that leads from the start to the goalState.
Returns said input as both a string and as a decimal.

Arguments:
    base: integer base
    parent: parent dictionary from findShortestPaths
    goalState: goal we are searching for.
"""
def findPathToState(base, parent, goalState):
    A = []
    B = []
    decimalA = 0
    decimalB = 0
    power = 1
    state = goalState
    while state:
        state = parent[state]
        if state:
            A.append(state[0])
            decimalA += state[0] * power
            B.append(state[1])
            decimalB += state[1] * power
            state = state[2]
            power *= base
    return (list(reversed(A)), list(reversed(B)), decimalA, decimalB)

"""
Run a reversed BFS starting from all the accepting states.
We can get then flag every state that could lead to an accept.
This lets us build a reduced automata that omits dead ends.

Arguments:
    states: machine from generateAutomata
    acceptA(q) = bool: returns true if q is an accepting state for machine M_L_A
    acceptB(q) = bool: returns true if q is an accepting state for machine M_L_B
"""
def pathScan(states, F_A, F_B):
    accepting = set()
    distanceToAccept = {}
    parents = {}
    parents[(0,0,0)] = []
    for state in states:
        for child in states[state]:
            if child[2] not in parents:
                parents[child[2]] = []
            parents[child[2]].append(state)
    queue = deque()
    for state in states:
        if state[0] == 0 and F_A(state[1]) and F_B(state[2]):
            accepting.add(state)
            for parent in parents[state]:
                queue.append((parent, 1))
    while queue:
        state, distance = queue.popleft()
        if state not in distanceToAccept or distance < distanceToAccept[state]:
            distanceToAccept[state] = distance
            for parent in parents[state]:
                queue.append((parent, distance+1))
    return accepting, distanceToAccept, parents

"""
Using the distanceToAccept dictionary and accepting set from pathScan,
we can reduce the automata to only states that have the possibility of leading to an accept.

Arguments:
    states: machine from generateAutomata
    accepting: set from pathScan
    distanceToAccept: dictionary from pathScan
"""
def simplifiedAutomata(states, accepting, distanceToAccept):
    newStates = {}
    for state in states:
        if state in accepting or state in distanceToAccept:
            newStates[state] = []
            for nextState in states[state]:
                if nextState[2] in accepting or nextState[2] in distanceToAccept:
                    newStates[state].append(nextState)
    return newStates

"""
Single function that generates the automata and then simplifies it and returns the simplified automata.

Arguments:
    p/q: rational p/q
    base: integer base
    delta_A(q_A, sigma_A) = q_A': transition function for machine M_A, takes state q_A and input sigma_A and returns q_A'
    delta_B(q_B, sigma_B) = q_B': transition function for machine M_B, takes state q_B and input sigma_B and returns q_B'
    F_A(q_A) = bool: returns true if q is an accepting state of M_A
    F_B(q_B) = bool: returns true if q is an accepting state of M_B
"""
def generateSimpleAutomata(p, q, base, delta_A, delta_B, F_A, F_B):
    automata = generateAutomata(p, q, base, delta_A, delta_B)
    accepting, distanceToAccept, parents = pathScan(automata, F_A, F_B)
    return simplifiedAutomata(automata, accepting, distanceToAccept)

"""
Front end to the complete algorithm. Builds the automata then finds the accepting input via BFS.
Returns (a, b) such that a/b = p/q, a \in A, and b \in B.

Arguments:
    p/q: rational p/q
    base: integer base
    delta_A(q_A, sigma_A) = q_A': transition function for machine M_A, takes state q_A and input sigma_A and returns q_A'
    delta_B(q_B, sigma_B) = q_B': transition function for machine M_B, takes state q_B and input sigma_B and returns q_B'
    F_A(q_A) = bool: returns true if q is an accepting state of M_A
    F_B(q_B) = bool: returns true if q is an accepting state of M_B
"""
def getSolution(p, q, base, delta_A, delta_B, F_A, F_B):
    states = generateAutomata(p, q, base, delta_A, delta_B, F_A=F_A, F_B=F_B, runAll=False)
    parents, acceptingState = findShortestPaths(states, F_A, F_B)
    if acceptingState:
        path = findPathToState(base, parents, acceptingState)
        if p * path[3] == q * path[2]:
            return (path[2], path[3])
        else:
            print("SOMETHING WENT WRONG")
            print(p, q, base)
            print(delta_A, delta_B, F_A, F_B, states, parents, acceptingState, path, flush=True)
            exit(1)
    else:
        return (-1, -1)

"""
Runs getSolution on n for start \leq n < stop.
For each run, prints "n 1 a b" for n = a/b, a \in A, and b \in B.
Prints all integers in base 10.

Arguments:
    start: integer starting point
    stop: integer end point
    base: integer base
    delta_A(q_A, sigma_A) = q_A': transition function for machine M_A, takes state q_A and input sigma_A and returns q_A'
    delta_B(q_B, sigma_B) = q_B': transition function for machine M_B, takes state q_B and input sigma_B and returns q_B'
    F_A(q_A) = bool: returns true if q is an accepting state of M_A
    F_B(q_B) = bool: returns true if q is an accepting state of M_B
"""
def bulkInteger(start, stop, base, delta_A, delta_B, F_A, F_B):
    for n in range(start, stop):
        solution = getSolution(n, 1, base, delta_A, delta_B, F_A, F_B)
        print(n, 1, solution[0], solution[1], flush=True)

"""
Runs getSolution on p/q for start \leq p < stop, 1 \leq q < p.
We only check q < p because the solution a and b for p/q is the solution b and a (i.e. swapped) for q/p.
For each run, prints "p q a b" for p/q = a/b, a \in A, and b \in B.
Prints all integers in base 10.

Arguments:
    start: integer starting point
    stop: integer end point
    base: integer base
    delta_A(q_A, sigma_A) = q_A': transition function for machine M_A, takes state q_A and input sigma_A and returns q_A'
    delta_B(q_B, sigma_B) = q_B': transition function for machine M_B, takes state q_B and input sigma_B and returns q_B'
    F_A(q_A) = bool: returns true if q is an accepting state of M_A
    F_B(q_B) = bool: returns true if q is an accepting state of M_B
"""
def bulkRational(start, stop, base, delta_A, delta_B, F_A, F_B):
    for p in range(start, stop):
        for q in range(1, p):
            if math.gcd(p, q) == 0:
                solution = getSolution(p, q, base, delta_A, delta_B, F_A, F_B)
                print(p, q, solution[0], solution[1], flush=True)

if __name__ == "__main__":
    if 1:
        # Example code to run this for fibbinary numbers
        def fibDelta(q, sigma):
            if q == 1 and sigma == 0:
                return 2
            if q == 1 and sigma == 1:
                return None
            if q == 2 and sigma == 0:
                return 2
            if q == 2 and sigma == 1:
                return 1
            if q == 0 and sigma == 0:
                return 0
            if q == 0 and sigma == 1:
                return 1 
        def fibAccept(q):
            return not q == 0
        base = 2
        p = 77
        q = 5

        print(getSolution(p, q, base, fibDelta, fibDelta, fibAccept, fibAccept))
