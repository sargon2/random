#!/bin/bash -e

BITBUCKET_USERNAME="dbesen"
BITBUCKET_APP_PASSWORD="..."
# read -s -p "Enter your Bitbucket app password: " BITBUCKET_APP_PASSWORD
BITBUCKET_WORKSPACE="dbesen"

# Manually run `gh auth login`

# Get list of Bitbucket repos (name + visibility)
REPOS_JSON=$(curl -s -u "$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD" \
    "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE?pagelen=100")

REPOS=$(echo "$REPOS_JSON" | jq -r '.values[] | @base64')

for REPO in $REPOS; do
    DECODED_REPO=$(echo "$REPO" | base64 --decode)
    REPO_NAME=$(echo "$DECODED_REPO" | jq -r '.slug')
    IS_PRIVATE=$(echo "$DECODED_REPO" | jq -r '.is_private')

    if [[ "$IS_PRIVATE" == "true" ]]; then
        VISIBILITY="true"
    else
        VISIBILITY="false"
    fi

    echo "Migrating $REPO_NAME (Private: $VISIBILITY)..."

    # Clone the repo
    git clone --mirror "https://$BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD@bitbucket.org/$BITBUCKET_WORKSPACE/$REPO_NAME.git"

    # Create GitHub repo with the same visibility
    cd $REPO_NAME.git
    git remote rm origin
    if [[ "$IS_PRIVATE" == "true" ]]; then
        gh repo create $REPO_NAME --source . --push --private
    else
        gh repo create $REPO_NAME --source . --push --public
    fi
    cd ..

    echo "Migration of $REPO_NAME completed!"
done

