#!/bin/bash -e
#
# Append a line to one or more files:
#
#   append_line_to_files.sh  <line-to-append> <file0> <file1> ...

LINE_TO_APPEND=$1 ; shift

for file in $@ ; do
  echo "Appending '$LINE_TO_APPEND' to file '${file}'"
  echo "$LINE_TO_APPEND" >> $file
done
