# Scripts

- `analysis/build_portfolio_figures.py` validates public table schemas and deterministically builds the banner and
  all five figures.
- `validation/validate_results.py` checks scientific counting rules and numeric integrity.
- `validation/validate_public_repository.py` checks the public tree, links, hashes, images, bilingual facts, and
  prohibited-content policy.

These scripts do not train, infer, export routing, download data, or access a GPU. Reproduction commands in the
documentation are dry-run or validation-oriented by default.
