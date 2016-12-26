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
