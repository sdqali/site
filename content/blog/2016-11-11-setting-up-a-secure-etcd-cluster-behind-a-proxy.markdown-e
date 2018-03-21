---
Categories:
- etcd
- development
Description: ""
Tags:
- etcd
- cluster
- coreos
- configuration
- proxy
- secure
- development
date: 2016-11-11T13:07:32-08:00
image: "images/etcd2-0.png"
keywords:
- etcd
- cluster
- coreos
- configuration
- proxy
- secure
title: Setting up a secure etcd cluster behind a proxy
---
This is a blog post that explains how to set up a highly available etcd cluster behind a proxy and securing the communication between a client and the proxy, between the proxy and the individual member in the cluster and between members in the cluster.
<!--more-->

CoreOS's etcd is

> ... a distributed key value store that provides a reliable way to store data across a cluster of machines. It’s open-source and available on GitHub. etcd gracefully handles leader elections during network partitions and will tolerate machine failure, including the leader.

It's highly available distributed nature makes it a great choice for storing application configuration. Kubernetes, for example uses etcd to store all it's API objects.

The proxy mode in etcd allows etcd to run as a transparent proxy for a cluster. This makes it possible to expose only the proxy to the clients and abstract away discovery and leader election away from the client. The client needs to know only about the proxy.

Communications to an etcd cluster and between members in a cluster can be secured through a PKI setup. Since an etcd proxy is in effect an etcd node that does not participate in leader election, communication between a client and a proxy can also be secured with similar infrastructure.

In this example, we will set up a cluster of 3 etcd nodes. We will use a key pair for the nodes and proxy to communicate between each other and another key pair for clients to communicate with the proxy.

![Diagram of a Secure Etcd Cluster with Proxy](/images/etcd-secure-cluster-proxy.svg "Secure Etcd Cluster with Proxy")

## Generating Keys
This section borrows heavily from Kelsey Hightower's [Kubernetes the Hard Way tutorial](https://github.com/kelseyhightower/kubernetes-the-hard-way). For the purposes of this blog post, we are going to assume that we will be running the three nodes and the proxy on a local machine. There will be changes that need to be made to the key configurations if these are deployed elsewhere. The instructions also assume that you are on OS X. Please make the necessary adjustments if you are on Linux.

### Install CloudFlare PKI toolkit
```bash
# Install the csffl utility
wget https://pkg.cfssl.org/R1.2/cfssl_darwin-amd64
chmod +x cfssl_darwin-amd64
sudo mv cfssl_darwin-amd64 /usr/local/bin/cfssl

# Install cfssljson utility
wget https://pkg.cfssl.org/R1.2/cfssljson_darwin-amd64
chmod +x cfssljson_darwin-amd64
sudo mv cfssljson_darwin-amd64 /usr/local/bin/cfssljson
```

### Create CA key and certificate
The first step will be to create a Certificate Authority configuration.
```bash
echo '{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "etcd-node": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "8760h"
      },
      "etcd-proxy": {
        "usages": ["signing", "key encipherment", "server auth", "client auth"],
        "expiry": "8760h"
      }
    }
  }
}' > ca-config.json
```
Here we are specifying two different profiles - one for the node key and one for the proxy key. We will then create a configuration for certificate signing request (CSR) for the CA key and certificate.
```bash
echo '{
  "CN": "Etcd",
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "San Francisco",
      "O": "Infra",
      "OU": "CA",
      "ST": "California"
    }
  ]
}' > ca-csr.json
```
Finally, we will generate the certificate and key.
```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```
This will generate the three files: `ca-key.pem` - private key for the CA, `ca.pem` - certificate for the CA and `ca.csr` - certificate signing request for the CA.

### Create Node certificate and key
Once we have the CA certificate and key in place, we can generate the TLS key for securing the communications between nodes and proxy. We will start by creating a configuration for this certificate. Since we are running everything locally, the hosts allowed to authenticate with this certificate include only `localhost`.
```bash
echo '{
  "CN": "etcd-node",
  "hosts": [
    "localhost",
    "0.0.0.0",
    "127.0.0.1"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "San Francisco",
      "O": "Infra",
      "OU": "Cluster",
      "ST": "California"
    }
  ]
}' > etcd-node-csr.json
```
Now we can generate the node certificate and key
```bash
cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=etcd-node \
  etcd-node-csr.json | cfssljson -bare etcd-node
```
This will create three files: `etcd-node.pem`- the node certificate, `etcd-node-key.pem` the key for this certificate and `etcd-node.csr` - the certificate signing request.
{{< mailchimp >}}
### Create Proxy certificate and key
We can now generate the TLS key for securing the communications between the client and the proxy. We will start by creating a configuration for this certificate. Since our client and proxy are running locally, the hosts allowed to authenticate with this certificate include only `localhost`.
```bash
echo '{
  "CN": "etcd-proxy",
  "hosts": [
    "localhost",
    "0.0.0.0",
    "127.0.0.1"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "San Francisco",
      "O": "Infra",
      "OU": "Cluster",
      "ST": "California"
    }
  ]
}' > etcd-proxy-csr.json
```
Now we can generate the proxy certificate and key
```bash
cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=etcd-proxy \
  etcd-proxy-csr.json | cfssljson -bare etcd-proxy
```
This will create three files: `etcd-proxy.pem`- the proxy certificate, `etcd-proxy-key.pem` the key for this certificate and `etcd-proxy.csr` - the certificate signing request.

