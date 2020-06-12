.DEFAULT_GOAL := help

.EXPORT_ALL_VARIABLES:

.PHONY: test-local

all: test-local test-remote

test-local: ## Run local test cases
	tests/local_test.sh 

test-remote: ## Run CI/CD test cases
	tests/remote_test.sh

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'