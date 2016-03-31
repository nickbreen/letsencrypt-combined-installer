# installation

Get and copy/link the files to the letsencrypt python virtual environment.
```
git clone https://github.com/nickbreen/letsencrypt-combined-installer /opt/letsencrypt-combined-installer
ln -s /opt/letsencrypt-combined-installer/combined.py /opt/letsencrypt/venv/lib/python2.7/site-packages/
```

Specify the installer and optionally the path to output the combined certificates to.

```
source venv/bin/activate
letsencrypt \
  --authenticator webroot -webroot-path /var/www/html \
  --installer combined --combined-path /certs \
  --domains www.example.com,example.com
```
