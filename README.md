# Daniel's Python Distribution

Do not use, ok maybe, works great but good luck. Only the best data science packages.

Dependencies are in `environment.yml`.

## Install

```
tar -xzf bundle.tar.gz
cd bundle
CONDA_DIR=/opt/conda ./install
```

## Building

### Dependencies

This needs to run in the conda root environment.

Install other `conda-bundle` deps on that environment:

```
make deps
```

### Build

```
make dist
```

## TODO

Cloudera Parcel and Amabari Mpack need to be updated to the new structure
