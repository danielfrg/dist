# Daniel's Python Distribution

Do not use, ok maybe, works great but good luck. Only the best data science packages.

Dependencies are in `environment.yml`.

## Dependencies

This needs to run in the conda root environment.

Install other `conda-bundle` deps on that environment:

```
make deps
```

## Build

```
make dist
```

## Install

```
tar -xzf bundle.tar.gz
CONDA_DIR=/opt/conda bash bundle/install
```
