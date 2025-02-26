#!/bin/bash

# Use: ./ExtraStyling.sh book.epub

# Unpack the zip and then modify the stylesheet.css to:
# Change margins, remove extra spaces between pargraphs.
# Repack tar ball into epub

# # Strip file path and extension
filenameWithPath=$1
filename=$(basename -- "$filenameWithPath")
filepath="$(dirname "${filenameWithPath}")"
fileBaseName="${filename%.*}"

pythonScript="PostModifyEpub.py"
bookDir="unzippedBook"
rm -rf $bookDir
mkdir $bookDir
unzip ${filenameWithPath} -d ./$bookDir
cp $pythonScript $bookDir
cd $bookDir

# Python script to modify the stylesheet as desired
python3 $pythonScript ./stylesheet.css

# Rezip
bookName="modifiedBook.epub"
zip -X0 $bookName mimetype
zip -r9 $bookName META-INF OEBPS *.jpg *.xhtml *.ncx *.opf *.css *.html
mv $bookName ../
cd ../
