#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

set -x

black --check todoist_github/
flake8 todoist_github/
isort -c -rc todoist_github/
mypy todoist_github/
