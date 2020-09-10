#!/bin/bash

set -e
set -u
set -o pipefail

checkIfThereAreNoUncommittedChanges() {
    UNCOMMITTED_CHANGES="$(git diff --name-status || true)"

    if [[ ! -z "${UNCOMMITTED_CHANGES}" ]]; then
        echo ""; echo "You have the below uncommitted changes: "
        echo "${UNCOMMITTED_CHANGES}"
        echo "We can't run bumpversion if you have uncommitted changes, please commit the changes and retry."
        exit -1
    fi
}

checkReleaseVersion() {
	if [[ -z "${RELEASE_VERSION}" ]]; then
		echo "No release version provided, using version from .bumpversion.cfg file. See docs for usage text."
	else
		echo "Release version provided: ${RELEASE_VERSION}"
		echo "Tag name to be created: ${TAG_NAME}"
	fi
}

checkIfAnyTagsExistAtAll() {
	EXISTING_TAGS="$(git tag --list || true)"
	if [[ -z "${EXISTING_TAGS}" ]]; then
		echo "We found no tags on your local repo (in sync with the remote repo)"
	else
		echo "List of tags on local repo (in sync with the remote repo):"
		echo "${EXISTING_TAGS}"
	fi
}

getCurrentVersion() {
	VERSION_STRING="$(grep "version" setup.py | tr -d " ," || true)"
	VERSION_STRING="$(echo "${VERSION_STRING}" | tr -d "version='" || true)"
	echo "${VERSION_STRING}"
}

showCurrentVersion() {
	echo""; echo "~~~ Current version of the library is $(getCurrentVersion)"
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

postRunBumpVersion() {
    exitCode=$1

    if [[ ${exitCode} -ne 0 ]]; then
       echo "Error occurred while running bumpversion, aborting..."
       displayBumpversionRunOutput
       exit ${exitCode}
	fi

	displayBumpversionRunOutput
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
	echo ""; echo "(Optional) You can delete the ${CREATED_TAG_NAME} tag from both your local and remote repos using the below command:"
	echo "./delete-tag.sh ${CREATED_TAG_NAME}"
}

displayBumpversionRunOutput() {
	### TravisCI (like other CI services) has a default environment variable called CI
	### indicates we are running on a CI service and not local machine
	### See https://docs.travis-ci.com/user/environment-variables/#default-environment-variables
    if [[ "${CI:-}" = "true" ]]; then
       cat "${BUMPVERSION_VERBOSE_OUTPUT_FILE}"
    else
       echo ""; echo "For brevity, the verbose output from bumpversion can be found at ${BUMPVERSION_VERBOSE_OUTPUT_FILE}"
    fi
}

run() {
    exitCode=0
    runBumpVersion                                \
	      &> "${BUMPVERSION_VERBOSE_OUTPUT_FILE}" \
	      || exitCode=$? && true

    postRunBumpVersion "${exitCode}"

	showNewVersion

	CREATED_TAG_NAME="v$(getCurrentVersion)"
	
	showCreatedTag

	showRecentCommitMessage

	pushTagToRemoteRepo

	printOptionalInfo
}

RELEASE_VERSION="${1:-}"
TAG_NAME="v${RELEASE_VERSION}"
CREATED_TAG_NAME=""
BUMPVERSION_VERBOSE_OUTPUT_FILE=".bumpversion-verbose-output.txt"

rm -fr "${BUMPVERSION_VERBOSE_OUTPUT_FILE}"
checkIfThereAreNoUncommittedChanges
checkReleaseVersion
checkIfAnyTagsExistAtAll
showCurrentVersion
run
