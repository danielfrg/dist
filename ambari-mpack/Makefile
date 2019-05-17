PWD := $(shell pwd)

all: installer mpack

installer:
	constructor .
.PHONY: installer

mpack:
	python build.py *.sh
.PHONY: parcel

clean:
	rm -rf output tmp *.sh
.PHONY: clean

cleanall: clean
.PHONY: cleanall
