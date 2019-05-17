NAME := HYPERCONDA
VERSION := 1.0.0
OS_VERSION := el6
WORKDIR := ./tmp
OUTPUTDIR := ./output

export NAME VERSION OS_VERSION WORKDIR OUTPUTDIR

all: env parcel manifest

setup:
	conda install -y openjdk maven; git clone https://github.com/cloudera/cm_ext.git ; cd cm_ext; mvn install
.PHONY: setup

env:
	bash mkenv.sh
.PHONY: env

parcel:
	bash mkparcel.sh
.PHONY: parcel

manifest:
	python manifest.py $(NAME) $(VERSION) $(OS_VERSION) $(OUTPUTDIR)
.PHONY: manifest

validate:
	java -jar cm_ext/validator/target/validator.jar -f output/*.parcel
.PHONY: validate

clean:
	rm -rf output tmp
.PHONY: clean

cleanall:
	rm -rf cm_ext output tmp
.PHONY: cleanall
