#!/bin/bash

set -e
set -u
set -o pipefail

TAG_NAME=${1:-}

deleteTag() {
	TARGET_IN_WORDS=$1
	TARGET_AS_COMMAND=$2
	read -p "Do you want to delete ${TAG_NAME} from ${TARGET_IN_WORDS} ([Y|y]es/[N|n]o)? " answer
	answer="$(echo "${answer}" | awk '{print tolower($0)}')"
	if [[ "${answer}" = "y" ]] || [[ "${answer}" = "yes" ]]; then
		echo "Deleting tag ${TAG_NAME} from ${TARGET_IN_WORDS}"
		eval ${TARGET_AS_COMMAND}
	else
		echo "You said 'no', and hence not deleting ${TAG_NAME} from ${TARGET_IN_WORDS}"
	fi
}

fetchTags() {
	echo "Fetching all tags from remote repo..."
	git fetch --tags
}

printUsageText() {
	echo "Please specify an existing tag to delete as a CLI arg (see list above, if any)"
	echo ""
	echo "Usage:"
	echo "    $0 [tag name]"
	echo "  for e.g.:"
	echo "    $0 v0.1.2"
	echo ""
}

EXISTING_TAGS=""
checkIfAnyTagsExistAtAll() {
	EXISTING_TAGS="$(git tag --list || true)"
	if [[ -z "${EXISTING_TAGS}" ]]; then
		echo "We found no tags on your local repo (which means we have none on your remote repo either)"
		exit 0
	else
		echo "List of tags on local repo (in sync with the remote repo):"
		echo ${EXISTING_TAGS}
		echo ""
	fi	
}

exitIfTagNameDoesNotExist() {
	DOES_THE_TAG_NAME_EXIST=$(echo "${EXISTING_TAGS}" | grep "${TAG_NAME}" || true)

	if [[ -z "${DOES_THE_TAG_NAME_EXIST}" ]]; then
		echo "${TAG_NAME} you are trying to delete, does not exist on your local or remote repo."
		echo "Please check list of existing tags above and use one of them."
		exit -1
	fi
}

printUsageAndExistIfNoTagNameIsSpecified() {
	if [[ -z "${TAG_NAME}" ]]; then
		printUsageText
		exit -1
	fi
}

checkIfRecentCommitIfFromBumpversion() {
	RELEASE_VERSION="$(echo "${TAG_NAME}" | tr -d "v" || true)"
	RECENT_COMMIT_MESSAGE="$(git log --oneline | grep -A 1 -B 1 " → ${RELEASE_VERSION}" || true)"
	
	BUMP_VERSION_COMMITS="$(echo "${RECENT_COMMIT_MESSAGE}" | grep -A 1 -B 1 "Bump version:" || true)"
	if [[ ! -z "${BUMP_VERSION_COMMITS}" ]]; then
       echo "~~~ Important to know"
       echo "You have deleted the tags but the commit messages related to them still linger about."
       echo ""
       echo "Your most recent commit message related to ${TAG_NAME} still exists:"
       echo "${BUMP_VERSION_COMMITS}"
       echo ""; echo "Current HEAD: $(git rev-parse --short HEAD || true)"
       echo ""; echo "Suggest using the below commands to remove commit message:"
       echo "   git log                 ### list all the commits to examine them"
       echo "   git rebase -i HEAD~10   ### and then interactively remove the bump version related commits"
       echo ""; echo "   or "; echo ""
       echo "   git log                 ### list all the commits to examine them"
       echo "   git reset --hard [commit-sha] ### in case you can do this based on the git commit history"
       echo "                ### [commit-sha] the safe commit point you want your HEAD to point to"
	fi
}

fetchTags
checkIfAnyTagsExistAtAll

printUsageAndExistIfNoTagNameIsSpecified

exitIfTagNameDoesNotExist

echo "${TAG_NAME} does exist, proceeding further..."
deleteTag "local repo"  "git tag --delete ${TAG_NAME}"
deleteTag "remote repo" "git push --delete origin ${TAG_NAME}"

checkIfRecentCommitIfFromBumpversion