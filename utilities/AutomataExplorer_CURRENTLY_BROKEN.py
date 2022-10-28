from ast import literal_eval
import math
from RegularLanguageRatioSetAutomataGenerator import generateAutomata, pathScan, findAcceptingInput, findAcceptingPath
import re

# Need to update this to work with the rational number version

# Contains the setup for Fibbinary numbers.

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def b(binaryStringAsInt):
    return int(str(binaryStringAsInt), base=2)

class AutomataExplorer:
    def __init__(self, default = None):
        # Session Variables
        self.sessionName = None
        self.base = -1
        self.deltaA = None
        self.deltaB = None
        self.acceptA = None
        self.acceptB = None

        # Automata Instance Variables
        self.N = -1
        self.A = []
        self.B = []
        self.path = []
        self.currentState = None
        self.states = None
        self.accepting = None
        self.distanceToAccept = None
        self.parents = None
        
        # Organization Variables
        self.skipDraw = False
        
        if default == "fibbinary/fibbinary":
            self.setupFibbinaryFibbinary()

    def setupInstance(self):
        self.N = -1
        self.A = []
        self.B = []
        self.path = []
        self.currentState = None
        self.states = None
        self.accepting = None
        self.distanceToAccept = None
        self.parents = None

    def setupFibbinaryFibbinary(self):
        self.sessionName = "fibbinary/fibbinary"
        self.base = 2
        def delta_A(q, sigma):
            if q == 0 and sigma == 0:
                return 2
            if q == 0 and sigma == 1:
                return 1
            if q == 1 and sigma == 0:
                return 3
            if q == 1 and sigma == 1:
                return 2
            if q == 2 and sigma == 0:
                return 2
            if q == 2 and sigma == 1:
                return 2
            if q == 3 and sigma == 0:
                return 3
            if q == 3 and sigma == 1:
                return 1
        def delta_B(q, sigma):
            if q == 0 and sigma == 0:
                return 0
            if q == 0 and sigma == 1:
                return 1
            if q == 1 and sigma == 0:
                return 3
            if q == 1 and sigma == 1:
                return 2
            if q == 2 and sigma == 0:
                return 2
            if q == 2 and sigma == 1:
                return 2
            if q == 3 and sigma == 0:
                return 3
            if q == 3 and sigma == 1:
                return 1
        def accept(q):
            return q == 1 or q == 3
        self.deltaA = delta_A
        self.deltaB = delta_B
        self.acceptA = accept
        self.acceptB = accept

    def displayInfo(self, allStates = False):
        print("-----------------------------------------------")
        print("Session =", self.sessionName)
        print("base =", self.base)
        print("N =", self.N, "(" + "".join([str(x) for x in numberToBase(self.N, self.base)]) + "_" + str(self.base) + ")" if self.N > 1 and self.N < 11 else "") 
        if self.N > 1:
            print("A =", "".join([str(x) for x in self.A]))
            print("B =", "".join([str(x) for x in self.B]))
            if allStates:
                print("Next States (All):")
                for state in self.states[self.currentState]:
                    print( "("+str(state[0])+","+str(state[1])+")", "->", state[2],
                           " (Accept State)" if state[2] in self.accepting else "",
                           "(" + str(self.distanceToAccept[state[2]]) + " to Accept)" if state[2] in self.distanceToAccept else "")
            else:
                print("Current State =", self.currentState, "(Accept State)" if self.currentState in self.accepting else "")
                if self.currentState:
                    if self.currentState in self.distanceToAccept:
                        print("Next States (Leading to Accepts):")
                        for state in self.states[self.currentState]:
                            if state[2] in self.distanceToAccept or state[2] in self.accepting:
                                print( "("+str(state[0])+","+str(state[1])+")", "->", state[2], 
                                       ("(" + str(self.distanceToAccept[state[2]]) + " to accept)") if state[2] in self.distanceToAccept else "",
                                       "(Accept State)" if state[2] in self.accepting else "")
                    else:
                        print("Next States (Dead ends):")
                        for state in self.states[self.currentState]:
                            print("("+str(state[0])+","+str(state[1])+")", "->", state[2])
        print("-----------------------------------------------")

    def doStep(self, sigmaA, sigmaB):
        for state in self.states[self.currentState]:
            if state[0] == sigmaA:
                if state[1] == sigmaB:
                    self.path.append(self.currentState)
                    self.currentState = state[2]
                    self.A.append(sigmaA)
                    self.B.append(sigmaB)
                    break
        else:
            print("Invalid Step")
            self.skipDraw = True

    def coreLoop(self):
        while True:
            if self.skipDraw:
                self.skipDraw = False
            else:
                self.displayInfo()

            command = input("> ").strip().lower().split()

            if command == []:
                continue

            try:
                # Exit commands

                if command[0] in ["e", "end", "exit", "exit()", "q", "q!", "quit", "x", "z", "zz"]:
                    break

                # Setup Commands

                elif command[0] in ["l", "load"]:
                    if command[1] == "fibbinary/fibbinary":
                        self.setupInstance()
                        self.setupFibbinaryFibbinary()

                elif command[0] in ["n", "new"] or command[0].split("=")[0] == "n":
                    self.setupInstance()
                    self.N = int(command[1]) if len(command) == 2 else int(command[0].split("=")[1])
                    self.states = generateAutomata(self.base, self.N, self.deltaA, self.deltaB)
                    self.accepting, self.distanceToAccept, self.parents = pathScan(self.states, self.acceptA, self.acceptB)
                    self.currentState = (0, 0, 0)

                # Instance Commands

                elif command[0] in ["s", "step"]:
                    if len(command) == 1:
                        nextStates = sorted([(self.distanceToAccept[state[2]] if state[2] in self.distanceToAccept else math.inf, state[1], state[0]) for state in self.states[self.currentState]])
                        sigmaA = nextStates[0][2]
                        sigmaB = nextStates[0][1]
                    elif len(command) == 3:
                        sigmaA = int(command[1])
                        sigmaB = int(command[2])
                    else:
                        _, sigmaA, sigmaB = filter(None, re.split("[,./ ]+", " ".join(command)))
                        sigmaA = int(sigmaA)
                        sigmaB = int(sigmaB)
                    self.doStep(sigmaA, sigmaB) 
                        
                elif command[0] in ["m", "ms", "multis", "mstep", "multistep", "w", "walk"]:
                    for x in range(int(command[1])):
                        nextStates = sorted([(self.distanceToAccept[state[2]] if state[2] in self.distanceToAccept else math.inf, state[1], state[0]) for state in self.states[self.currentState]])
                        sigmaA = nextStates[0][2]
                        sigmaB = nextStates[0][1]
                        self.doStep(sigmaA, sigmaB)

                elif command[0] in ["b", "back"]:
                    for x in range(int(command[1]) if len(command) == 2 else 1):
                        self.currentState = self.path.pop()
                        self.A.pop()
                        self.B.pop()

                elif command[0] in ["g", "goto"]:
                    state = literal_eval(" ".join(command[1:]))
                    if state in self.states:
                        self.path.append(self.currentState)
                        self.currentState = state
                        self.A.append("#")
                        self.B.append("#")
                    else:
                        print("State doesn't exist")
                        self.skipDraw = True

                elif command[0] in ["i", "initial"]:
                    self.path.append(self.currentState)
                    self.currentState = (0, 0, 0)
                    self.A.append("#")
                    self.B.append("#")

                elif command[0] in ["alledges", "showall"]:
                    self.displayInfo(allStates = True)
                    self.skipDraw = True

                # Utilities

                elif command[0] in ["r", "result"]:
                    N = eval(command[1])
                    states = generateAutomata(self.base, N, self.deltaA, self.deltaB)
                    result = findAcceptingPath(states, self.acceptA, self.acceptB)
                    if result:
                        result2 = findAcceptingInput(self.base, result[0], result[1])
                        print("A =", result2[0], "(" + str(int("".join([str(x) for x in result2[0]]), base=self.base)) + ")" if self.base < 10 else "")
                        print("B =", result2[1], "(" + str(int("".join([str(x) for x in result2[1]]), base=self.base)) + ")" if self.base < 10 else "")
                        print("N =", numberToBase(N, self.base), "(" + str(N) + ")")
                    else:
                        print("N =", numberToBase(N, self.base), "(" + str(N) + ") <- No solution")
                    self.skipDraw = True


                elif command[0] in ["c", "convert"]:
                    fromBase = int(command[1])
                    toBase = int(command[2])
                    if fromBase == 10:
                        x = eval(" ".join(command[3:]))
                    else:
                        x = int(command[3], base=fromBase)
                    if toBase > 10:
                        print(numberToBase(x, toBase))
                    else:
                        print("".join([str(y) for y in numberToBase(x, toBase)]))
                    self.skipDraw = True

                elif command[0] in ["d", "do"]:
                    #exec("print(" + " ".join(command[1:]) + ")")
                    print(eval(" ".join(command[1:])))
                    self.skipDraw = True

                # Help Message

                elif command[0] in ["h", "help", "?"]:
                    print("[h]elp Message:")
                    print("[q]uit - quits (alias: [e]xit)")
                    print("[n]ew N - builds automata for N")
                    print("[l]oad L - new session of type L")
                    print("[s]tep a b - steps down edge (a,b) steps down shortest path if a and b are omitted")
                    print("[m]ultistep x - steps down shortest path x times")
                    print("[b]ack x - jumps back x steps (default 1)")
                    print("[g]oto state - jumps to given state")
                    print("[i]nitial - jumps to the initial state")
                    print("showall - shows all edges, including edges that never lead to accepts (alias: alledges)")
                    print("[r]esult N - Gets automata information in this session for N but doesn't switch explorer")
                    print("[c]onvert fromBase toBase x - converts x between fromBase and toBase")
                    print("[d]o script - executes python and prints result")

                # Catch fails

                else:
                    print("Unrecognized Command")
                    self.skipDraw = True

            except Exception as e:
                print(e)
                print("Something went wrong")
                self.skipDraw = True

if __name__ == "__main__":
    AutomataExplorer("fibbinary/fibbinary").coreLoop()
