---
Categories:
- java
- docker
- kubernetes
Description: ""
keywords:
- java
- docker
- kubernetes
- spring
- spring boot
Tags:
- java
- docker
- kubernetes
date: 2016-11-04T22:34:53-07:00
image: "img/KubernetesLogo.png"
title: A very basic introduction to deploying a Java application using Kubernetes
---

I have been playing around with Kubernetes and Docker lately. To borrow the description of Kubernetes from their website,

> "Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications."

One of the first things I did was to try and see what it would take to go from an application to deploying it. I started with a simple Java application and had to set up the development environment. These are my notes from this process. This assumes that you have docker installed on your development environment.

## Install minikube
[Minikube](https://github.com/kubernetes/minikube) is a tool that makes it easy to run Kubernetes for local development. To run minikube, you need to have a virtualizer installed - in my case I already had VirtualBox installed. Instructions for installing minikube is available [here](https://github.com/kubernetes/minikube/releases). In my case, this is what I did:
```
> curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.12.2/minikube-darwin-amd64
> chmod +x minikube
> sudo mv minikube /usr/local/bin/
```

## Install kubectl
[Kubectl](http://kubernetes.io/docs/user-guide/kubectl-overview/) is a command line application that executes commands against Kubernets clusters. Instructions for installing kubectl are available [here](http://kubernetes.io/docs/getting-started-guides/minikube/#install-kubectl).
```
> curl -Lo kubectl http://storage.googleapis.com/kubernetes-release/release/v1.3.0/bin/darwin/amd64/kubectl
> chmod +x kubectl
> sudo mv kubectl /usr/local/bin/
```

## Set up a Docker repository
Kubernetes pulls container images from publicly available registries. But because we are building an application that we will not be publishing to public docker registries, we need to create a local registry. There is a great write up on how to set up a local docker registry at [Newstack](http://thenewstack.io/tutorial-configuring-ultimate-development-environment-kubernetes/).

## Start minikube with the registry
Now that we have a local docker registry, we can go ahead and tell minikube to consume images from this registry. However, if you have started a minikube cluster previously, the registry override will not be available to it unless it is deleted.
```
> docker-machine ip registry
192.168.99.100
> minikube stop
> minikube delete
> minikube start --vm-driver="virtualbox" --insecure-registry=192.168.99.100:80
```
{{< mailchimp >}}
## Create a container image for the application
The application in this case is a simple Spring Boot application that has exactly one controller.
```java
@RestController
public class HelloController {
  @RequestMapping("/hello")
  public Map hello() {
    return singletonMap("message", "hello");
  }
}
```
In order to create a docker container from this application, we will use the [Maven Docker Plugin](https://github.com/spotify/docker-maven-plugin). We will need to set a prefix for our docker image. This can be done with this maven property:
```
<docker.image.prefix>sadiqueio</docker.image.prefix>
```
Th plugin expects a `Dockerfile` to be present in the `src/main/docker` directory. Our `Dockerfile` will look like this:
```
FROM frolvlad/alpine-oraclejdk8:slim
ADD hello-world-0.0.1-SNAPSHOT.jar app.jar
RUN sh -c 'touch /app.jar'
ENTRYPOINT ["java","-jar","/app.jar"]
```
With this in place, we can generate a docker image. We need to ensure that we are looking at the dev docker host.
```
> eval $(docker-machine env dev)
> mvn package docker:build
```

## Tag and push the image to local registry
The generated image `sadiqueio/hello-world` need to be published to the local registry we created.
```
> docker tag sadiqueio/hello-world 192.168.99.100:80/hello-world
> docker push 192.168.99.100:80/hello-world
```

## Define and create a service
We will define a Kubernetes service object for this application `hello-world-service.yaml`:
```
apiVersion: v1
kind: Service
metadata:
  name: hello-world
  labels:
    app: hello-world
    tier: backend
spec:
  type: NodePort
  ports:
    # the port that this service should serve on
  - port: 8080
  selector:
    app: hello-world
    tier: backend
```

The service can be created using:
```
> kubectl create -f hello-world-service.yaml
You have exposed your service on an external port on all nodes in your
cluster.  If you want to expose this service to the external internet, you may
need to set up firewall rules for the service port(s) (tcp:30194) to serve traffic.

See http://releases.k8s.io/release-1.3/docs/user-guide/services-firewalls.md for more details.
service "hello-world" created
```
Make a note of the port assigned to this service. We will use this port later to access our application.

## Define and create a deployment
The next step is to define and create a deployment for our application. This is where we specify the image we previously created and published to the registry.
```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello-world
        tier: backend
    spec:
      containers:
      - name: hello-world
        image: 192.168.99.100:80/hello-world
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        env:
        - name: GET_HOSTS_FROM
          value: dns
        ports:
        - containerPort: 8080
```

```
> kubectl create -f hello-world-deployment.yaml
deployment "hello-world" created
```

## Ensure that the deployment is successful
```
> kubectl get services
NAME          CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
hello-world   10.0.0.252   <none>        8080/TCP   4m
> kubectl get deployments
NAME          DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
hello-world   1         1         1            1           4m
```

## Access the service
We already know the port assigned to our service. Because we specified `type: NodePort`, the IP address we need to use is that of the Kubernetes cluster. This IP address can be found using the minikube command.
```
> minikube ip
192.168.99.102
```
Now that we have both pieces of information, we can test that our application is up.
```
> curl  -s http://192.168.99.102:30194/hello | jq .
{
  "message": "hello"
}
```
That is it. We have deployed our hello world application using Kubernetes.
