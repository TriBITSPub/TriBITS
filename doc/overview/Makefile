##---------------------------------------------------------------------------##
## MAKEFILE
##---------------------------------------------------------------------------##

PSTEX  := latex
TEX    := pdflatex
BIB    := bibtex
DVI    := dvips
PDF    := ps2pdf13
SED    := sed
PSBOOK := psbook

XFIG := $(wildcard *fig)
PDFFIG := $(patsubst %.fig, %.pdf, $(XFIG))

##---------------------------------------------------------------------------##

.PHONY: clean realclean all denovo

BASE_NAME = TribitsOverview
EXTRA_FILES = \
  Makefile \
  references.bib \
  ../examples/RawHelloWorld/hello_world/CMakeLists.txt \
  ../examples/TribitsHelloWorld/hello_world/CMakeLists.txt

all: $(BASE_NAME).pdf

$(BASE_NAME).pdf: $(BASE_NAME).tex $(PDFFIG) $(EXTRA_FILES) 
	$(TEX) $(BASE_NAME)
	$(BIB) $(BASE_NAME)
	$(TEX) $(BASE_NAME)
	$(TEX) $(BASE_NAME)

clean:
	-rm -f *~
	-rm -f *.log
	-rm -f *.aux
	-rm -f *.dvi
	-rm -f *.rel
	-rm -f *.bbl
	-rm -f *.blg
	-rm -f *.out
	-rm -f *.toc *.lof *.lot
	-rm -f *.bak
	-rm -f TAGS

realclean: clean
	-rm -f $(BASE_NAME).pdf

##---------------------------------------------------------------------------##
## end of Makefile
##---------------------------------------------------------------------------##
