---
aliases:
- /blog/2012/06/05/managing-security-certificates-from-the-console-windows-mac-linux/
bbissueid: 78
categories:
- code
- ssl
- certificates
- console
- mac-osx
- windows
- linux
- development
- firefox
comments: true
date: 2012-06-05
ghissueid: 36
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- ssl
- certificates
- console
- mac-osx
- windows
- linux
- development
- firefox
title: Managing security certificates from the console - on Windows, Mac OS X and
  Linux
---

For me the last two weeks or so have involved a lot of wrestling with SSL certificates. One of the things that took some time to figure out was how to piggy-back on the tools provided by different Operating Systems to manage certificates. We did not want to rewrite [NSS](https://www.mozilla.org/projects/security/pki/nss/ "NSS"). Luckily for us, all the major OSes provide tools to manage certificates from the command line.

<!--more-->

## Windows
----
Windows provides two ways to deal with certificates from the command line - [Certutil](http://technet.microsoft.com/en-us/library/cc732443%28WS.10%29.aspx "Certutil") and [certmgr.exe](http://msdn.microsoft.com/en-us/library/e78byta0.aspx "certmgr.exe"). We decided to go with Certutil because it is present out of the box on Windows 7 and Windows Server 2008, while certmgr.exe is part of the .Net runtime. This blog post will deal with Certutil.

### Adding a certificate
```bash
certutil.exe -addstore -user root foo.crt
```

This will install the `foo.crt` certificate to the Trusted Root Certification Authorities store for the current user.

### View certificates in a store
```bash
certutil.exe -viewstore -user root
```

This will list all the certificates in the Trusted Root Certification Authorities store for the current user. One drawback is that it throws up a Window to list as opposed to using STDOUT for output.

### List certificates in a store
```bash
certutil.exe -user -store root
```

This will list all the certificates in the Trusted Root Certification Authorities store for the current user to STDOUT.

There are more detailed explanations [here](http://technet.microsoft.com/en-us/library/cc772898\(WS.10\).aspx).

## Mac OS X
----
Mac OS X ships the [security](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/Manpages/man1/security.1.html) tool to let the user manage certificates and keychains.

### Adding a certificate
```bash
security add-certificate foo.crt
security add-trusted-cert foo.crt
```

The first line will add `foo.crt` to the current user's keychain, while the second line ensures that the newly added certificate is trusted. This would mean that the certificate will be trusted for SSL, EAP and Code Signing. To get more fine grained control over what to trust the certificate for, the `-p (policy)` flag can be used.
```bash
security add-trusted-cert -p ssl foo.crt
```

This will trust the certificate only for SSL interactions.

### Listing certificates
```bash
security find-certificates -a -e foo@bar.com
```

This would list all the certificates where e-mail address of the issuer `foo@bar.com`. Other fields that can be used for matching include `-c (name)`.

## Linux
----
On Linux, the best we could find was [certutil](http://www.mozilla.org/projects/security/pki/nss/tools/certutil.html certutil) which is part of Mozilla's NSS project.

### Adding a certificate
```bash
certutil -A -d sql:~/.pki/nssdb -t C -n "Certificate Common Name" -i foo.crt
```

This will add `foo.crt` to the certificate database `~/.pki/nssdb`. This is where applications like Chromium look for certificates.

### Listing certificates
```bash
certutil -L -d sql:~/.pki/nssdb -n "Certificate Common Name"
```

This will list the certificates in the `~/.pki/nssdb` with the common name "Certificate Common Name".

## Firefox
----
While the above steps work fine for pretty much all applications on the three OSes, Firefox does things in it's own way. Firefox implements [NSS](https://www.mozilla.org/projects/security/pki/nss/ NSS) and hence does not look at the certificates the OS knows about. One solution to manage certificates from the command line will be to install certutil and point it at the `cert.db` certificate database in your Firefox profile directory. Alternatively, one could do the following

1. Launch Firefox with a blank profile
* Accept the certificates we are interested in.
* Save a copy of the `cert8.db` file.
* Import this database to the profiles we wish to run Firefox on.

While copying the database is not as clean a solution as using certutil, we decided to go with the second option because there is no guarantee that certutil will be present on the user's box, especially if they are running Windows or Mac OS X. And we had a fairly high control over the Firefox profiles.