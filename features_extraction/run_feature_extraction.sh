#!/bin/bash

# sudo yum install python3.7
# sudo yum install python3-devel

sudo pip3 install -r requirements.txt

nohup python3 extract_features.py