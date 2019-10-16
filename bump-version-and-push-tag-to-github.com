#!/bin/bash

set -e
set -u
set -o pipefail

echo "Bumping the version of package to next version"
bumpversion --list patch setup.py

echo "Tag created $(git tag --list | head -n 1)"

echo "Pushing created tag to remote"
git push --tags