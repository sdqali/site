---
title: Command line clients for gRPC - 1
date: 2018-04-03T22:40:08-07:00
draft: true
tags:
  - grpc
---
We are in the middle of considering replacing JSON over HTTP with gRPC for communication between our internal services. One of my concerns about this was how we would be able to debug and poke around things in a world where we will no longer be able to use cURL. I have been looking at cURL like command line utilities we can use to replace most of the capabilities, if not all of cURL. So far, I have looked at [grpcurl](https://github.com/fullstorydev/grpcurl), [grpc_cli](https://github.com/grpc/grpc/blob/master/doc/command_line_tool.md) and [polyglot](https://github.com/grpc-ecosystem/polyglot) .In these blog posts, we will try and compare these tools.
<!--more-->

In this example, we will be running the example implementations provided by the [grpc-java](https://github.com/grpc/grpc-java/tree/master/examples) project and using the command line tools against the services from these examples. We will also be running these services without enabling reflection.

## grpcurl
One of the things that immediately struck me when I started looking at grpcurl was how neat it's command line interface was, especially in comparison with that of polyglot. grpcurl is written in Go and expects you to provide `protoset` files that contain service descriptors exported from the `proto` files of the service.

For example, for the `hello-world` service from the examples, the `protoset` files can be generated using:

```bash
> pwd
grpc-java/examples/src/main/proto
> protoc --proto_path=./ \
    --descriptor_set_out=helloworld.protoset \
    --include_imports \
    ./helloworld.proto
```

This will produce a `protoset` file named `helloworld.protoset`. Using this, we can now list the services available:

```bash
> grpcurl -protoset ./helloworld.protoset list
helloworld.Greeter
```

We can also list all the methods available in a service:

```bash
> grpcurl -protoset ./helloworld.protoset list helloworld.Greeter
SayHello
```

There is also a describe command that produces description of a service:

```bash
> grpcurl -protoset ./helloworld.protoset describe helloworld.Greeter
helloworld.Greeter is a service:
{
  "name": "Greeter",
  "method": [
    {
      "name": "SayHello",
      "inputType": ".helloworld.HelloRequest",
      "outputType": ".helloworld.HelloReply",
      "options": {

      }
    }
  ],
  "options": {

  }
}
```

Now we can execute the method on this service running on a server by specifying the address and the path to the method:

```bash
> grpcurl -plaintext -protoset ./helloworld.protoset -d '{"name":"World"}' localhost:50051 helloworld.Greeter/SayHello
{
  "message": "Hello World"
}
```

It can also read the JSON data to pass to the server from STDIN, by setting the value of `-d` to `@`:

```bash
> echo '{"name": "World"}' | grpcurl -plaintext -protoset ./helloworld.protoset -d @ localhost:50051 helloworld.Greeter/SayHello
{
  "message": "Hello World"
}
```

In both these examples, we passed the `-plaintext` switch because our server is not running with TLS. 

If we were to [turn on reflection](https://github.com/grpc/grpc-java/blob/master/documentation/server-reflection-tutorial.md), we will no longer need to depend on the `protoset` file. 

```bash
> echo '{"name": "World"}' | grpcurl -plaintext -d @ localhost:50051 helloworld.Greeter/SayHello
{
  "message": "Hello World"
}
```

Overall, I like what the creator of grpcurl have done. The only thing I dont like is the fact that when reflection is turned off, we have to generate `protoset` files. It would have been great if it could just look at the existing `proto` files, which is what `polyglot` does. We will look at polyglot in the next blog post.
