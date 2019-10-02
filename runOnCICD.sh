#!/bin/bash

set -e
set -u
set -o pipefail

if [[ "$(codeChangesAreMade.sh)" = "false" ]]; then
   echo "We have not made code related changes in this PR/branch, hence exiting gracefully now. No TravisCI build will be triggered for this PR/branch."
   exit 0
fi

echo "Running tox..."
tox

echo "Running coverage..."
pip install -r requirements-coverage.txt

coverage run --source picknmix -m pytest
coverage report -m
coverage html