import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import RegularLanguageRatioSetAutomataGenerator as RLRSAG

from utilities.utilities import *

base3 = readResults(open("../StartingWithOne/base3startingwith1.txt", "r").read())
base4 = readResults(open("../StartingWithOne/base4startingwith1.txt", "r").read())
base5 = readResults(open("../StartingWithOne/base5startingwith1.txt", "r").read())
base6 = readResults(open("../StartingWithOne/base6startingwith1.txt", "r").read())

print(getColumn(failures(base3), 0)[:20])
print(getColumn(failures(base4), 0)[:20])
print(getColumn(failures(base5), 0)[:20])
print(getColumn(failures(base6), 0)[:20])

print(latexify([["A_{k, 1}", "First elements $n \\in \\N$ not an element of R(A_{k, 1})"], ["A_{3, 1}", getColumn(failures(base3), 0)[:20]], ["A_{4, 1}", getColumn(failures(base4), 0)[:20]], ["A_{5, 1}", getColumn(failures(base5), 0)[:20]], ["A_{6, 1}", getColumn(failures(base6), 0)[:20]]]))

l3 = deleteColumns(largestSolutions(base3), [1])[:7]
l3 = l3 + [["", "", ""]] * (7-len(l3))
l4 = deleteColumns(largestSolutions(base4), [1])[:7]
l5 = deleteColumns(largestSolutions(base5), [1])[:7]
l6 = deleteColumns(largestSolutions(base6), [1])[:7]
print(l3)
print(l4)
print(l5)
print(l6)
#print(latexify([[*l3[i], *l4[i], *l5[i], *l6[i]] for i in range(7)]))
print(latexify([[*l4[i], *l5[i], *l6[i]] for i in range(7)]))


print(gaps(base3))
print(gaps(base4))
print(gaps(base5))
print(gaps(base6))

g3 = [(g[0], g[1][0]) for g in gaps(base3)][:6]
g4 = [(g[0], g[1][0]) for g in gaps(base4)][:6]
g5 = [(g[0], g[1][0]) for g in gaps(base5)][:6]
g6 = [(g[0], g[1][0]) for g in gaps(base6)][:6]

print(latexify([[*g4[i], *g5[i], *g6[i]] for i in range(6)]))

print(latexify([[r[0], r[1][3], r[1][0]] for r in runs(base6)[:40]]))
