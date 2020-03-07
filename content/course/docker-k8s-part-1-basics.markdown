---
title: "Docker + K8s Workshop - Setup for Part 1"
date: 2020-03-02T19:53:43-08:00
---
## Hello World

```
docker run hello-world
```

### Explanation

Docker containers are run time instances of images. Think of a Docker image as a set of files (like the set of files we placed in the jail directory in the chroot demo).

In this case, we are asking docker to create a container with the image `hello-world`.

The image has to come from somewhere. By default, Docker searches in a public repository of images hosted by Docker at docker.io.

It fetches the image and then creates a container from the image (file system)

### What is `latest`?

Docker convention uses `latest` to denote the very latest version of a particular image. This is just a convention - not all images have a version tagged `latest`.

By default, `docker run` tries to run the `latest` if no specific tag (version) is not specified.

### The second time

```
docker run docker.io/hello-world:latest
```

This time Docker did not have to download a new image because this is the same image as before.

### Image name

In `docker run docker.io/hello-world:latest`:

- Registry: `docker.io`
- Product/Service name `hello-world`
- Version `latest`

### Versioning

Versions can be denoted in any format:

Alpine:

```
docker run alpine:3.7 echo "Hello from Alpine"
```

OpenJDK 15:

```
docker run -it openjdk:15-slim-buster bash
```

## Creating a custom image from scratch.

We will build an image from the files we used for the chroot example.

- Download and unzip this [file]().
- Build the image in the directory using `docker build .`
- Run the container using `docker run <id> ./demo.sh`

## Creating a custom image from a Linux base.
