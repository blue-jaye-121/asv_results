#!/C:/users/savan/Unidata/asv_metpy/metpy/benchmarks
#Simple bash script to view the commit messages
echo "Path to file:" 
read file_path; 
while IFS= read -r line; do
    git show -s --format=%s $line
done < "$file_path"