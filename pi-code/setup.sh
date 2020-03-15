#!/bin/bash

sudo mkdir /var/www/html/.well-known
sudo mkdir /var/www/html/.well-known/acme-challenge
echo '---> Installing Open SSL <---------'
sudo apt-get install openssl
echo '---> Installing GPIO library <----------'
sudo apt-get install python-rpi.gpio
echo '---> Installing Nginx <----------'
sudo apt-get install nginx
echo '---> Installing certbot <----------'
sudo apt-get install certbot
echo '---> Starting Nginx <----------'
sudo systemctl start nginx

echo '---> Creating certs for GCP Core IoT <--------------'
if [ ! -d "certs" ]; then
	mkdir certs
fi

openssl genrsa -out certs/rsa_private.pem 2048
openssl rsa -in certs/rsa_private.pem -pubout -out certs/rsa_public.pem
cd certs
wget https://pki.goog/roots.pem
cd ..

echo '---> Installing python requirements <--------'
pip3 install -r requirements.txt

#if ! test -f "cert.pem"; then
#	echo 'Generating self-signed certs'
#	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem
#fi

