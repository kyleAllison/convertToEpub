import re
import sys
import os

filename = sys.argv[1]
myFile = open(filename, 'a')

# Remove the spaces between paragraphs, center titles. Indent still doesn't work
linesToAdd = [".ltx_p, .ltx_p1, .ltx_p2, .ltx_p3, .ltx_p4, .ltx_p5 {",
              "    display: block;",
              "    margin: 0;",
              "    padding: 0;",
              "    white-space: normal;",
              "}",
              ".ltx_title1 {",
              "    text-align: center;",
              "}",
              ".ltx_para3 {",
              "    text-indent: 0;",
              "}"
              ]

for line in linesToAdd:
    myFile.write(line + "\n")
