# Set repo info
REPO_URL="https://github.com/Unidata/MetPy.git"
CLONE_DIR="temp_repo"

# --- SHALLOW CLONE ---
git clone --depth=100 --no-tags "$REPO_URL" "$CLONE_DIR"
cd "$CLONE_DIR" || exit 1
git fetch --tags

# Set the range: from last v1.6.x to present (all 1.7.x merge commits, no bots)
git log --merges v1.6.3.. --pretty=format:"%H %s" | \
grep -v -i "dependabot" | \
grep -v -i "github-actions" | \
awk '{print $1}'  > ../no_bot_merge_commits.txt


#Get the commits for each minor version
git for-each-ref --sort=version:refname \
  --format='%(refname:short) %(objectname)' refs/tags | \
  grep -E '^v[1-9][0-9]*\..*' |
  awk '{print $2}' >> ../no_bot_merge_commits.txt
  
cd ..

# --- CLEANUP ---
rm -rf "$CLONE_DIR"