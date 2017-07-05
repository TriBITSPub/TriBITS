#!/bin/bash

echo "Generating HTML and PDF files ..."

latex  -output-format=pdf ../TribitsTutorialHelloWorld_0.tex
latex  -output-format=pdf ../TribitsTutorialHelloWorld_1.tex
