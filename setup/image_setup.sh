#!/usr/bin/env bash
# For setting up an AMI

# Initialize variables and access AMI
# ======================================================================================================================
# Launch an Ubuntu AMI under EC2 (currently using 16.04)
SERVER=ubuntu@ec2-54-169-238-164.ap-southeast-1.compute.amazonaws.com
ssh -i ~/.ssh/eugene_aws.pem ${SERVER}


# Set up datagene.io environment
# ======================================================================================================================
# Create new key
ssh-keygen -t rsa -C "eugeneyanziyou@gmail.com"
cat ~/.ssh/id_rsa.pub

# Pull datagene.io
cd datagene
git pull


# Set up SortMySkills
# ======================================================================================================================
# Set up SortMySkills Docker
sudo docker-compose build
screen -S skillsort
sudo docker-compose up


# Start datagene.io
# ======================================================================================================================
cd ~/datagene
screen -S web
python run.py 127.0.0.1 6688 >> web.log 2>&1
