#!/bin/bash

# Use: ./MakeEpupBook.sh path/to/main.tex

# Strip file path and extension
filenameWithPath=$1
filename=$(basename -- "$filenameWithPath")
filepath="$(dirname "${filenameWithPath}")"
fileBaseName="${filename%.*}"

#echo $filename
#echo $filepath

# First, copy over everything book to a temp directory
tempDir="tempDir"
rm -rf ./$tempDir
mkdir $tempDir
cp -r $filepath/* ./$tempDir

# Changes \vspace{10pt} to "vspacevspacevspace"
python3 ./ModifyLatexFilesForVSpace.py ./$tempDir/$filename

# Convert to xml
latexml --dest=$fileBaseName.xml ./$tempDir/$filename

# Correct the errors from \adjustwidth and vspace. Everything else besides that and vspace are handled
# properly. For these two, make a special xml class/tag with the following python script
