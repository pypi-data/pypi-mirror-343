# The simple dns.he.net certbot plugin

This certbot plugin allows you to validate ACME challenges against dns.he.net.
Unlike earlier plugins, this does not require access to your username/password,
but only to the DDNS key for the record(s) to validate. This follows the
principle of least privilege and prevents unwanted modifications to your zone.

## Usage

Manually create a `_acme-challenge` TXT record and set a DDNS key.

1. log in at https://dns.he.net and navigate to the zone in question
2. create a new TXT record for each (sub)domain to validate:
   * Name: e.g. `_acme-challenge.subdomain.example.com`
   * Text: (empty; doesn't matter)
   * TTL: 5 minutes
   * check *Enable entry for dynamic dns*
3. click the circling arrows to generate a DDNS key for each of the added
   records. if you want a single certificate with multiple domain names, you
   must use the same key for all these records. You can use `pwgen -s 64` to
   generate good random tokens.

Then invoke certbot with `--authenticator dns-he-simple --dns-he-simple-key
$your_ddns_key`. You can also add the following to `/etc/letsencrypt/cli.ini`
instead:

```
authenticator=dns-he-simple
dns-he-simple-key=$your_ddns_key
```

## Copyright

Copyright (c) 2025, Tobias Girstmair <tobi@isticktoit.net>. [permissively
licensed](LICENSE).
