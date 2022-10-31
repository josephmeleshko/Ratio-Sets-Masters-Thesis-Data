from utilities import *

palpal = countRepresentableByLength(readResults(open("../../Palindrome-Ratio-Set-Automata-Generator/data/base3palpal.txt").read()), 3, resultColumn=2)
palapal = countRepresentableByLength(readResults(open("../../Palindrome-Ratio-Set-Automata-Generator/data/base3palapal.txt").read()), 3, resultColumn=2)
apalpal = countRepresentableByLength(readResults(open("../../Palindrome-Ratio-Set-Automata-Generator/data/base3apalpal.txt").read()), 3, resultColumn=2)
apalapal = countRepresentableByLength(readResults(open("../../Palindrome-Ratio-Set-Automata-Generator/data/base3apalapal.txt").read()), 3, resultColumn=2)

print(palpal)
l = []
for i in palpal.keys():
    l.append([i, palpal[i] if i in palpal else 0, palapal[i] if i in palapal else 0])
for i in palpal.keys():
    l.append([i, apalpal[i] if i in apalpal else 0, apalapal[i] if i in apalapal else 0])

print(latexify(l))
