"""
This file contains a variety of small utility functions for analyzing results from my ratio set related programs.
Generally we assume that each element of our list of lists has the same length.
Most functions base their size estimation by the first element.
Typical rows is "p q a b" maybe with extra data afterward.
"""

import math
import sys

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

"""
Discovers runs of inputs that aren't representable
"""
def gaps(rows):
    print("NOT YET IMPLEMENTED")
    exit(1)

"""
Converts a list of lists to a string that encodes a table in LaTeX.
"""
def latexify(rows):
    output = "\\begin{table}\n    \\centering\n    \\begin{tabular}{" + ("c|" * (len(rows[0])-1)) + "c}\n"
    for row in rows[:-1]:
        output = output + "        " + " & ".join(map(str, row)) + "\\\\\n        \\hline\n"
    output = output + "        " + " & ".join(map(str, row)) + "\n    \\end{tabular}\n    \\caption{CAPTION TODO} %TODO\n    \\label{table:TODO} %TODO\n\\end{table}"
    return output
