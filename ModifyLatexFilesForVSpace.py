import re
import sys
import os


def modifyVspaceInSubfile(filePath):
    """Reads a LaTeX file and modifies '\vspace{20pt}' to 'vspacevspacevspace'."""
    with open(filePath, 'r') as f:
        content = f.read()

    # Replace all instances of \vspace{20pt} with vspacevspacevspace
    content = re.sub(r'\\vspace\{20pt\}', 'vspacevspacevspace', content)

    # Write the modified content back to the file
    with open(filePath, 'w') as f:
        f.write(content)

def processMainTex(mainTexFile):
    """Reads the main.tex file, finds all input commands, and processes the corresponding subfiles."""
    # Get the directory of the main.tex file
    mainTexDir = os.path.dirname(os.path.abspath(mainTexFile))

    with open(mainTexFile, 'r') as f:
        mainTexContent = f.read()

    # Regex pattern to find all \input commands
    inputPattern = r'\\input\s+([^\s]+)'
    inputFiles = re.findall(inputPattern, mainTexContent)

    # Process each subfile found in the main.tex
    for inputFile in inputFiles:
        inputFilePath = os.path.join(mainTexDir, inputFile)
        
        # Check if the subfile exists before processing
        if os.path.exists(inputFilePath):
            print(f'Processing subfile: {inputFilePath}')
            modifyVspaceInSubfile(inputFilePath)
        else:
            print(f"Warning: Subfile {inputFilePath} not found!")

# Usage example
filename = sys.argv[1]
processMainTex(filename)
