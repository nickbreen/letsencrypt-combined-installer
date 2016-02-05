


# installation

be sure this module is installed. It it not yet pip activated. It means coping the files
to

/path/to/letsencrypt/venv/lib/python2.7/site-packages/letsencrypt_haproxy
/path/to/letsencrypt/venv/lib/python2.7/site-packages/letsencrypt_haproxy-0.0.1.dist-info/

afterwards, source the letsencrypt enviroment and get a certificate

```
source venv/bin/activate
letsencrypt --authenticator letsencrypt-haproxy:auth --installer  letsencrypt-haproxy:installer  -d domainname.com
```


# haproxy configuration. 


Below is a snippet of haproxy configuration. 
The ACL lines are important to redirect traffice to the ACME challenge 
system. The LE-BIND and LE-REDIRECT are placeholders for where
the lets encrypt system can configure the domainnames

This because haproxy is not domainname/servername aware per default


```
frontend http
    log     global
    mode http
    option tcplog
    bind 0.0.0.0:80

    # Handle LE requests and forward them locally
    acl is_letsencrypt path_beg -i /.well-known/acme-challenge/
    use_backend letsencrypt if is_letsencrypt


    # This '## LE-BIND and ## LE-REDIRECT are magic placeholders'
    # LE-BIND means (SNI) bind will be added here for the specified domain
    # LE-REDIRECT means URL matching the given URL will be redirect to https://

    ## LE-BIND example.com

    ## LE-REDIRECT example.com
    
    default_backend default


backend letsencrypt
    log global 
    mode http
    server letsencrypt 127.0.0.1:8080


backend default
    log     global
    mode http
    option tcplog

    server default 127.0.0.1:8000
```
