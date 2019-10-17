#!/bin/bash

set -e
set -u
set -o pipefail

RELEASE_VERSION="${1:-}"
TAG_NAME="v${RELEASE_VERSION}"

printUsageText() {
	echo "It's optional to specify a release version, if you do, below is the format"
	echo ""
	echo "Usage:"
	echo "    $0 [new release version]"
	echo "  for e.g.:"
	echo "    $0 0.1.2"
	echo ""
	echo "In the absence of the release version supplied via CLI args, we will use the information in the .bumpversion.cfg file"
}

checkReleaseVersion() {
	if [[ -z "${RELEASE_VERSION}" ]]; then
		echo "You haven't supplied any release version, hence we will use the information from the .bumpversion.cfg file."
		printUsageText
	else
		echo "Release version provided: ${RELEASE_VERSION}"
		echo "Tag name to be created: ${TAG_NAME}"
	fi
}

checkIfAnyTagsExistAtAll() {
	EXISTING_TAGS="$(git tag --list || true)"
	echo "~~~ For your information"
	if [[ -z "${EXISTING_TAGS}" ]]; then
		echo "We found no tags on your local repo (which means we have none on your remote repo either)"
	else
		echo "List of tags on local repo (in sync with the remote repo):"
		echo "${EXISTING_TAGS}"
	fi
	echo "~~~~~~~~~~~~~~~~~~~~~~~"
}

getCurrentVersion() {
	VERSION_STRING="$(grep "version" setup.py | tr -d " ," || true)"
	VERSION_STRING="$(echo "${VERSION_STRING}" | tr -d "version='" || true)"
	echo "${VERSION_STRING}"
}

showCurrentVersion() {
	echo "Current version of the library is $(getCurrentVersion)"
}

runBumpVersion() {
	if [[ -z "${RELEASE_VERSION}" ]]; then
		echo ""; echo "Bumping the version of library to the next version"
		bumpversion --verbose --list patch
	else
		echo ""; echo "Bumping the version of library to the new version: ${RELEASE_VERSION}"
		bumpversion --verbose --new-version "${RELEASE_VERSION}" --list patch
	fi
}

showNewVersion() {
	echo ""; echo "~~~ New version of the library is $(getCurrentVersion)"
}

showRecentCommitMessage() {
	echo ""; echo "~~~ Recent commit: $(git log --oneline | head -n 1 || true)"
}

showCreatedTag() {
	echo ""; echo "~~~ Tag created ${CREATED_TAG_NAME}"
}

pushTagToRemoteRepo() {
	echo ""; echo "Pushing ${CREATED_TAG_NAME} tag to remote"
	git push origin "${CREATED_TAG_NAME}"
}

printOptionalInfo() {
	echo ""; echo "(Optional info) You can delete the ${CREATED_TAG_NAME} tag from both your local and remote repos using the below command:"
	echo "./delete-tag.sh ${CREATED_TAG_NAME}"
}

CREATED_TAG_NAME=""
run() {
	runBumpVersion

	showNewVersion

	CREATED_TAG_NAME="v$(getCurrentVersion)"
	
	showCreatedTag

	showRecentCommitMessage

	pushTagToRemoteRepo

	printOptionalInfo

}

checkReleaseVersion
checkIfAnyTagsExistAtAll
showCurrentVersion
run