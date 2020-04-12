#!/bin/bash
sudo apt-get -y install git
sudo apt-get -y install python3-pip
sudo apt-get -y install vim 

pip3 install venmo

# for Raspberry Pi setup - adds venmo directory to PATH
echo 'export PATH=$PATH:/home/pi/.local/bin' >> ~/.bashrc

# this will require user input to setup
venmo configure

# install Google Client Library
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
