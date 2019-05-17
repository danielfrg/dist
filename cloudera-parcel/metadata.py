import os
import re
import sys
import json
import shutil
from optparse import OptionParser
from subprocess import check_call


CONDA_ENV_SH = """#!/bin/bash

if [ -z "${CDH_PYTHON}" ]; then
  export CDH_PYTHON=${PARCELS_ROOT}/${PARCEL_DIRNAME}/bin/python
fi

if [ -n "${R_HOME}" ]; then
  export R_HOME="${PARCELS_ROOT}/${PARCEL_DIRNAME}/lib"
fi

if [ -n "${RHOME}" ]; then
  export RHOME="${PARCELS_ROOT}/${PARCEL_DIRNAME}/lib/conda-R"
fi

if [ -n "${R_SHARE_DIR}" ]; then
  export R_SHARE_DIR="${PARCELS_ROOT}/${PARCEL_DIRNAME}/lib/R/share"
fi

if [ -n "${R_INCLUDE_DIR}" ]; then
  export R_INCLUDE_DIR="${PARCELS_ROOT}/${PARCEL_DIRNAME}/lib/R/include"
fi
"""


def metadata(name, version, os_version, prefix):
    # $PREFIX/meta
    meta_dir = os.path.join(prefix, "meta")
    if not os.path.exists(meta_dir):
        os.mkdir(meta_dir)
    
    # Write parcel.json
    packages = get_package_list(prefix)
    data = get_parcel_json(name, version, packages, os_version)
    with open(os.path.join(meta_dir, "parcel.json"), "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

    # Write parcel env scripts
    with open(os.path.join(meta_dir, "conda_env.sh"), "w") as f:
        f.write(CONDA_ENV_SH)


def get_package_list(prefix):
    """Get packages from an anaconda installation
    """
    packages = []

    # Get the (set of canonical names) of linked packages in prefix
    meta_dir = os.path.join(prefix, "conda-meta")
    pkg_list = set(fn[:-5] for fn in os.listdir(meta_dir) if fn.endswith(".json"))
    # print(pkgs)
    for dist in sorted(pkg_list):
        name, version, build = dist.rsplit("-", 2)
        packages.append({
            "name": name,
            "version": "%s-%s" % (version, build),
        })
    return packages


def get_parcel_json(name, version, packages, os_version):
    _ = {
        "schema_version": 1,
        "name": name,
        "version": version,
        "provides": [
            "conda",
        ],
        "scripts": {
            "defines": "conda_env.sh",
        },
        "packages": packages,
        "setActiveSymlink": True,
        "extraVersionInfo": {
            # "fullVersion":"%s-%s" % (version, os_version),
            "baseVersion": version,
            "patchCount": "p0",
        },
        "components": [{
            "name": name,
            "version": version,
            "pkg_version": version,
        }],
        "users": {},
        "groups": [],
    }
    return _

if __name__ == "__main__":
    params = OptionParser(
        usage="usage: %prog [options] NAME VERSION OS_VERSION PREFIX",
        description="Create parcel metadata for a conda installation")

    opts, args = params.parse_args()
    if len(args) != 4:
        params.error("Exactly 4 arguments expected")

    name = args[0]
    version = args[1]
    os_version = args[2]
    prefix = args[3]
    
    metadata(name, version, os_version, prefix)
