# Public configurations

These YAML files are path-parameterized protocol records. They do not bundle a dataset, launch training, or replace
the upstream YOLO-Master model YAML files.

- `formal_protocol.yaml` records the audited nine-run architecture protocol and routing scope.
- `visdrone_issue54_public.yaml` provides a placeholder-only dataset layout.

Resolve `${DATASET_ROOT}` and use a separate, explicit YOLO-Master checkout. Review every generated command before
starting compute. This portfolio contains no automatic training launcher.

