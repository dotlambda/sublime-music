#! /bin/bash

set -e

# The release notes for this version should be the first line of the CHANGELOG.
if [[ $(head -n 1 CHANGELOG.rst) == "${CI_COMMIT_TAG}" ]]; then
    # Extract all of the bullet points and other things until the next header.
    i=0
    first=1
    while read l; do
        i=$(( $i + 1 ))
        if [[ $l =~ ^=+$ ]]; then
            if [[ $first == 0 ]]; then
                break
            fi
            first=0
        fi
    done < CHANGELOG.rst

    # i is now the index of the line below the second header.

    description="**Release Notes:**
$(head -n $(( $i - 2 )) CHANGELOG.rst | tail -n $(( $i - 5 )))"
fi

if [[ "${description}" == "" ]]; then
    description="No description provided for this release."
fi

description=$(echo "$description" | sed ':a;N;$!ba;s/\n/\\n/g')

url="${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/releases"
data="
{
    \"name\": \"${CI_COMMIT_TAG}\",
    \"tag_name\": \"${CI_COMMIT_TAG}\",
    \"description\": \"${description}\",
    \"assets\": {
        \"links\": [
            {
                \"name\": \"sublime-music-${CI_COMMIT_TAG}.flatpak\",
                \"url\": \"${CI_PROJECT_URL}/-/jobs/artifacts/${CI_COMMIT_TAG}/raw/flatpak/sublime-music.flatpak?job=build_flatpak\"
            }
        ]
    }
}
"

echo "URL:"
echo "$url"
echo "DATA:"
echo "$data"

curl \
    --header 'Content-Type: application/json' \
    --header "PRIVATE-TOKEN: ${RELEASE_PUBLISH_TOKEN}" \
    --data "$data" \
    --request POST \
    $url
