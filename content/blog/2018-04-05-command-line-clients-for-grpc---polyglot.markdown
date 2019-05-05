---
date: 2018-04-06 05:45:08
aliases:
- /blog/2018/04/05/command-line-clients-for-grpc-polyglot/
ghcommentid: 136
tags:
- grpc
- grpcurl
- polyglot
title: Command line clients for gRPC - polyglot
---

Polyglot was the second gRPC client that I looked at. One of the things that I liked about it is the fact that it does not need users to generate `protoset` files. It generates the protoset files in flight every time it runs. This, combined with the fact that it is written in Java does have a disadvantage - every time the client makes a call, it has to fire up a JVM, generate protosets and make the request.

<!--more-->

You run polyglot by using the distributed polyglot jar. To list all the services available on an endpoint, polyglot can be executed as:
```bash
> java -jar ~/Downloads/polyglot.jar --command=list_services \
  --proto_discovery_root=$PROTO_DISCOVERY_ROOT \
  --deadline_ms=3000
[main] INFO me.dinowernli.grpc.polyglot.Main - Polyglot version: 1.6.0
[main] INFO me.dinowernli.grpc.polyglot.Main - Loaded configuration:

manualflowcontrol.StreamingGreeter -> /Users/sdqali/src/grpc/grpc-java/examples/src/proto/hello_streaming.proto
manualflowcontrol.StreamingGreeter/SayHelloStreaming

routeguide.RouteGuide -> /Users/sdqali/src/grpc/grpc-java/examples/src/proto/route_guide.proto
routeguide.RouteGuide/GetFeature
routeguide.RouteGuide/ListFeatures
routeguide.RouteGuide/RecordRoute
routeguide.RouteGuide/RouteChat

helloworld.Greeter -> /Users/sdqali/src/grpc/grpc-java/examples/src/proto/helloworld.proto
helloworld.Greeter/SayHello
```

The command `call` can be issued to execute a particular service method:
```bash
echo "{'name': 'World'}" | java -jar ~/Downloads/polyglot.jar --command=call \
  --full_method=helloworld.Greeter/SayHello \
  --endpoint=localhost:50051 \
  --proto_discovery_root=$PROTO_DISCOVERY_ROOT \
  --deadline_ms=3000
[main] INFO me.dinowernli.grpc.polyglot.Main - Polyglot version: 1.6.0
[main] INFO me.dinowernli.grpc.polyglot.Main - Loaded configuration:
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Creating channel to: localhost:50051
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Using proto descriptors obtained from protoc
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Creating dynamic grpc client
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Making rpc with 1 request(s) to endpoint [localhost:50051]
[main] INFO me.dinowernli.grpc.polyglot.grpc.DynamicGrpcClient - Making unary call
[grpc-default-executor-0] INFO me.dinowernli.grpc.polyglot.io.LoggingStatsWriter - Got response message
{
"message": "Hello World"
}

[grpc-default-executor-0] INFO me.dinowernli.grpc.polyglot.io.LoggingStatsWriter - Completed rpc with 1 response(s)
```
Notice how we are passing path to proto files and polyglot executes `protoc` on them to get protosets.
With reflection turned ON, we no longer need to provide a path to the proto files.

```bash
echo "{'name': 'World'}" | java -jar ~/Downloads/polyglot.jar --command=call \
  --full_method=helloworld.Greeter/SayHello \
  --endpoint=localhost:50051 \
  --deadline_ms=3000 \
  --use_reflection=true
[main] INFO me.dinowernli.grpc.polyglot.Main - Polyglot version: 1.6.0
[main] INFO me.dinowernli.grpc.polyglot.Main - Loaded configuration:
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Creating channel to: localhost:50051
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Using proto descriptors fetched by reflection
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Creating dynamic grpc client
[main] INFO me.dinowernli.grpc.polyglot.command.ServiceCall - Making rpc with 1 request(s) to endpoint [localhost:50051]
[main] INFO me.dinowernli.grpc.polyglot.grpc.DynamicGrpcClient - Making unary call
[grpc-default-executor-0] INFO me.dinowernli.grpc.polyglot.io.LoggingStatsWriter - Got response message
{
"message": "Hello World"
}
```

That is nice, except that reflection does not work for listing services.

```bash
java -jar ~/Downloads/polyglot.jar --command=list_services \
  --endpoint=localhost:50051 \
  --deadline_ms=3000 \
  --use_reflection=true
[main] INFO me.dinowernli.grpc.polyglot.Main - Polyglot version: 1.6.0
[main] INFO me.dinowernli.grpc.polyglot.Main - Loaded configuration:
[main] WARN me.dinowernli.grpc.polyglot.Main - Caught top-level exception during command execution
java.lang.IllegalArgumentException: A proto discovery root is required for proto analysis
  at com.google.common.base.Preconditions.checkArgument(Preconditions.java:122)
  at me.dinowernli.grpc.polyglot.protobuf.ProtocInvoker.forConfig(ProtocInvoker.java:36)
  at me.dinowernli.grpc.polyglot.Main.getFileDescriptorSet(Main.java:93)
  at me.dinowernli.grpc.polyglot.Main.main(Main.java:62)
Exception in thread "main" java.lang.RuntimeException: java.lang.IllegalArgumentException: A proto discovery root is required for proto analysis
  at me.dinowernli.grpc.polyglot.Main.main(Main.java:86)
Caused by: java.lang.IllegalArgumentException: A proto discovery root is required for proto analysis
  at com.google.common.base.Preconditions.checkArgument(Preconditions.java:122)
  at me.dinowernli.grpc.polyglot.protobuf.ProtocInvoker.forConfig(ProtocInvoker.java:36)
  at me.dinowernli.grpc.polyglot.Main.getFileDescriptorSet(Main.java:93)
  at me.dinowernli.grpc.polyglot.Main.main(Main.java:62)
```
This was unexpected, as adding this capability to Polyglot should not be too diffcult, considering that they already support reflection for executing services. This is something that I am interested in implementing.
