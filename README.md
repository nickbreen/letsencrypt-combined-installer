


# installation

Copy the files to the letsencrypt python virtual environment.
```
cp -r letsencrypt_haproxy letsencrypt_haproxy-0.0.1.dist-info /path/to/letsencrypt/venv/lib/python2.7/site-packages/
```

Specify the installer and optionally the path to output the combined certificates to.

```
source venv/bin/activate
letsencrypt \
  --authenticator webroot -webroot-path /var/www/html \
  --installer letsencrypt-haproxy:installer --combined-path /certs \
  --domains www.example.com,example.com
```
