#!/usr/bin/env bash
# For setting up an empty server from scratch


# Initialize variables
# ======================================================================================================================
# Launch an Ubuntu AMI under EC2 (currently using 16.04)
SERVER=ubuntu@ec2-52-77-223-31.ap-southeast-1.compute.amazonaws.com
CATEGORIZATION_DIR=~/eugeneyan/datagene/data/model
IMAGE_CATEGORIZATION_DIR=~/eugeneyan/datagene/data/images_clothes/model
SEARCH_IMAGE_DIR=~/eugeneyan/datagene/data/images/

ssh -i ~/.ssh/eugene_aws.pem ${SERVER}


# Set up linux environment
# ======================================================================================================================
sudo apt-get -y update
sudo apt-get -y install build-essential python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libhdf5-dev libx11-dev llvm libpq-dev
sudo apt-get -y install uwsgi-core libapache2-mod-wsgi nginx
sudo apt-get -y install git python-pip docker.io mailutils
sudo apt-get -y install mailutils postfix
sudo apt-get -y install uwsgi-plugin-python
sudo apt-get -y install python-pip
sudo apt-get -y dist-upgrade
sudo apt-get -y update


# Set up python environment
# ======================================================================================================================
# Download and install anaconda
wget http://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh -b -p /home/ubuntu/anaconda2  # silent installation without answering options
nano .profile
# Set the following as path
PATH="$HOME/bin:$HOME/.local/bin:/home/ubuntu/anaconda2/bin:$PATH"
PYTHONHOME="/home/ubuntu/anaconda2/bin"

# Update all packages
conda update --all -y
conda install keras -y
conda install -c conda-forge uwsgi=2.0.12 -y

# Pip install other essentials (not available on conda)
pip install regex
pip install uwsgi
sudo pip install docker-compose==1.2.0  # need sudo for this!

# Install nltk stop words
python -m nltk.downloader stopwords
python -m nltk.downloader wordnet

# Change to use theano backend
# Start python and import Keras at least once
cd ~/.keras
nano keras.json
# Set the following
{
    "image_dim_ordering": "th",
    "epsilon": 1e-07,
    "floatx": "float32",
    "backend": "theano"
}


# Set up datagene.io environment
# ======================================================================================================================
# Create new key
ssh-keygen -t rsa -C "eugeneyanziyou@gmail.com"
cat ~/.ssh/id_rsa.pub

# Clone datagene
git clone git@gitlab.com:eugeneyan/datagene.git
mkdir -p datagene/data/model
mkdir -p datagene/data/images_clothes/model
mkdir -p datagene/data/images_clothes/pred_images
mkdir -p datagene/data/images/search_features
mkdir -p datagene/data/images/search_dicts
mkdir -p datagene/data/images/search_image

# Upload models
scp -i ~/.ssh/eugene_aws.pem ${SEARCH_IMAGE_DIR}/train_top_level.tar.gz ${SERVER}:datagene/data/images
scp -i ~/.ssh/eugene_aws.pem ${CATEGORIZATION_DIR}/categorization_dicts_small.pickle ${SERVER}:datagene/data/model
scp -i ~/.ssh/eugene_aws.pem ${CATEGORIZATION_DIR}/categorization_dicts.tar.gz ${SERVER}:datagene/data/model
scp -i ~/.ssh/eugene_aws.pem ${IMAGE_CATEGORIZATION_DIR}/resnet50_finetuned_4block.h5 ${SERVER}:datagene/data/images_clothes/model
scp -i ~/.ssh/eugene_aws.pem ${IMAGE_CATEGORIZATION_DIR}/image_category_dict.pickle ${SERVER}:datagene/data/images_clothes/model
scp -i ~/.ssh/eugene_aws.pem ${SEARCH_IMAGE_DIR}/search_features/search_features.npy ${SERVER}:datagene/data/images/search_features
scp -i ~/.ssh/eugene_aws.pem ${SEARCH_IMAGE_DIR}/search_dicts/search_dicts.pickle ${SERVER}:datagene/data/images/search_dicts

# Test datagene
python run.py 0.0.0.0 6688


# Set up ruby environment
# ======================================================================================================================
# Install RVM and update Ruby
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -sSL https://get.rvm.io | bash -s stable --rails
source /home/ubuntu/.rvm/scripts/rvm
rvmsudo gem install pg -v '0.19.0'
cd datagene/skillsort
rvmsudo bundle install
gem install rubygems-bundler
sudo chmod -R 1777 /home/ubuntu/.rvm/gems/ruby-2.3.3/bin
gem regenerate_binstubs

# Set up SortMySkills Docker
sudo docker-compose run app script/setup
bundle install
sudo docker-compose build
screen -S skillsort
sudo docker-compose up
sudo rm tmp/pids/server.pid  # If "a server is already running error"


# Set up nginx
# ======================================================================================================================
# To associate datagene with ec2
# - Get elastic IP and associate with EC2 instance
# - Route 53 > Domain > Manage DNS
# - Update datagene.io record set (with type A) with elastic IP

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
        client_max_body_size 3M;
    }

#    Doesn't work
#    location /sortmyskills {
#        proxy_set_header   X-Real-IP $remote_addr;
#        proxy_set_header   Host      $http_host;
#        proxy_pass         http://127.0.0.1:5555/;
#    }
}

server {
    listen 6689;
    server_name datagene.io;

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


# Start datagene.io
# ======================================================================================================================
cd ~/datagene
screen -S web
python run.py 127.0.0.1 6688 >> web.log 2>&1