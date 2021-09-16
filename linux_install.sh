#!/bin/bash
pip3 install -r requirements.txt
sudo apt-get update
sudo apt-get -y install build-essential libpoppler-cpp-dev pkg-config python-dev
sudo apt-get -y install python3-tk  # Only works for debian systems
