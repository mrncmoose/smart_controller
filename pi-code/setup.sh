sudo mkdir /var/www/html/.well-known
sudo mkdir /var/www/html/.well-known/acme-challenge
echo '---> Installing python requirements <--------'
pip3 install -r requirements.txt
echo '---> Installing GPIO library <----------'
sudo apt-get install python-rpi.gpio
echo '---> Installing Nginx <----------'
sudo apt-get install nginx
echo '---> Installing certbot <----------'
sudo apt-get install certbot
echo '---> Starting Nginx <----------'
sudo systemctl start nginx

#if ! test -f "cert.pem"; then
#	echo 'Generating self-signed certs'
#	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem
#fi

