.DEFAULT_GOAL := help

init:  ## Setup venv using pipenv
	pipenv install --dev
	pipenv requirements > requirements.txt


proto-compile:  ## Compile the proto file, only necessary if you change the .proto
	pipenv run python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. my_service.proto

run-simple-api-core-repro:  ## Run simple_api_core_repro.py to reproduce basic failure
	pipenv run python simple_api_core_repro.py

# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## When you just dont know what to do with your life, look for inspiration here!
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

