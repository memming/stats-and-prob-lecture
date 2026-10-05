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

# Publish the student handout (never the key) as a GitHub release asset.
# First run creates the release; later runs replace the PDF in it.
# Link: https://github.com/memming/stats-and-prob-lecture/releases/download/$(TAG)/$(DOC).pdf
TAG ?= day2-worksheet-2026
release: $(DOC).pdf
	if gh release view $(TAG) >/dev/null 2>&1; then \
		gh release upload $(TAG) $(DOC).pdf --clobber; \
	else \
		gh release create $(TAG) $(DOC).pdf \
			--title "Day 2 worksheet: Is the dealer's coin fair?" \
			--notes "Student handout, paper and pencil. Source: worksheets/$(DOC).tex"; \
	fi

clean:
	latexmk -c $(DOC).tex
	latexmk -c -jobname=$(DOC)_key $(DOC).tex

.PHONY: all student key release clean
