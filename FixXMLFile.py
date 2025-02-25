import sys

filename = sys.argv[1]

file = open(filename, "r")

nLinesToSkip = 3

for i, line in enumerate(file):

    strippedLine = line.strip()

    # For handling the adjustwidth lines. Skip the next three always, and then modify the
    # next paragraph tag to include a new class
    if "ERROR" in line:
        i = i + nLinesToSkip
        for j in range(nLinesToSkip):
            next(file, None)
        continue

    
    
    # IF the line has "<ERROR class="undefined">{adjustwidth}", then
    # skip it, and next three lines
    print("line: " + line)

