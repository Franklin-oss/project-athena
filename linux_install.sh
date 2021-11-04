#!/bin/bash
sudo apt-get update
sudo apt-get -y install build-essential libpoppler-cpp-dev pkg-config python-dev python3-pip
sudo apt-get -y install python3-tk  # Only works for debian systems
pip3 install -r requirements.txt
