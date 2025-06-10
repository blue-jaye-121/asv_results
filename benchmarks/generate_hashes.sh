# Set repo info
REPO_URL="https://github.com/Unidata/MetPy.git" #metpy repo to clone from
CLONE_DIR="temp_repo" #temporary repo to clone to 

# --- SHALLOW CLONE ---
git clone --depth=100 --no-tags "$REPO_URL" "$CLONE_DIR" #shallow clone metpy repo
cd "$CLONE_DIR" || exit 1 #change directories to temporary repo
git fetch --tags #fetch metpy tags

# Set the range: from last v1.6.x to present (all 1.7.x merge commits) - no commits authored by or mentioning dependabot or github-actions
git log --merges v1.6.3.. --pretty=format:"%H %s" | \
grep -v -i "dependabot" | \
grep -v -i "github-actions" | \
awk '{print $1}'  > ../no_bot_merge_commits.txt #print output to this file in the benchmarks dir


#Get the commit hashes for each minor version after 1.0
git for-each-ref --sort=version:refname \
  --format='%(refname:short) %(objectname)' refs/tags | \
  grep -E '^v[1-9][0-9]*\..*' |
  awk '{print $2}' >> ../no_bot_merge_commits.txt #append these results to same file 
  
cd ..

# --- CLEANUP ---
rm -rf "$CLONE_DIR" #clean up by removing temporary repo