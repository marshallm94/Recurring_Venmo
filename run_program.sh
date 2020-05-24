#!/bin/bash

# >> = append to file if the file already has data
# > _file_ = stdout will overwrite data in _file_
# 2> _file_ = stderr will overwrite data in _file_ 

# get bills to request money for and create bash script
python3 main.py > main_logs.log

# execute venmo requests
# pipe any errors to request_logs.log, stdout to venmo_logs.log and only remove
# venmo_requests_to_make.sh if there weren't any any errors
bash venmo_requests_to_make.sh 2> request_logs.log > venmo_logs.log && rm venmo_requests_to_make.sh
