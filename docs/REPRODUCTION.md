# Reproduction guide

## Scope and safety

Portfolio validation and figure generation are offline, CPU-only tasks. Training, inference, routing export, data
download, and GPU use are not performed by the commands below.

Full experimental reproduction must occur in a separate Tencent/YOLO-Master checkout with a separately obtained
dataset and an output root outside this repository. Do not copy this portfolio over an upstream checkout.

## 1. Validate the public artifact

Use Python 3.11 for the lightweight public workflow:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install matplotlib numpy pillow pyyaml ruff
python scripts/validation/validate_results.py
python scripts/analysis/build_portfolio_figures.py --check
python scripts/validation/validate_public_repository.py
```

The last command requires a clean Git worktree. During an intentional pre-commit review, use `--allow-dirty` and
then rerun without it after committing.

## 2. Rebuild figures and manifests

```bash
python scripts/analysis/build_portfolio_figures.py
python scripts/analysis/build_portfolio_figures.py --check
python scripts/validation/build_manifests.py
python scripts/validation/validate_results.py
```

The figure check regenerates all six PNGs in a temporary directory and compares bytes. Rebuild manifests after any
intentional public-file change, then rerun the repository validator.

## 3. Obtain an upstream checkout separately

For formal experiment reproduction, clone Tencent/YOLO-Master into an explicit external project directory and
checkout the audited Issue #54 revision or a reviewed equivalent. Do not replace the current branch silently, and
do not assume results apply to a later upstream main.

Recorded branch/commit:

```text
issue54-mot-routing-stability
dd490a80840dd70836e9363e14630039c7086a87
```

The public portfolio does not automate this checkout and does not contain the upstream source tree.

## 4. Prepare VisDrone independently

Obtain VisDrone2019-DET from its maintainers and review its terms. Set `${DATASET_ROOT}` locally and adapt
[the public path template](../configs/visdrone_issue54_public.yaml). No dataset path should be committed.

## 5. Review the formal protocol

Read [formal_protocol.yaml](../configs/formal_protocol.yaml) and [Experiment protocol](EXPERIMENT_PROTOCOL.md).
Verify model keys, independent seeds, precision, epochs, batch, image size, fixed validation manifest, and output
isolation before compute.

## 6. Dry-run before execution

The audited upstream branch includes Issue #54 Phase 3 runners with `--dry-run` modes. Begin by printing and
reviewing commands in the separate upstream checkout. Do not add execution flags until data, environment, paths,
and output isolation have been confirmed.

This portfolio deliberately does not repeat a ready-to-run training command: copying a formal command without the
external path and license review would be unsafe. The upstream entry points are documented in
[the contribution record](../contributions/ISSUE_54.md).

## 7. Formal evidence requirements

Every new run must preserve:

- one unique experiment ID, logical seed, and checkpoint SHA256;
- finite final metrics and completed epoch count;
- dataset/version/split identity;
- configuration and manifest hashes;
- fixed-image routing identity for MoT;
- separation of formal, diagnostic, smoke, failed, not-executed, routing-only, and repeated-export evidence.

Do not count image, token, layer, export repeat, or seed-pair rows as independent training seeds.

## 8. Environment notes

The audited fixes include Torch 1.8 autocast fallback, export-safe scatter, legacy-safe reductions, and
cross-platform tests. Reproducing exact numerical results still depends on Python/PyTorch versions, device,
deterministic-kernel availability, dataset preparation, and upstream revision. Record these explicitly.
