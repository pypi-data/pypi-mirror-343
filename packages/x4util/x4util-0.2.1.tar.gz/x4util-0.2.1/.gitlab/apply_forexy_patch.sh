#!/bin/bash

# Script to apply changes from a specific commit in one git repository to another
# Usage: ./apply_changes.sh <source_repo_path> <target_repo_path> [commit_hash]

set -e

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 <source_repo_path> <target_repo_path> [commit_hash]"
    echo "If commit_hash is not provided, HEAD will be used"
    exit 1
fi

SOURCE_REPO=$1
TARGET_REPO=$2
COMMIT_HASH=$3

echo $(pwd)
echo $(ls -a)

# Validate paths - convert to absolute paths
SOURCE_REPO=$SOURCE_REPO # $(realpath "$SOURCE_REPO")
TARGET_REPO=$TARGET_REPO # $(realpath "$TARGET_REPO")

if [ ! -d "$SOURCE_REPO/.git" ]; then
    echo "Error: Source path '$SOURCE_REPO' is not a git repository"
    exit 1
fi

if [ ! -d "$TARGET_REPO/.git" ]; then
    echo "Error: Target path '$TARGET_REPO' is not a git repository"
    exit 1
fi

# Validate commit hash exists
(cd "$SOURCE_REPO" && git cat-file -e "$COMMIT_HASH" 2>/dev/null) || {
    echo "Error: Commit hash '$COMMIT_HASH' does not exist in source repository"
    exit 1
}

echo "Using commit: $(cd "$SOURCE_REPO" && git rev-parse --short "$COMMIT_HASH") - $(cd "$SOURCE_REPO" && git log -1 --pretty=format:'%s' "$COMMIT_HASH")"

# Get list of Python files changed in the specified commit
echo "Finding Python files changed in the specified commit..."
CHANGED_FILES=$(cd "$SOURCE_REPO" && git diff-tree --no-commit-id --name-only -r "$COMMIT_HASH" | grep '\.py$' || echo "")

# Check if we found any Python files
if [ -z "$CHANGED_FILES" ]; then
    echo "No Python files changed in the specified commit"
    exit 1
fi

echo "Found $(echo "$CHANGED_FILES" | wc -l) changed Python files in the commit"

# Create a temporary directory for patches
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# For each changed Python file, create and apply patch
for RELATIVE_PATH in $CHANGED_FILES; do
    # Get the filename without the path
    FILENAME=$(basename "$RELATIVE_PATH")
    
    echo "Processing $FILENAME ($RELATIVE_PATH)..."
    
    # Find the corresponding file in the target repo
    TARGET_FILE=$(find "$TARGET_REPO" -name "$FILENAME" -type f | head -1)
    
    if [ -z "$TARGET_FILE" ]; then
        echo "  - Warning: No matching file found in target repository for $FILENAME, skipping"
        continue
    fi

    # Get relative path components
    cd "$TARGET_REPO"
    TARGET_REPO_ABSOLUTE=$(pwd)
    cd - > /dev/null

    TARGET_FILENAME=$(basename "$TARGET_FILE")
    TARGET_DIR=$(dirname "$TARGET_FILE")

    # Get absolute path of directory containing the file
    cd "$TARGET_DIR"
    TARGET_DIR_ABSOLUTE=$(pwd)
    cd - > /dev/null

    # Calculate relative path
    TARGET_RELATIVE_PATH=${TARGET_DIR_ABSOLUTE#$TARGET_REPO_ABSOLUTE/}/$TARGET_FILENAME


    # Get target file path relative to target repo
    #TARGET_RELATIVE_PATH=$(realpath --relative-to="$TARGET_REPO" "$TARGET_FILE")
    echo "  - Found target file: $TARGET_FILE (relative: $TARGET_RELATIVE_PATH)"
    
    # Create separate working directories to handle patches properly
    SRC_WORK_DIR="$TEMP_DIR/source"
    TGT_WORK_DIR="$TEMP_DIR/target"
    
    mkdir -p "$SRC_WORK_DIR" "$TGT_WORK_DIR"
    
    # Get the content of the file before and after the commit
    (cd "$SOURCE_REPO" && git show "$COMMIT_HASH^:$RELATIVE_PATH" > "$SRC_WORK_DIR/file.old") || {
        # File might be new, create empty file
        touch "$SRC_WORK_DIR/file.old"
    }
    
    (cd "$SOURCE_REPO" && git show "$COMMIT_HASH:$RELATIVE_PATH" > "$SRC_WORK_DIR/file.new") || {
        echo "  - Error getting new file content, skipping"
        continue
    }
    
    # Copy the current target file
    cp "$TARGET_FILE" "$TGT_WORK_DIR/file"
    
    # Create a proper unified diff
    diff -u "$SRC_WORK_DIR/file.old" "$SRC_WORK_DIR/file.new" > "$TEMP_DIR/$FILENAME.diff" 2>/dev/null || true
    
    # Check if diff is empty
    if [ ! -s "$TEMP_DIR/$FILENAME.diff" ]; then
        echo "  - No changes detected for $FILENAME, skipping"
        continue
    fi
    
    # Modify the diff headers to match the target file paths
    sed -i "s|^--- $SRC_WORK_DIR/file.old|--- a/$TARGET_RELATIVE_PATH|" "$TEMP_DIR/$FILENAME.diff"
    sed -i "s|^+++ $SRC_WORK_DIR/file.new|+++ b/$TARGET_RELATIVE_PATH|" "$TEMP_DIR/$FILENAME.diff"
    
    # Apply the patch to the target repository
    echo "  - Applying changes to target file"
    (cd "$TARGET_REPO" && git apply --verbose --reject --whitespace=fix "$TEMP_DIR/$FILENAME.diff") || {
        echo "  - Warning: Patch application had issues, check for .rej files"
    }
done

echo "All changes have been applied"
echo "Please check the target repository for any .rej files that indicate failed patches"
echo "You may need to review and commit the changes in the target repository manually"

# Clean up
rm -rf "$TEMP_DIR"
echo "Temporary files cleaned up"