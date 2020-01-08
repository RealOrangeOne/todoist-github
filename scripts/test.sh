#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

set -x

black --check todoist-github/
flake8 todoist-github/
isort -c -rc todoist-github/
mypy todoist-github/
