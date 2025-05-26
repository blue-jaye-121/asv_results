#!/C:/users/savan/Unidata/asv_metpy/metpy/benchmarks
#Simple bash script to view the commit messages
while IFS= read -r line; do
    git show -s --format=%s $line
done < benchmarks/commit_message_pr_merges.txt