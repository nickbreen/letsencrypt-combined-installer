# Installation

Install (in to the letsencrypt python virtual environment). Assuming letsencrypt is installed to `/opt/letsencrypt`.

```
URL=$(curl -LsSf https://api.github.com/repos/nickbreen/letsencrypt-combined-installer/releases/latest | jq .tarball_url)
curl -LsSf $URL | tar zx -C /opt
source /opt/letsencrypt/venv/bin/activate
cd /opt/letsencrypt-combined-installer-*
python setup.py install
```

# Usage

Specify the installer and optionally the path to output the combined certificates to.

```
source /opt/letsencrypt/venv/bin/activate
letsencrypt \
  --authenticator webroot -webroot-path /var/www \
  --installer letsencrypt-combined:combined --letsencrypt-combined:combined-path /certs \
  --domains example.com
```


# Self Signed Certificates

Self-signed certificates can also be installed with this tool.

```
# Generate a self-signed certificate.
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 90 -nodes -subj '/CN=example.com/O=Test/C=NZ'

# Install it
le --config $XDG_CONFIG_HOME/letsencrypt/install.ini install \
    --cert-path cert.pem \
    --key-path key.pem \
    --domains example.com
```
