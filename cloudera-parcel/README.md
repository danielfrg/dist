Run only in Linux

Most likely you want to run this on the docker image from the root of this repo

## Before creating

Setup the validation tools:

```
make setup
```

## Building

Edit the `construct.yaml` file to include the packages you want in the parcel.

```
make

# same as:
make env
make parcel
make manifest
```

## Installation

The easiest is to move the parcel to the cloudera manager server under the local parcel repository (default: `/opt/cloudera/parcel-repo`).
[Offical docs](https://www.cloudera.com/documentation/enterprise/latest/topics/cm_ig_create_local_parcel_repo.html#concept_cdc_kbk_mz)

## Notes

Based on :

1. http://quasiben.github.io/blog/2016/4/15/conda-spark
2. https://github.com/cloudera/cm_ext/wiki
3. https://github.com/chezou/cloudera-parcel
