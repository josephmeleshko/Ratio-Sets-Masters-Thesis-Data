import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import RegularLanguageRatioSetAutomataGenerator as RLRSAG

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

def naturalDelta(q, sigma):
    if q == 0 and sigma == 0:
        return 0
    elif q == 0:
        return 1
    return 1

def runFibbinary(n):
    return RLRSAG.getSolution(n, 1, 2, fibDelta, fibDelta, fibAccept, fibAccept)

if __name__ == "__main__":
    if False: #R(FIB, FIB)
        l = 16
        RLRSAG.bulkInteger(1, 2**l, 2, fibDelta, fibDelta, fibAccept, fibAccept)
    if True: #R(FIB, N)
        l = 16
        RLRSAG.bulkInteger(1, 2**l, 2, fibDelta, naturalDelta, fibAccept, fibAccept)