## Running the nodes securely
Now that we have the certificates and keys, we will start the three nodes that form our etcd cluster. We will create three shell scripts that does this for us. In each of these, we will pass the appropriate parameters to etcd so that it uses the node certificate and key.
```bash
#script for node1
echo '#!/usr/bin/env sh

etcd \
--name='node1' \
--listen-client-urls='https://localhost:1179' \
--advertise-client-urls='https://localhost:1179' \
--listen-peer-urls='https://localhost:1180' \
--initial-advertise-peer-urls='https://localhost:1180' \
--initial-cluster='node1=https://localhost:1180,node2=https://localhost:1280,node3=https://localhost:1380' \
--initial-cluster-token='etcd-cluster-token' \
--initial-cluster-state='new' \
--cert-file=./etcd-node.pem \
--key-file=./etcd-node-key.pem \
--peer-cert-file=./etcd-node.pem \
--peer-key-file=./etcd-node-key.pem \
--trusted-ca-file=./ca.pem \
--peer-trusted-ca-file=./ca.pem \
--data-dir=./nodes/node1 \
--peer-client-cert-auth='true'
' > start-node1.sh

# script for node2
echo '#!/usr/bin/env sh

etcd \
--name='node2' \
--listen-client-urls='https://localhost:1279' \
--advertise-client-urls='https://localhost:1279' \
--listen-peer-urls='https://localhost:1280' \
--initial-advertise-peer-urls='https://localhost:1280' \
--initial-cluster='node1=https://localhost:1180,node2=https://localhost:1280,node3=https://localhost:1380' \
--initial-cluster-token='etcd-cluster-token' \
--initial-cluster-state='new' \
--cert-file=./etcd-node.pem \
--key-file=./etcd-node-key.pem \
--peer-cert-file=./etcd-node.pem \
--peer-key-file=./etcd-node-key.pem \
--trusted-ca-file=./ca.pem \
--peer-trusted-ca-file=./ca.pem \
--data-dir=./nodes/node2 \
--peer-client-cert-auth='true'
' > start-node2.sh

#script for node3
echo '#!/usr/bin/env sh

etcd \
--name='node3' \
--listen-client-urls='https://localhost:1379' \
--advertise-client-urls='https://localhost:1379' \
--listen-peer-urls='https://localhost:1380' \
--initial-advertise-peer-urls='https://localhost:1380' \
--initial-cluster='node1=https://localhost:1180,node2=https://localhost:1280,node3=https://localhost:1380' \
--initial-cluster-token='etcd-cluster-token' \
--initial-cluster-state='new' \
--cert-file=./etcd-node.pem \
--key-file=./etcd-node-key.pem \
--peer-cert-file=./etcd-node.pem \
--peer-key-file=./etcd-node-key.pem \
--trusted-ca-file=./ca.pem \
--peer-trusted-ca-file=./ca.pem \
--data-dir=./nodes/node3 \
--peer-client-cert-auth='true'
' > start-node3.sh

chmod +x ./start-node1.sh ./start-node2.sh ./start-node3.sh
```
Once these scripts are executed, we have an etcd cluster of three nodes. We can test that this cluster is started correctly with the right security using `etcdctl` client. For this purpose, we will be using the node certificate and key temporarily. We will also be assuming that we know what the individual nodes are. It is important to note that in our final configuration, the client will not have access to this certificate and key. It will have access only to the proxy key and there is no guarantee that the client knows what the individual nodes are.
```bash
$ etcdctl --cert-file=./etcd-node.pem  --key-file=./etcd-node-key.pem --ca-file=./ca.pem --endpoints=https://0.0.0.0:1179,https://0.0.0.0:1279,https://0.0.0.0:1379 cluster-health
member 5a68dbeefb870ed1 is healthy: got healthy result from https://localhost:1179
member 772c76fe731a3914 is healthy: got healthy result from https://localhost:1379
member aa3bff8d4d84db66 is healthy: got healthy result from https://localhost:1279
cluster is healthy
```

## Configuring the secure proxy
Once we have the cluster running, we can run the proxy. To secure it, we will tell etcd to use the etcd-node key for communicating with the nodes and to use the etcd-proxy certificate to accept connection from clients.
```bash
echo '#!/usr/bin/env sh

etcd \
    --name='proxy' \
     --proxy=on \
     --listen-client-urls https://localhost:2379 \
     --initial-cluster 'node1=https://localhost:1180,node2=https://localhost:1280,node3=https://localhost:1380' \
     --peer-cert-file=./etcd-node.pem \
     --peer-key-file=./etcd-node-key.pem \
     --peer-trusted-ca-file=./ca.pem \
     --peer-client-cert-auth='true' \
     --ca-file=./ca.pem \
     --cert-file=./etcd-proxy.pem \
     --key-file=./etcd-proxy-key.pem \
     --data-dir=./nodes/proxy
' > start-proxy.sh

chmod +x start-proxy.sh
```
Once we have the proxy running with these parameters, we can test that the cluster and the proxy is configured correctly. This time, we will be using only the proxy certificate and the proxy end point.
```bash
$ etcdctl --cert-file=./etcd-proxy.pem  --key-file=./etcd-proxy-key.pem --ca-file=./ca.pem --endpoints=https://0.0.0.0:2379 cluster-health
member 5a68dbeefb870ed1 is healthy: got healthy result from https://localhost:1179
member 772c76fe731a3914 is healthy: got healthy result from https://localhost:1379
member aa3bff8d4d84db66 is healthy: got healthy result from https://localhost:1279
cluster is healthy
```

This set up gives us a secure etcd cluster with a secure proxy in front of it. Communications between client and proxy, proxy and nodes and among nodes are all secured.
