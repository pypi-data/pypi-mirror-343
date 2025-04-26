# Copyright (c) 2023-2024 Datalayer, Inc.
#
# BSD 3-Clause License

SHELL=/bin/bash

.DEFAULT_GOAL := default

.PHONY: clean build

default: all ## Default target is all.

help: ## display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: clean dev ## Clean Install and Build

install:
	pip install .

dev:
	pip install ".[test,lint,typing]"

build:
	pip install build
	python -m build .

clean: ## clean
	git clean -fdx

jupyterlab: ## jupyterlab
	jupyter lab \
		--port 8888 \
		--ServerApp.root_dir ./dev/content \
		--IdentityProvider.token=

server: ## server
	@exec echo
	@exec echo open http://localhost:4400/api/ai-agents/v1/ping
	@exec echo
	python -m uvicorn jupyter_ai_agents.server.main:main --reload --port 4400

prompt:
	jupyter-ai-agents prompt \
		--url http://localhost:8888 \
		--token MY_TOKEN \
		--model-provider azure-openai \
		--model-name gpt-4o-mini \
		--path test.ipynb \
		--input "Create a matplotlib example"

explain-error:
	jupyter-ai-agents explain-error \
		--url http://localhost:8888 \
		--token MY_TOKEN \
		--model-provider azure-openai \
		--model-name gpt-4o-mini \
		--path test.ipynb

publish-pypi: # publish the pypi package
	git clean -fdx && \
		python -m build
	@exec echo
	@exec echo twine upload ./dist/*-py3-none-any.whl
	@exec echo
	@exec echo https://pypi.org/project/jupyter-ai-agents/#history
