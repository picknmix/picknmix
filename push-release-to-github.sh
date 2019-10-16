#!/bin/bash

set -e
set -u
set -o pipefail

TARGET_REPO="picknmix/picknmix"

if [[ -z "${GITHUB_TOKEN}" ]]; then
  echo "GITHUB_TOKEN cannot be found in the current environment, please populate to proceed."
  exit -1
fi

TAG_NAME="${1:-}"
if [[ -z "${TAG_NAME}" ]]; then
  echo ""
  echo "Tag name is not specified, please pass it as a CLI arg"
  echo "   $0 [tag name]"
  echo "   for e.g. $0 v0.1"
  echo ""

  echo "Use git tag --list to find out available tags (tag names)"
  exit -1
fi

POST_DATA=$(printf '{
  "tag_name": "%s",
  "target_commitish": "master",
  "name": "%s",
  "body": "Release %s",
  "draft": false,
  "prerelease": false
}' ${TAG_NAME} ${TAG_NAME} ${TAG_NAME})
echo "Creating release ${RELEASE_VERSION}: $POST_DATA"
curl \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/vnd.github.v3+json" \
    -X POST -d "${POST_DATA}" "https://api.github.com/repos/${TARGET_REPO}/releases"

CURL_OUTPUT=".github-release.listing"
echo "Getting Github ReleaseId"
curl \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    -X GET "https://api.github.com/repos/${TARGET_REPO}/releases/tags/${TAG_NAME}" |
    tee ${CURL_OUTPUT}
RELEASE_ID=$(cat ${CURL_OUTPUT} | grep id | head -n 1 | tr -d " " | tr "," ":" | cut -d ":" -f 2)
echo "Release has been created ${RELEASE_ID} for tag ${TAG_NAME}"

echo ""
echo "Finished uploading to GitHub"
echo ""
echo "Checkout curl output at ${CURL_OUTPUT}, in case of errors"
echo ""
echo "Use curl -O -L [github release url] to download an installable artifact."
echo "    for e.g."
echo "        curl -O -L https://github.com/picknmix/releases/download/${TAG_NAME}.tgz"
echo ""
echo "        tar xvzf  ${TAG_NAME}.tgz"
echo ""
echo "        pip install ${TAG_NAME}"