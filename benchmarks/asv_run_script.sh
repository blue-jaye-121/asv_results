#!/bin/bash
#Set repository info
RESULTS_REPO_URL="https://github.com/blue-jaye-121/results_asv_results.git" #results repo
ASV_RESULTS_PATH="./asv/results" #the path of the asv results folder in the main repo
CLONE_DIR="temp_repo_asv_run" # A temporary repo to clone to - deleted at the end of the script

#Call on the script to generate the commit hashes
echo "----------------executing generate_hashes-------------------------"
sh ./generate_hashes.sh #TODO: make this not an absolute path
echo "----------------generate_hashes complete -------------------------"


#Set up asv machine
asv machine --yes

#Run asv
#TODO: Make this everything & also a does not exist 
asv run HASHFILE:no_bot_merge_commits.txt
