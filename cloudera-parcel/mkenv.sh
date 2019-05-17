#!/bin/bash

[ -z "$NAME" ] && NAME=HYPERCONDA;
[ -z "$VERSION" ] && VERSION=1.0.0;
[ -z "$WORKDIR" ] && WORKDIR=./tmp;
PREFIX=$WORKDIR/$NAME-$VERSION

echo $PREFIX

echo "Creating environment ..."
conda create -y -p $PREFIX --copy -c http://repo.continuum.io/pkgs/free -c http://conda.anaconda.org/conda-forge -c http://conda.anaconda.org/danielfrg --file requirements.txt

echo "Patching environment ..."
python patch.py $PREFIX
