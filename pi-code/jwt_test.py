import jwt
import datetime

certDir = 'certs'
#privateKeyFile = certDir + '/rsa_public.pem'
privateKeyFile = certDir + '/rsa_private.pem'
ca_certs = certDir + '/roots.pem'
algorithm = 'RS256'
#algorithm = 'HS256'

with open(privateKeyFile, 'r') as f:
    private_key = f.read()
        
myJwt = jwt.encode({'some': 'payload'}, private_key, algorithm=algorithm)
print('Jwt created: {0}'.format(myJwt))

