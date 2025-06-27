#!/bin/bash
#Set repository info
RESULTS_REPO_URL="https://github.com/blue-jaye-121/results_asv_results.git" #results repo
ASV_RESULTS_PATH="./asv/results" #the path of the asv results folder in the main repo
CLONE_DIR="temp_repo_results" # A temporary repo to clone to - deleted at the end of the script


#Checkout results repo
git clone "$RESULTS_REPO_URL" "$CLONE_DIR"

#If the results folder exists, copy it into our main repo for asv running
if [ -d "$CLONE_DIR"/results ]; then 
   echo "---------copying results---------"
   cp -r "$CLONE_DIR"/results/* "$ASV_RESULTS_PATH"
   echo "---------results copied----------"
else 
   echo "cannot copy results"
   exit 1
fi