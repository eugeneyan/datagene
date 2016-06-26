#!/usr/bin/env bash

# Set up environment
sudo apt-get -y update
sudo apt-get -y install build-essential python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libhdf5-dev libx11-dev llvm git uwsgi-core libapache2-mod-wsgi

# Download and install anaconda
wget http://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh
bash Anaconda2-4.0.0-Linux-x86_64.sh -b -p /home/ubuntu/anaconda2  # silent installation without answering options

# Source add anaconda to path and source
export PATH=/home/ubuntu/anaconda2/bin:$PATH
source .bashrc

# Install pip
sudo apt-get install python-pip
pip install --upgrade pip

# Update all packages
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# Pip install virtualenvwrapper
sudo pip install virtualenvwrapper
source "/usr/local/bin/virtualenvwrapper.sh"

# Pip install other essentials
pip install regex

# Install nltk stop words
python -m nltk.downloader stopwords

# Install uwsgi
sudo apt-get -y install nginx supervisor
pip install uwsgi