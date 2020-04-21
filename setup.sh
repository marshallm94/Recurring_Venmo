#!/bin/bash

# raspberry pi related installations 
sudo apt-get -y install git
sudo apt-get -y install python3-pip
sudo apt-get -y install python3-numpy
sudo apt-get -y install vim 

# program related installations
pip3 install venmo
pip3 install httplib2
pip3 install oauth2client
pip3 install base64
pip3 install email
pip3 install apiclient

# for Raspberry Pi setup - adds venmo directory to PATH
echo 'export PATH=$PATH:/home/pi/.local/bin' >> ~/.bashrc

# this will require user input to setup
venmo configure

# install Google Client Library
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
