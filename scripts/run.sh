#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

python3 todoist-github/cli.py
