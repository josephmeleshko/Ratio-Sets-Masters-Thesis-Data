"""
This file contains a variety of small utility functions for analyzing results from my ratio set related programs.
Generally we assume that each element of our list of lists has the same length.
Most functions base their size estimation by the first element.
Typical rows is "p q a b" maybe with extra data afterward.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
try:
    import RegularLanguageRatioSetAutomataGenerator as RLRSAG
except:
    pass

import pickle
import math

try:
    import matplotlib.pyplot as plt
except:
    pass
try:
    import networkx as nx
except:
    pass

"""
Takes an input string of data and builds a list of lists.
Can send doSort=False to skip sorting.
Can send nonIntegerColumns=List to not convert columns listed to integers.
"""
def readResults(dataString, doSort=True, nonIntegerColumns=[]):
    rows = []
    lines = dataString.split("\n")
    for line in lines:
        line = line.split()
        if len(line) == 0:
            continue
        convertedLine = []
        for i in range(len(line)):
            if i not in nonIntegerColumns:
                convertedLine.append(int(line[i]))
            else:
                convertedLine.append(line[i])
        rows.append(convertedLine)
    if doSort:
        rows.sort()
    return rows

"""
Builds a new list of lists such that the column numbers given in columns aren't present.
"""
def deleteColumns(rows, columns):
    newRows = []
    for row in rows:
        nextRow = []
        for i in range(len(row)):
            if i not in columns:
                nextRow.append(row[i])
        newRows.append(nextRow)
    return newRows

"""
Goes through the list of lists and returns record breakers by some row, usually b for p/q = a/b.
"""
def largestSolutions(rows, sizeColumn=3):
    largest = -math.inf
    newRows = []
    for row in rows:
        if row[sizeColumn] > largest:
            newRows.append(row)
            largest = row[sizeColumn]
    return newRows

"""
Convert a list of lists to a string to write to file.
"""
def stringify(rows):
    output = ""
    for row in rows:
        output = output + " ".join(map(str, row)) + "\n"
    return output

"""
Code to generate a visual representation of a given automata.
Expects an automaton in dictionary form.
"""
def drawAutomata(states, layout=None):
    G = nx.DiGraph()
    # Add nodes
    G.add_nodes_from(states.keys())
    edges = {}
    for state in states:
        for child in states[state]:
            edges[(state, child[2])] = (child[0], child[1])
    G.add_edges_from(edges.keys())
    plt.figure()
    if layout == "planar":
        pos = nx.planar_layout(G)
    elif layout == "graphviz":
        pos = nx.nx_agraph.graphviz_layout(G)
    elif layout == "spring":
        pos = nx.spring_layout(G)
    elif layout == "random":
        pos = nx.random_layout(G)
    elif layout == "circle":
        pos = nx.circular_layout(G)
    else:
        try:
            pos = nx.planar_layout(G)
        except:
            pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=5000)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, node_size=5000)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
    plt.show()

"""
Discovers runs of inputs that are not representable, i.e. runs of -1.
"""
def gaps(rows, resultColumn=3, onlyLargest=True):
    output = []
    currentRun = 0
    runStart = -1
    largestRun = -1
    for row in rows:
        if row[resultColumn] == -1:
            if currentRun == 0:
                runStart = row
            currentRun += 1
        else:
            if currentRun > 0:
                if currentRun > largestRun or not onlyLargest:
                    output.append((currentRun, runStart))
                    largestRun = currentRun
                currentRun = 0
    if currentRun > 0:
        output.append((currentRun, runStart))
    return output

def runs(rows, resultColumn=3, onlyLargest=False):
    output = []
    currentRun = 0
    runValue = -1
    runStart = -1
    largestRun = -1
    for row in rows:
        if currentRun == 0:
            runValue = row[resultColumn]
        if row[resultColumn] == runValue:
            if currentRun == 0:
                runStart = row
            currentRun += 1
        else:
            if currentRun > largestRun or not onlyLargest:
                output.append((currentRun, runStart))
            currentRun = 1
            runValue = row[resultColumn]
            runStart = row
    output.append((currentRun, runStart))
    return output

"""
Filters out digits without representations.
"""
def failures(rows, resultColumn=2):
    output = []
    for row in rows:
        if row[resultColumn] == -1:
            output.append(row)
    return output

"""
Extract a single column from the list of lists.
"""
def getColumn(rows, column):
    return [row[column] for row in rows]

"""
Counts natural numbers of length i in base k that are accepted
"""
def countRepresentableByLength(rows, base, nColumn=0, resultColumn=3):
    output = dict()
    for row in rows:
        if row[resultColumn] != -1:
            i = math.floor(math.log(row[nColumn], base))
            if i not in output:
                output[i] = 0
            output[i] = output[i] + 1
    return output

"""
Converts a list of lists to a string that encodes a table in LaTeX.
"""
def latexify(rows):
    output = "\\begin{table}\n    \\centering\n    \\begin{tabular}{" + ("c|" * (len(rows[0])-1)) + "c}\n"
    for row in rows[:-1]:
        output = output + "        " + " & ".join(map(str, row)) + "\\\\\n        \\hline\n"
    output = output + "        " + " & ".join(map(str, rows[-1])) + "\n    \\end{tabular}\n    \\caption{CAPTION TODO} %TODO\n    \\label{table:TODO} %TODO\n\\end{table}"
    return output

"""
Converts an automata in a dictionary to a tikzpicture.
"""
def tikzAutomata(automata):
    output = "\\begin{figure}\n    \\centering\n    \\begin{tikzpicture}\n"
    try:
        states = sorted(automata.keys())
    except:
        states = automata.keys()
    for state in states:
        output = output + "        \\node[state] " + "(" + "-".join(map(str, state)) + ")" + " {$" + str(state) + "$};\n"
    output = output + "        \\draw\n"
    for state in states:
        for nextState in automata[state]:
            if nextState[2] == state:
                output = output + "                " + "(" + "-".join(map(str, state)) + ")" + " edge [loop above] node {$" + str((nextState[0], nextState[1])) + "$} " + "(" + "-".join(map(str, nextState[2])) + ")" + "\n"
            elif state in [s[2] for s in automata[nextState[2]]]:
                output = output + "                " + "(" + "-".join(map(str, state)) + ")" + " edge [bend right, above] node {$" + str((nextState[0], nextState[1])) + "$} " + "(" + "-".join(map(str, nextState[2])) + ")" + "\n"
            else:
                output = output + "                " + "(" + "-".join(map(str, state)) + ")" + " edge [above] node {$" + str((nextState[0], nextState[1])) + "$} " + "(" + "-".join(map(str, nextState[2])) + ")" + "\n"
    output = output + ";\n    \\end{tikzpicture}\n    \\caption{Automaton}\n    \\label{fig:Automaton}\n\\end{figure}"
    return output
