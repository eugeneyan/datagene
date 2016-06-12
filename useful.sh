#!/usr/bin/env bash

# To install nltk stopwords
python -m nltk.downloader stopwords

# Sample api call on localhost
curl -i http://localhost:6688/categorize -X post -H "Content-type: application/json" -d'{"title":"This is a wooden bookshelf with a clock"}'

# Sample api call to machine ipaddress
curl -i http://192.168.1.107:6688/categorize -X post -H "Content-type: application/json" -d'{"title":"This is a wooden bookshelf with a clock"}'
