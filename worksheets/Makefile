# TEXINPUTS must resolve catniplab.sty and math_preamble.tex
# from memmingCommons/latex/. Do not commit local copies of those files.
# Verify with: kpsewhich catniplab.sty

DOC = coin_test

all: student key

student: $(DOC).pdf
key: $(DOC)_key.pdf

$(DOC).pdf: $(DOC).tex
	latexmk -pdf -interaction=nonstopmode $(DOC).tex

# The answer key: same source, \showsolutions defined before the document is read.
$(DOC)_key.pdf: $(DOC).tex
	latexmk -pdf -interaction=nonstopmode -jobname=$(DOC)_key \
		-usepretex='\def\showsolutions{}' $(DOC).tex

clean:
	latexmk -c $(DOC).tex
	latexmk -c -jobname=$(DOC)_key $(DOC).tex

.PHONY: all student key clean
