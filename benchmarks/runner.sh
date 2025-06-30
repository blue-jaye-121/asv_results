#!/bin/bash
git config --global --add safe.directory /container-benchmarks
cd /container-benchmarks/benchmarks
./asv_run_script.sh
