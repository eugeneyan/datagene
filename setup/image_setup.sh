#!/usr/bin/env bash
# For setting up an AMI

# Initialize variables and access AMI
# ======================================================================================================================
# Launch an Ubuntu AMI under EC2 (currently using 16.04)
SERVER=ubuntu@ec2-52-76-234-207.ap-southeast-1.compute.amazonaws.com
ssh-keygen -R ec2-52-76-234-207.ap-southeast-1.compute.amazonaws.com
ssh -i ~/.ssh/datagene_aws.pem ${SERVER}

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
cd skillsort
bundle install
sudo docker-compose build
sudo docker-compose up
sudo docker-compose run app script/setup
screen -S skillsort
sudo docker-compose up


# Start datagene.io
# ======================================================================================================================
cd ~/datagene
tar -zxvf data/model/categorization_dicts.tar.gz
mv categorization_dicts.pickle data/model/

# Test datagene
python run.py 0.0.0.0 6688

screen -S web
uwsgi --socket 127.0.0.1:6688 --ini uwsgi.ini >> web.log 2>&1

# Connect to public DNS to QA: ec2-54-254-154-139.ap-southeast-1.compute.amazonaws.com

# Associate datagene.io with EC2 instance
# ======================================================================================================================
# To associate datagene with ec2
# Network & Security -> Elastic IPs
# Disassociate from existing EC2 instance and associate with new EC2 instance