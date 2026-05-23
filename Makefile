# Makefile for the Quantum Notes site.
#
# Figures are produced by standalone scripts in code/, each declaring its
# own dependencies inline (PEP 723) and run via `uv run`. Posts embed the
# saved SVGs from figures/; Quarto does NOT execute code at build time,
# so figures and downloadable code can never drift out of sync.
#
# Common targets:
#   make figures   -- regenerate every figure from code/*.py
#   make preview   -- live-reload local preview (quarto preview)
#   make render    -- one-shot static build into _site/
#   make clean     -- remove _site/ and generated figures
#   make zip       -- bundle code/ as a single download (code.zip)

UV      ?= uv
QUARTO  ?= quarto

CODE_DIR    := code
FIGURE_DIR  := figures
SCRIPTS     := $(wildcard $(CODE_DIR)/*.py)

.PHONY: all figures preview render clean zip help

all: figures render

help:
	@echo "Targets:"
	@echo "  figures  - regenerate every figure (uv run code/*.py)"
	@echo "  preview  - quarto preview with live reload"
	@echo "  render   - quarto render into _site/"
	@echo "  clean    - remove _site/ and figures/*.svg"
	@echo "  zip      - create code.zip for readers to download"

figures: $(SCRIPTS)
	@mkdir -p $(FIGURE_DIR)
	@for script in $(SCRIPTS); do \
		echo ">> uv run $$script"; \
		$(UV) run $$script || exit 1; \
	done
	@echo "all figures regenerated in $(FIGURE_DIR)/"

preview:
	$(QUARTO) preview

render:
	$(QUARTO) render

clean:
	rm -rf _site/ .quarto/
	rm -f $(FIGURE_DIR)/*.svg

zip:
	@rm -f code.zip
	zip -r code.zip $(CODE_DIR)
	@echo "wrote code.zip"
