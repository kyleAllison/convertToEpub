import re
import sys
import os

# Modify the latex commands that don't work with latexml
# for later modification of the xml, html, and css files
def ModifySubfile(filePath, commandName):

    with open(filePath, 'r') as currentFile:
        content = currentFile.read()

    # Depending on the command name, modify the files and capture the pt value
    # The r in front makes it raw string literals, to simplify the backslashes and {}
    if commandName == "vspace":
        content = re.sub(r'\\(vspace)\{(\d+[a-zA-Z]+)\}', r'\1\1\1\2', content)
    elif commandName == "adjustwidth":
        content = re.sub(r'\\begin\{(adjustwidth)\}\{(\d+[a-zA-Z]+)\}\{(\d+[a-zA-Z]+)\}',
                         r'begin\1begin\1begin\1\2\3', content)
        content = re.sub(r'\\end\{(adjustwidth)\}', r'end\1end\1end\1', content)
        
    with open(filePath, 'w') as currentFile:
        currentFile.write(content)

# Get the sub chapters
def ProcessMainTex(mainTexFile, commandName):

    mainTexDir = os.path.dirname(os.path.abspath(mainTexFile))
    with open(mainTexFile, 'r') as currentChapter:
        mainTexContent = currentChapter.read()

    # Regex pattern to find all \input commands. Not generic at all, but works for me
    inputPattern = r'\\input\s+([^\s]+)'
    inputFiles = re.findall(inputPattern, mainTexContent)

    # Process each subfile found in the main.tex
    for inputFile in inputFiles:
        inputFilePath = os.path.join(mainTexDir, inputFile)
        
        if os.path.exists(inputFilePath):
            print(f'Processing subfile: {inputFilePath}')
            ModifySubfile(inputFilePath, commandName)
        else:
            print(f"Warning: Subfile {inputFilePath} not found!")

if len(sys.argv) != 3:
    print("Incorrect usage. Use: ModifyLatexFilesForConversion.py pathToBook.tex commandName")
    sys.exit(1)

filename = sys.argv[1]
commandName = sys.argv[2]
ProcessMainTex(filename, commandName)
