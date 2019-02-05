NAME = daniel-dist

git_rev = $(shell git rev-parse --short HEAD)
git_tag = $(subst v,,$(shell git describe --tags --abbrev=0))
VERSION ?= $(git_tag)

TMP_DIR = ./tmp
DIST_DIR = $(TMP)/$(NAME)
ENV_DIR = $(TMP_DIR)/condaenv
OUTPUT = $(TMP_DIR)/$(NAME)-$(VERSION).tar.gz

all: help

build: env deps fixes pack ## Build all

env: ## Create the environemnt
	conda create -y -p $(ENV_DIR) -c conda-forge python=3.6 notebook jupyterlab

deps: ## Install dependencies
	$(ENV_DIR)/bin/pip install -r requirements.txt

fixes: ## Fix shit
	$(ENV_DIR)/bin/pip uninstall -y wrapt
	conda install -y -p $(ENV_DIR) -c conda-forge wrapt=1.11.1

pack: ##
	conda pack -p $(ENV_DIR) -o $(OUTPUT) --arcroot $(NAME)

clean: ##
	rm -rf $(ENV_DIR) $(OUTPUT) $(DIST_DIR)

help:
	@grep -E '^[a-zA-Z_-]+:.*?##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"; OFS="\t\t"}; {printf "\033[36m%-30s\033[0m %s\n", $$1, ($$2==""?"":$$2)}'
