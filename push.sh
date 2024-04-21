bastimestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Check if the user provided a commit message as the first argument
if [ -z "$1" ]; then
    # No message provided, use default
    commit_message="${timestamp} committed via bash"
else
    # Use the provided message
    commit_message="$1"
fi

git add .
git commit -m "${commit_message}"
git push
