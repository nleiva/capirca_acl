TAG?=0.1.3
.DEFAULT_GOAL := help

.EXPORT_ALL_VARIABLES:

.PHONY: test-local

all: test-local test-remote

test-local: ## Run local test cases
	tests/local_test.sh 

test-remote: ## Run CI/CD test cases
	tests/remote_test.sh

build: ## Build and upload to Galaxy. Make sure you TAG correctly
	sed -i "s/version:.*/version: ${TAG}/" galaxy.yml
	sed -i "s/VERSION=.*/VERSION=${TAG}/" tests/*.sh
	sed -i "s/'metadata_version':.*/'metadata_version': '${TAG}',/" plugins/modules/translate.py
	git tag v${TAG}
	git push origin v${TAG}
	ansible-galaxy collection build
	ansible-galaxy collection publish ./nleiva-capirca_acl-${TAG}.tar.gz

example: ## Run example
	tests/local_example.sh

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'