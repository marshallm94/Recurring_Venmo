#!/bin/bash

# get bills to request money for and create bash script
python main.py

# execute venmo requests
source venmo_requests_to_make.sh >> last_run_logs.log

# clean up directory and prepare for next run
rm venmo_requests_to_make.sh
