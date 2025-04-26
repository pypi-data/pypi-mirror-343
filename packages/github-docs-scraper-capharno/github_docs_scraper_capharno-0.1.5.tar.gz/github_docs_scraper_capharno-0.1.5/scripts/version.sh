#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Check for release type argument (patch, minor, major)
if [ -z "$1" ]; then
  echo "Usage: ./release.sh <patch|minor|major>"
  exit 1
fi

PART=$1

echo "Bumping version ($PART)..."
bump-my-version bump "$PART"

# Assuming bump-my-version created a commit and tag
echo "Pushing commit..."
git push

echo "Pushing tags..."
git push --tags

echo "Release process initiated for $PART bump."
