#!/bin/bash
pip3 install venmo

# this will require user input to setup
venmo configure

# install Google Client Library
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
