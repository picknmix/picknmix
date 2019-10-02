#!/bin/bash

set -e
set -u
set -o pipefail

git diff --name-only master                   \
     | perl -ne 'print $1 if m/\.([^.\/]+)$/' \
     | sort -u                                \
       > all-changed-files-extensions.txt

EXCLUDE_EXTENSIONS=(rst md png jpeg jpg bmp gif)

for EXT in "${EXCLUDE_EXTENSIONS[@]}"
do
	awk '!/'"${EXT}"'/' all-changed-files-extensions.txt > \
	     temp && mv temp all-changed-files-extensions.txt
done

REMANINING_LINES=$(cat all-changed-files-extensions.txt | wc -l || true)

CODE_CHANGES_DETECTED="false"
if [[ ${REMANINING_LINES} -ne 0 ]]; then
	CODE_CHANGES_DETECTED="true"
fi

rm -f all-changed-files-extensions.txt all-changed-files-extensions.txt.bak
echo "${CODE_CHANGES_DETECTED}"