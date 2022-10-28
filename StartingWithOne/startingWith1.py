import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import RegularLanguageRatioSetAutomataGenerator as RLRSAG

def startingWith1Delta(q, sigma):
    if q == 0:
        if sigma == 1:
            return 1
        if sigma == 0:
            return 0
        return None
    return 1

def startingWith1Accept(q):
    return not q == 0

def runStartingWith1(n, base):
    return RLRSAG.getSolution(n, 1, base, startingWith1Delta, startingWith1Delta, startingWith1Accept, startingWith1Accept)

if __name__ == "__main__":
    if False:
        import utilities.utilities as U
        print(U.tikzAutomata(RLRSAG.generateSimpleAutomata(5, 1, 3, startingWith1Delta, startingWith1Delta, startingWith1Accept, startingWith1Accept)))
        U.drawAutomata(RLRSAG.generateSimpleAutomata(5, 1, 3, startingWith1Delta, startingWith1Delta, startingWith1Accept, startingWith1Accept))
        U.drawAutomata(RLRSAG.generateAutomata(5, 1, 3, startingWith1Delta, startingWith1Delta))
    if True:
        base = 6
        digits = 6
        RLRSAG.bulkInteger(1, base**digits, base, startingWith1Delta, startingWith1Delta, startingWith1Accept, startingWith1Accept)
