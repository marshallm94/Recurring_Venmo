#!/bin/bash

# get bills to request money for and create bash script -
# In english: "Run main.py and pipe and errors to main_errors.log and any output
# to main_logs.log. If main.py succeeds, make venmo_requests_to_make.sh executable"
python3 main.py 2> main_errors.log > main_logs.log && chmod +x venmo_requests_to_make.sh

# execute venmo requests -
# In english: "Run venmo_requests_to_make.sh and pipe and errors to request_errors.log
# and any output to venmo_logs.log. If venmo_requests_to_make.sh succeeds, delete the file."
bash venmo_requests_to_make.sh 2> request_errors.log > venmo_logs.log && rm venmo_requests_to_make.sh
