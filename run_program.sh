#!/bin/bash

# get bills to request money for and create bash script
python3 main.py >> main_logs.log

# execute venmo requests
source venmo_requests_to_make.sh >> venmo_logs.log

# clean up directory and prepare for next run
rm venmo_requests_to_make.sh
