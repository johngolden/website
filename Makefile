# Makefile for the Quantum Notes site.
#
# Figures are produced by standalone scripts in code/. Posts embed the
# saved SVGs from figures/; Quarto does NOT execute code at build time,
# so figures and downloadable code can never drift out of sync.
#
# Common targets:
#   make figures   -- regenerate every figure from code/*.py
#   make preview   -- live-reload local preview (quarto preview)
#   make render    -- one-shot static build into _site/
#   make clean     -- remove _site/ and generated figures
#   make deps      -- pip install -r requirements.txt
#   make zip       -- bundle code/ as a single download (code.zip)

PYTHON ?= python
QUARTO ?= quarto

CODE_DIR    := code
FIGURE_DIR  := figures
SCRIPTS     := $(wildcard $(CODE_DIR)/*.py)

.PHONY: all figures preview render clean deps zip help

all: figures render

help:
	@echo "Targets:"
	@echo "  figures  - regenerate every figure (runs all code/*.py)"
	@echo "  preview  - quarto preview with live reload"
	@echo "  render   - quarto render into _site/"
	@echo "  clean    - remove _site/ and figures/*.svg"
	@echo "  deps     - pip install -r requirements.txt"
	@echo "  zip      - create code.zip for readers to download"

figures: $(SCRIPTS)
	@mkdir -p $(FIGURE_DIR)
	@for script in $(SCRIPTS); do \
		echo ">> $$script"; \
		$(PYTHON) $$script || exit 1; \
	done
	@echo "all figures regenerated in $(FIGURE_DIR)/"

preview:
	$(QUARTO) preview

render:
	$(QUARTO) render

clean:
	rm -rf _site/ .quarto/
	rm -f $(FIGURE_DIR)/*.svg

deps:
	$(PYTHON) -m pip install -r requirements.txt

zip:
	@rm -f code.zip
	zip -r code.zip $(CODE_DIR) requirements.txt
	@echo "wrote code.zip"
