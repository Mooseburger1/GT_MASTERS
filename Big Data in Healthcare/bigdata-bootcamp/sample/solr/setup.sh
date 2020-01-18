#!/bin/bash

echo 'Downloading Solr'
wget http://www-eu.apache.org/dist/lucene/solr/6.4.0/solr-6.4.0.tgz

echo 'Unzipping Solr'
tar -xvf solr-6.4.0.tgz

echo 'Remove tar'
rm solr-6.4.0.tgz
