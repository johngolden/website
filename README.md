# Quantum Notes

Source for [johngolden.github.io/website](https://johngolden.github.io/website) —
a Quarto blog of pedagogical write-ups on quantum computing.

## How the site is organized

```
.
├── _quarto.yml         # site config, theme, bibliography wiring
├── custom.scss         # cosmetic overrides on the cosmo/darkly themes
├── index.qmd           # blog listing (reverse-chronological)
├── about.qmd           # about page
├── references.bib      # single global BibTeX file
├── posts/
│   └── bloch-sphere/
│       └── index.qmd   # one post per directory
├── code/               # standalone scripts, deps declared inline (PEP 723)
│   └── bloch_sphere.py
├── figures/            # SVGs written by code/*.py, embedded by posts
├── Makefile            # `make figures`, `make preview`, etc.
└── .github/workflows/publish.yml
```

### The figure / code contract

- Every figure on the site is produced by a script in `code/`.
- Each script declares its own dependencies inline ([PEP 723](https://peps.python.org/pep-0723/))
  and is run with `uv run`, which transparently sets up the right
  environment on the fly.
- Scripts write SVGs into `figures/`.
- Posts embed those saved files; **Quarto does not execute code at build
  time** (`execute.enabled: false`).
- `make figures` runs every script, so a reader who downloads the code
  and runs it gets the same image they see in the post.

This keeps posts reproducible without coupling page rendering to a Python
environment, and it means the snippets shown in prose are purely for
reading.

## Local development

Install once:

```sh
brew install quarto uv               # or: https://quarto.org/docs/get-started/
                                     # and: https://docs.astral.sh/uv/
```

That's it — there is no `requirements.txt` and no virtualenv to manage.
`uv run code/<script>.py` reads the script's inline `# /// script` block
and installs exactly what that script needs in an isolated, cached
environment.

Preview with live reload:

```sh
make preview
```

Other useful targets:

```sh
make figures   # regenerate every figure in figures/ from code/*.py
make render    # one-shot static build into _site/
make zip       # bundle code/ as code.zip for readers to download
make clean     # remove _site/ and generated SVGs
```

## Authoring conventions

- Posts are `.qmd` Markdown. Math uses standard LaTeX: `$inline$` and
  `$$display$$`. Tag display equations with `{#eq-name}` and reference
  them with `@eq-name`. Figures use `{#fig-name}` / `@fig-name`.
- Use standard Markdown links and images (`[text](path)`, `![](path)`)
  rather than Obsidian wikilinks — the source is Obsidian-friendly but
  the build is plain Quarto.
- Citations live in a single `references.bib`. Cite with `@bibkey`.
- New figure scripts go in `code/` with a PEP 723 header listing their
  deps, e.g.:

  ```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = ["numpy>=1.26", "matplotlib>=3.8", "qiskit>=1.0"]
  # ///
  ```

## Deployment

Push to `main`. The workflow in `.github/workflows/publish.yml`:

1. Installs `uv` and Quarto.
2. Runs `make figures`, which `uv run`s each script (deps resolved from
   each script's inline metadata, cached between CI runs).
3. Bundles `code/` into `code.zip` for the download link.
4. Renders the site and deploys to GitHub Pages.

**Manual one-time setup in the GitHub UI:** in *Settings → Pages*, set
*Source* to *GitHub Actions*.
