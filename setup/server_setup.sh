#!/usr/bin/env bash

# Launch an Ubuntu AMI under EC2 (currently using 16.04)

# Set up environment
sudo apt-get -y update
sudo apt-get -y install build-essential python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libhdf5-dev libx11-dev llvm libpq-dev
sudo apt-get -y install uwsgi-core libapache2-mod-wsgi nginx
sudo apt-get -y install git python-pip docker.io
sudo apt-get -y dist-upgrade

# Download and install anaconda
wget http://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh -b -p /home/ubuntu/anaconda2  # silent installation without answering options
nano .profile
# Set the following as path
PATH="$HOME/bin:$HOME/.local/bin:/home/ubuntu/anaconda2/bin:$PATH"

# Update all packages
conda update --all -y

# Pip install other essentials (not available on conda)
pip install regex

# Install nltk stop words
python -m nltk.downloader stopwords
python -m nltk.downloader wordnet

# Create new key
ssh-keygen -t rsa -C "eugeneyanziyou@gmail.com"
cat ~/.ssh/id_rsa.pub

# Clone datagene
git clone git@gitlab.com:eugeneyan/datagene.git
mkdir -p datagene/data/model

# Upload models
scp -i ~/.ssh/eugene_aws.pem categorization_dicts_small.pickle ubuntu@ec2-54-254-198-240.ap-southeast-1.compute.amazonaws.com:datagene/data/model
scp -i ~/.ssh/eugene_aws.pem categorization_dicts.tar.gz ubuntu@ec2-52-76-234-207.ap-southeast-1.compute.amazonaws.com:datagene/data/model

# Test datagene
python run.py 0.0.0.0 6688

# Set up proxy
cd /etc/nginx/sites-enabled/
sudo nano datagene.conf

# Paste this in
server {
    listen 80;
    server_name datagene.io;
    location / {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host      $http_host;
        proxy_pass         http://127.0.0.1:6688;
    }
}

server {
    listen 6689;
    server_name datagene.io;

    proxy_redirect off;
    proxy_buffering off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    location / {
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host      $http_host;
        proxy_pass         http://127.0.0.1:5555;
    }
}

# Remove existing configuration files
sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default

# Restart nginx
sudo service nginx restart
