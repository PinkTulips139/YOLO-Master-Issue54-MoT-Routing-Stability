# Checkpoint publication policy

- Publish only checkpoint metadata, final metrics, and SHA256 values.
- Do not publish `best.pt`, `last.pt`, recovery checkpoints, or intermediate weights.
- Do not release weights before upstream, model, and dataset-license review is complete.
- A matching hash demonstrates file identity; it does not establish authorship, license, or redistribution rights.
- Every public checkpoint field is therefore `false` with reason `metadata-only; checkpoint binary not included`.

