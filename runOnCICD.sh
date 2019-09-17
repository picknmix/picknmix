#!/bin/bash

set -e
set -u
set -o pipefail

echo "Running tox..."
tox

echo "Running coverage..."
pip install -r requirements-coverage.txt

coverage run --source picknmix -m pytest
coverage report -m
coverage html