#!/bin/bash

function make_doc {
if [ -z ${1+x} ]; then
  echo "no file specified to make_doc"
  return 1
elif [ ! -f src/$1.rst ]; then
   echo "File not found! $1.rst"
else
  echo "Generating HTML and PDF files for ${1} ..."
  cp src/$1.rst .
  rst2html $1.rst $1.html
  rst2latex $1.rst $1.tex
  latex  -output-format=pdf $1.tex
  rm $1.aux
  rm $1.out
  rm $1.log
  rm $1.toc
  rm $1.rst
  scp $1.pdf cupojoe.srn.sandia.gov:
fi
}

make_doc TribitsTutorial_ConvertAProject
make_doc TribitsTutorial_Dependencies
make_doc TribitsTutorial_HelloWorld
make_doc TribitsTutorial_ProjectStructure
