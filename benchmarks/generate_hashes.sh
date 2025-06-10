# Set the range: from last v1.6.x to present (all 1.7.x merge commits, no bots)
git log --merges v1.6.3.. --pretty=format:"%H %s" | \
grep -v -i "dependabot" | \
grep -v -i "github-actions" | \
awk '{print $1}'  > no_bot_merge_commits.txt


#Get the commits for each minor version
git for-each-ref --sort=version:refname \
  --format='%(refname:short) %(objectname)' refs/tags | \
  grep -E '^v[1-9][0-9]*\..*' |
  awk '{print $2}' >> no_bot_merge_commits.txt
