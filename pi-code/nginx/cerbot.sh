#At this time, just a scratch pad to get things working.
# currently uses test-cert to hit a staging server and dry-run 

# register, a one time deal
sudo certbot register -m mrncmoose@gmail.com --agree-tos

# get inital cert
sudo certbot run -d trainingtstat.hopto.org --nginx -m mrncmoose@gmail.com --agree-tos --test-cert 

# renew cert
sudo certbot certonly -d trainingtstat.hopto.org --nginx -m mrncmoose@gmail.com --agree-tos --test-cert --dry-run
