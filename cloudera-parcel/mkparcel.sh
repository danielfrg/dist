#!/bin/bash

[ -z "$NAME" ] && NAME=HYPERCONDA;
[ -z "$VERSION" ] && VERSION=1.0.0;
[ -z "$WORKDIR" ] && WORKDIR=./tmp;
[ -z "$OS_VERSION" ] && OS_VERSION=el6;
[ -z "$OUTPUTDIR" ] && OUTPUTDIR=./output;

PREFIX=$WORKDIR/$NAME-$VERSION

echo "Writing metadata ..."
python metadata.py $NAME $VERSION $OS_VERSION $PREFIX

echo "Writing parcel ..."
mkdir -p $OUTPUTDIR
cd $WORKDIR && tar czf ../$OUTPUTDIR/$NAME-$VERSION-$OS_VERSION.parcel $NAME-$VERSION
