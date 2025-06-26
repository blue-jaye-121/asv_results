#!/bin/bash
#Set repository info
RESULTS_REPO_URL="https://github.com/blue-jaye-121/results_asv_results.git" #results repo
ASV_RESULTS_PATH="./asv/results" #the path of the asv results folder in the main repo
CLONE_DIR="temp_repo_asv_run" # A temporary repo to clone to - deleted at the end of the script


#Checkout results repo
#git clone "$RESULTS_REPO_URL" "$CLONE_DIR" TODO: Add this to Jenkinsfile

#If the results folder exists, copy it into our main repo for asv running
#if [ -d "$CLONE_DIR"/results ]; then 
#    echo "copying results"
#    cp -r "$CLONE_DIR"/results/* "$ASV_RESULTS_PATH"
#else 
#    echo "cannot copy results"
#    exit 1
#fi

#Call on the script to generate the commit hashes
echo "----------------executing generate_hashes-------------------------"
sh ./generate_hashes.sh #TODO: make this not an absolute path
echo "----------------generate_hashes complete -------------------------"

#Install asv
pip install asv virtualenv

#Set up asv machine
asv machine --yes

#Run asv
#TODO: Make this everything & also a does not exist 
asv run HASHFILE:no_bot_merge_commits.txt -q -b other_benchmarks
   
#Commit and push benchmark results to results repo
#if [ -d "$CLONE_DIR"/results ]; then #if the results_asv_results repo exits
#    rm -r "$CLONE_DIR"/results       #delete it 
#fi 
#cp -r "$ASV_RESULTS_PATH" "$CLONE_DIR"/results #copy the results to the results_asv_results repo
#cd "$CLONE_DIR"                                #move into the results repo
#git config --local user.email "script@noreply.com"
#git config --local user.name "ASV Script [bot]"
#git add results                                #TODO: Add following to Jenkinsfile
#git commit -m "Update benchmark results"

#git push "$RESULTS_REPO_URL" main:main
    

#cd .. # Leave temporary repo
#CLEANUP: remove temp_repo
#rm -rf "$CLONE_DIR"
