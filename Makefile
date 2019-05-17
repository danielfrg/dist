all: help

clean:
	rm -rf bundle
.PHONY: clean

cleanall: clean
	rm -rf .venv
.PHONY: cleanall

deps:  ## Install dependencies
	pip install requests_download progressbar2
.PHONY: env

dist:  ## Make distribution
	./conda-bundle/conda-bundle -f environment.yml
.PHONY: dist

help:
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'
.PHONY: help
