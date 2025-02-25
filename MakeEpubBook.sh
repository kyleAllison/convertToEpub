#!/bin/bash

# Use: ./MakeEpupBook.sh path/to/main.tex
# Then load the book.html in Calibre gui, then convert to epub.
# Using command line ebook-convert seems to ignore extra-css no matter what I try, which
# is why this last step has to be manual

# TODO if I wanted:
# To avoid making the scripts overly complicated, the tex files needs the following:
# Blank lines around the special latex commands adjustwidth and vspace
# The chapters are included by: \input path/chapterName/tex
# I wasn't careful about vspace, so I don't parse the value and instead set it here for everywhere
# All of my desires to not indent after breaks and after epigraphs seem to be overridden
vspaceValue="10mm"

# # Strip file path and extension
filenameWithPath=$1
filename=$(basename -- "$filenameWithPath")
filepath="$(dirname "${filenameWithPath}")"
fileBaseName="${filename%.*}"

# # First, copy over everything book to a temp directory
tempDir="tempDir"
rm -rf ./$tempDir
mkdir $tempDir
cp -r $filepath/* ./$tempDir

# Modify the tex files to remove the latex commands that don't work with latexml
# These are: \vspace, \begin{adjustwidth}
# All it does is changes \vspace{10pt} to "vspacevspacevspace10pt"
python3 ./ModifyLatexFilesForConversion.py ./$tempDir/$filename adjustwidth
exitStatus=$?
if [ "$exitStatus" -ne 0 ]; then
    exit 1
fi
python3 ./ModifyLatexFilesForConversion.py ./$tempDir/$filename vspace
exitStatus=$?
if [ "$exitStatus" -ne 0 ]; then
    exit 1
fi

# Convert to xml
latexml --dest=$fileBaseName.xml ./$tempDir/$filename

# Fix the xml issues from the latex comands
python3 ./FixXMLFile.py $fileBaseName.xml $vspaceValue

# # Convert to html
latexmlpost -dest=$fileBaseName.html modified_$fileBaseName.xml

# Link my custom.css file in book.html after first css link
sed -i '/<link rel="stylesheet" href="LaTeXML.css" type="text\/css">/a <link rel="stylesheet" href="./customClasses.css" type="text/css">' "$fileBaseName.html"

# Make the epub.
#ebook-convert $fileBaseName.html $fileBaseName.epub --language en --no-default-epub-cover --extra-css customClasses.css

# Add in the special adjust width and vspace rules

