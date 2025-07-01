#!/bin/bash
#Run asv

#Set up asv machine
asv machine --yes

#TODO: Make this everything & also a does not exist 
asv run HASHFILE:benchmarks/no_bot_merge_commits.txt
