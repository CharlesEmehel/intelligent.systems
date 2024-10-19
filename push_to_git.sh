#!/bin/bash

echo "Pushing updates..."

# Navigate to project directory
cd ~/andromeda || exit 1

# Display the current status
git status

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
  echo "No changes to commit."
else
  # Stage all changes
  git add .

  # Check if a commit message was provided
  if [ -z "$1" ]; then
    COMMIT_MESSAGE="Automated commit"
  else
    COMMIT_MESSAGE="$1"
  fi

  # Commit the changes with the message
  git commit -m "$COMMIT_MESSAGE"

  # Push the changes to the remote repository
  git push origin main

  echo "...done!"
fi
