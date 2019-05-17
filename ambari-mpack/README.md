Run only in Linux

Most likely you want to run this on the docker image from the root of this repo

## Building

Edit the `construct.yaml` file to include the packages you want in the parcel.

```
make

# its the same as
make installer
make mpack
```

## Install

Requires Ambari 2.4 and newer that support the installation of management packs using the `ambari-server install-mpack` command.

Move the `tar.gz` to the Ambari server node, for example using scp:

```
$ scp -i ~/.ssh/keypair.pem hyperconda-mpack-1.0.0.0.tar.gz centos@ambari-server:.
```

Install the Anaconda management pack using:

```
$ ambari-server install-mpack --mpack=anaconda-mpack-1.0.0.0.tar.gz

# Restart amabari-server
$ ambari-server restart
```
