#!/bin/bash

#Required services
req_services=( "mysql-server" "apache2" "phpmyadmin" "python-pip" "python-dev" )

for rs in "${req_services[@]}"
do
  sudo apt-get install $rs
  echo "Installed ${rs}"
done

#required folders
cd /home/
mkdir foober
mkdir foober/files


#required python dependencies
echo "Installing python-dependencies"
req_python_libs=( "beautifulsoup4" "requests" "IPython" "peewee" "PyMySQL" "psutil" )
for lib in "${req_python_libs[@]}"
do
  sudo pip install $lib
  echo "Installed ${lib}"
done

sudo apt-get upgrade
