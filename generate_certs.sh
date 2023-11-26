#!/bin/bash

ENV=$1 # Pass "prod" or "dev" as an argument
DOM=mydomain.com # Replace with your domain
MAIL=your-email@mydomain.com # Replace with your email

if [ "$ENV" == "prod" ]; then
    # Generate certificates with Let's Encrypt
    sudo certbot certonly --standalone -d "$DOM" --non-interactive --agree-tos --email "$MAIL"
    sudo cp /etc/letsencrypt/live/$DOM/fullchain.pem ./certs/cert.pem
    sudo cp /etc/letsencrypt/live/$DOM/privkey.pem ./certs/key.pem
elif [ "$ENV" == "dev" ]; then
    # Generate certificates with mkcert
    mkcert -install
    mkcert -key-file ./certs/key.pem -cert-file ./certs/cert.pem localhost
else
    echo "Please specify 'prod' or 'dev' as an environment."
fi
ч