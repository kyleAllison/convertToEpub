import xml.etree.ElementTree as ET
import sys
import re

def AdjustXML(filename):

    with open(filename, 'r') as currentFile:
        lines = currentFile.readlines()

    modifiedFile = open("modified_" + filename, "w")
        
    # Because python for loops are annoying. When we encounter one of the patterns,
    # Have to keep track of the surrounding lines
    deleteNextLine = False
    deleteCurrentLine = False
    modifyLine = False
    previousLine = ""
    widthValue = -1
        
    # Parse through the lines to find the ones to modify.
    # There are three cases: beginadjustwidth, endadjustwidth, and vspace.
    for i, line in enumerate(lines):

        print("\nCurrent line: " + line)

        #Delete single line xml comments
        line = re.sub(r'<!--.*?-->', '', line)

        # Delete multi-line comments, which always are:
        # <!-- %, %, or % -->
        # Have to be careful about the order we do this
        # Delete the first line of multi-line comments
        line = re.sub(r'<!--.*', '', line)
        # Delete the end line of multi-line comments
        line = re.sub(r'%.*?-->', '', line)
        # Delete the middle lines. Can start with any number of white spaces
        line = re.sub(r"^\s*%.*\n?", '', line)

        # Lastly, skip empty lines (empty of only white spaces)
        if bool(re.match(r'^\s*$', line)):
            continue
                
        if deleteCurrentLine:
            deleteCurrentLine = False
            previousLine = line
            continue
        if deleteNextLine:
            deleteNextLine = False
            previousLine = line
            continue

        print("After skip lines. Current line: " + line)
        
        
        # For adjust width, delete current line, previous one, and next one. Then modify
        # the nextnext line to add a new xml class to the tag
        # For vspace...
        foundBeginAdjustWidthPattern = False
        foundEndAdjustWidthPattern = False
        foundVSpacePattern = False
        
        # Handle beginadjustwidth
        if "beginadjustwidthbeginadjustwidthbeginadjustwidth" in line:
            
            # Extract the width value
            match = re.search(r'(\d+pt\d+pt)', line)
            widthValue = match.group(0)
            foundBeginAdjustWidthPattern = True
            print("\nFound: " + str(widthValue))

        elif "endadjustwidthendadjustwidthendadjustwidth" in line:
            # No width value
            foundEndAdjustWidthPattern = True
            widthValue = -1
            print("\nFound end adjust withd")

        # When we have beginadjustwidth, don't write the previous line, the current line, or the
        # the next line. After skipping to the nextnextline, modify it to add an xml class
        if foundBeginAdjustWidthPattern:
            deleteNextLine = True
            deleteCurrentLine = True
            modifyLine = True
            previousLine = line
            continue

        # If we found the endadjustwidth, skip the lines and don't modify anything
        if foundEndAdjustWidthPattern:
            deleteNextLine = True
            deleteCurrentLine = True
            modifyLine = False
            previousLine = line
            continue

        # Modify the line we're writing. Make sure to modify the correct line
        if modifyLine and '<para xml:id="Ch' in previousLine:
            print("\nModifying the adjustwidth")
            lineWithClass = '<para class="ltx_adjustwidth' + str(widthValue) + '" xml:id='
            previousLine = previousLine.replace('<para xml:id=', lineWithClass)
            modifyLine = False

            print("New line: " + previousLine)
            print("line with class: " + lineWithClass)
                    
                    
        # We have to stay one line behind
        print("Writing line: " + previousLine)
        modifiedFile.write(previousLine)
        previousLine = line

    # Don't forget the last line!
    modifiedFile.write(previousLine)

if len(sys.argv) != 2:
    print("Incorrect usage. Use: FixXMLFile.py pathToXML.xml")
    sys.exit(1)

filename = sys.argv[1]
AdjustXML(filename)
