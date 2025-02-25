import xml.etree.ElementTree as ET
import sys
import re

def AdjustXML(filename):

    with open(filename, 'r') as currentFile:
        buffer = currentFile.readlines()

    # First, clean everything up
    cleanedUpBuffer = []
    for i, line in enumerate(buffer):

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

        cleanedUpBuffer.append(line)

    # With our clean buffer, fix the adjustwidths and vspaces
    finalBuffer = cleanedUpBuffer
    finished = False
    while not finished:
        for i, line in enumerate(cleanedUpBuffer):

            #print(line)

            # If we have beginadjustwidth, modify all para class until endadjustwidth
            if "beginadjustwidthbeginadjustwidthbeginadjustwidth" in line:

                # Delete the current line, previous line, and next line
                del finalBuffer[i + 1]
                del finalBuffer[i]
                del finalBuffer[i - 1]
            
                # Extract the width value
                match = re.search(r'(\d+pt\d+pt)', line)
                widthValue = match.group(0)
                foundBeginAdjustWidthPattern = True

                # Modify the final buffer until the endadjustwidth
                index = i - 1
                foundEndAdjustWidth = False
                while not foundEndAdjustWidth:

                    # Make sure we haven't his end
                    currentLine = finalBuffer[index]
                    nextLine = finalBuffer[index + 1]
                    if "endadjustwidthendadjustwidthendadjustwidth" in nextLine:
                        foundEndAdjustWidth = True
                        continue
                    elif "<para" in currentLine:

                        # If it contains a class, add to it
                        classString = ""
                        match = re.search(r'class="([^"]*)"', currentLine)
                        if "class" in currentLine:
                            classString = match.group(1)
                            lineWithClass = '<para class="ltx_adjustwidth' + str(widthValue)
                            lineWithClass = lineWithClass +  " " + classString + '" '
                            stringToReplace = '<para class="' + classString + '"'
                            finalBuffer[index] = currentLine.replace(stringToReplace, lineWithClass)
                        else:
                            lineWithClass = '<para class="ltx_adjustwidth' + str(widthValue) + '" '
                            stringToReplace = '<para '
                            finalBuffer[index] = currentLine.replace(stringToReplace, lineWithClass)
                    index = index + 1
    
                
                # Reset from beginning, since we changed buffer, to keep things simple
                break

            elif "endadjustwidthendadjustwidthendadjustwidth" in line:

                # Delete the current line, previous line, and next line
                del finalBuffer[i + 1]
                del finalBuffer[i]
                del finalBuffer[i - 1]

                # Reset
                break;

            elif "vspacevspacevspace" in line:

                # Delete the current line, previous line, and next line
                del finalBuffer[i + 1]
                del finalBuffer[i]
                del finalBuffer[i - 1]

                # Modify the next <para after vspace to have an additional vspace class
                # Modify the final buffer until the endadjustwidth
                index = i - 1
                foundNextPara = False
                while not foundNextPara:

                    # Make sure we haven't his end
                    currentLine = finalBuffer[index]
                    if "<para" in currentLine:

                        # If it contains a class, add to it
                        foundNextPara = True
                        classString = ""
                        print("Is class in string: " + currentLine)
                        match = re.search(r'class="([^"]*)"', currentLine)
                        if "class" in currentLine:
                            classString = match.group(1)
                            lineWithClass = '<para class="ltx_vspace' + str(vspaceValue)
                            lineWithClass = lineWithClass +  " " + classString + '" '
                            stringToReplace = '<para class="' + classString + '"'
                            print("\n\n\nReplacing: " + classString)
                            print(stringToReplace)
                            finalBuffer[index] = currentLine.replace(stringToReplace, lineWithClass)
                        else:
                            lineWithClass = '<para class="ltx_vspace' + str(vspaceValue) + '" '
                            stringToReplace = '<para '
                            finalBuffer[index] = currentLine.replace(stringToReplace, lineWithClass)
                    index = index + 1
                
                # Reset
                break;
                
            if i == len(finalBuffer) - 1:
                finished = True
    
    modifiedFile = open("modified_" + filename, "w")
    modifiedFile.writelines(finalBuffer)

if len(sys.argv) != 3:
    print("Incorrect usage. Use: FixXMLFile.py pathToXML.xml vspacevalue")
    sys.exit(1)

filename = sys.argv[1]
vspaceValue = sys.argv[2]

print(str(vspaceValue))

AdjustXML(filename)
