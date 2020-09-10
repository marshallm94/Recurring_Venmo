#!/bin/bash

log_dir='logs'
mkdir $log_dir

python3 main.py 2> $log_dir/main_errors.log > $log_dir/main_logs.log
