# Artifact publication policy

## Public

Compact formal CSV tables, deterministic PNG figures, written reports, checksums, source manifests, parameterized
configs, validation/analysis scripts, exact commit patches, and metadata-only checkpoint records.

## Private archive

The formal raw cross-seed routing JSON and downloaded provenance bundle are copied to an isolated private archive.
Public records use `${ISSUE54_PRIVATE_ARCHIVE}` and `${FORMAL_ROOT}` placeholders rather than machine paths.

## Excluded

Checkpoints, datasets, raw images, training logs, TensorBoard, caches, archives, process state, AutoDL details,
credentials, private URLs, and machine-specific absolute paths.

Raw evidence is never deleted or moved from the existing `Issue54-LocalArchive`; the new private archive is
copy-only. The public repository contains no large raw JSON.

