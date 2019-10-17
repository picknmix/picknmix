#!/bin/bash

set -e
set -u
set -o pipefail

EXISTING_TAGS="$(git tag --list || true)"
echo "~~~ For your information"
if [[ -z "${EXISTING_TAGS}" ]]; then
	echo "We found no tags on your local repo (which means we have none on your remote repo either)"
else
	echo "List of tags on local repo (in sync with the remote repo):"
	echo ${EXISTING_TAGS}
fi

echo "Current version of the library is $(grep "version" setup.py | tr -d " ," || true)"

read -p "Do you want to bump the version of your library to the next version ([Y|y]es/[N|n]o)? " answer
answer="$(echo "${answer}" | awk '{print tolower($0)}')"
if [[ "${answer}" = "y" ]] || [[ "${answer}" = "yes" ]]; then
	echo ""; echo "Bumping the version of library to next version"
	bumpversion --verbose --list patch setup.py
   
	echo ""; echo "New version of the library is $(grep "version" setup.py | tr -d " ," || true)"

	CREATED_TAG_NAME="$(git tag --list | head -n 1)"
	echo ""; echo "Tag created ${CREATED_TAG_NAME}"

	echo ""; echo "Recent commit: $(git log --oneline | head -n 1 || true)"

	echo ""; echo "Pushing ${CREATED_TAG_NAME} tag to remote"
	git push origin ${CREATED_TAG_NAME}	

	echo ""; echo "You can delete the ${CREATED_TAG_NAME} tag from both your local and remote repos using the below command:"
	echo "./delete-tag.sh ${CREATED_TAG_NAME}"
else
	echo ""; echo "You said 'no', and hence NOT bumping version of library (version stays unchanged)."
fi