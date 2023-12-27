#!/bin/bash

is_readable() {
  head -c1 "$1" > /dev/null 2>&1
  return $?
}

DIRECTORY="/backup-pool1/"

if [ -d "$DIRECTORY" ]; then
  # List all files in the directory and its subdirectories
  find "$DIRECTORY" -type f | while read -r FILE; do
    if is_readable "$FILE"; then
      echo "File is readable: $FILE"
    else
      echo "File is not readable: $FILE"
    fi
  done
else
  echo "Directory not found: $DIRECTORY"
fi
