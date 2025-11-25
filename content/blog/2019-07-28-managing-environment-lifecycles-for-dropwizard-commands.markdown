---
title: Managing environment lifecycles for Dropwizard Commands
date: 2019-07-28T18:29:49-07:00
ghissueid: 144
bbissueid: 137
tags:
- java
- dropwizard
---
If you have built background workers or other non-server applications with Dropwizard, chances are that you used the Dropwizard Command pattern. In fact, even the sever you wrote with Dropwizard executes a command - specifically `io.dropwizard.cli.ServerCommand`. While the server command is great, sometimes you want to build applications that have all the goodies that Dropwizard offers, but you dont want to start a server. Managing Lifecycles is one example of a Dropwizard feature that works great for server applications, but needs some tweaking to get working for non-server commands.

<!--more-->

Let's take the following example. We have the simplest Dropwizard command below. It doesn't do much, except print some logs and sleep for a second in between.

```java
public class WaitingCommand extends EnvironmentCommand<AppConfiguration> {

  public WaitingCommand(Application<AppConfiguration> application) {
    super(application, "wait", "Wait for a second.");
  }

  @Override
  protected void run(Environment environment, Namespace namespace, AppConfiguration configuration) throws Exception {
    Logger.getInstance(getClass()).info("Starting command");
    try {
      Thread.sleep(1000);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    Logger.getInstance(getClass()).info("Finished running command");
  }
}
```

We can wire this to our application.

```java
public class MetricsApplication extends Application<AppConfiguration> {
  public static void main(String[] args) throws Exception {
    new MetricsApplication().run(args);
  }

  @Override
  public void run(AppConfiguration configuration, Environment environment) throws Exception {

  }

  @Override
  public void initialize(Bootstrap<AppConfiguration> bootstrap) {
    bootstrap.addCommand(new WaitingCommand(this));

    bootstrap.setConfigurationSourceProvider(new ResourceConfigurationSourceProvider());
  }
}
```

When our application runs with the `wait` command (i.e. we invoke it as `java -jar app.jar wait config.yml`), it does the little work we asked it to do.

```
INFO  [2019-07-29 01:42:43,703] org.eclipse.jetty.util.log: Logging initialized @2699ms to org.eclipse.jetty.util.log.Slf4jLog
INFO  [2019-07-29 01:42:43,952] io.dropwizard.server.DefaultServerFactory: Registering jersey handler with root path prefix: /
INFO  [2019-07-29 01:42:43,957] io.dropwizard.server.DefaultServerFactory: Registering admin handler with root path prefix: /
INFO  [2019-07-29 01:42:43,960] io.sadique.dropwizard.WaitingCommand: Starting command
INFO  [2019-07-29 01:42:44,966] io.sadique.dropwizard.WaitingCommand: Finished running command
```

## Adding a lifecycle
Let's try adding an object whose lifecycle we intend to be managed by Dropwizard. Again, this entity in the example doesn't do much - except log when it is started and stopped by Dropwizard.

```java
import io.dropwizard.lifecycle.Managed;
import org.apache.log4j.Logger;

public class ManagedObject implements Managed {
  @Override
  public void start() throws Exception {
    Logger.getInstance(getClass()).info("Starting managed object");
  }

  @Override
  public void stop() throws Exception {
    Logger.getInstance(getClass()).info("Stopping managed object");
  }
}
```

We will of course need to tell Dropwizard to manage this object:

```java

  @Override
  public void run(AppConfiguration configuration, Environment environment) throws Exception {
    environment.lifecycle().manage(new ManagedObject());
  }
```

When the application is run with the `wait` command, the log looks like:

```
INFO  [2019-07-29 01:50:28,510] org.eclipse.jetty.util.log: Logging initialized @1640ms to org.eclipse.jetty.util.log.Slf4jLog
INFO  [2019-07-29 01:50:28,640] io.dropwizard.server.DefaultServerFactory: Registering jersey handler with root path prefix: /
INFO  [2019-07-29 01:50:28,642] io.dropwizard.server.DefaultServerFactory: Registering admin handler with root path prefix: /
INFO  [2019-07-29 01:50:28,647] io.sadique.dropwizard.WaitingCommand: Starting command
INFO  [2019-07-29 01:50:29,649] io.sadique.dropwizard.WaitingCommand: Finished running command
```

Looks like the object we expected Dropwizard to start and stop was ignored. What if we run the application with the `server` command?

```
INFO  [2019-07-29 02:09:17,067] org.eclipse.jetty.setuid.SetUIDListener: Opened application@680a66dd{HTTP/1.1,[http/1.1]}{0.0.0.0:8080}
INFO  [2019-07-29 02:09:17,067] org.eclipse.jetty.setuid.SetUIDListener: Opened admin@2dd8239{HTTP/1.1,[http/1.1]}{0.0.0.0:8081}
INFO  [2019-07-29 02:09:17,126] org.eclipse.jetty.server.Server: jetty-9.4.z-SNAPSHOT
INFO  [2019-07-29 02:09:17,143] io.sadique.dropwizard.ManagedObject: Starting managed object
...
...
...
INFO  [2019-07-29 02:09:21,747] org.eclipse.jetty.server.AbstractConnector: Stopped admin@2dd8239{HTTP/1.1,[http/1.1]}{0.0.0.0:8081}
INFO  [2019-07-29 02:09:21,751] org.eclipse.jetty.server.handler.ContextHandler: Stopped i.d.j.MutableServletContextHandler@2ee83775{/,null,UNAVAILABLE}
INFO  [2019-07-29 02:09:21,756] org.eclipse.jetty.server.handler.ContextHandler: Stopped i.d.j.MutableServletContextHandler@19382338{/,null,UNAVAILABLE}
INFO  [2019-07-29 02:09:21,760] io.sadique.dropwizard.ManagedObject: Stopping managed object
```

The server seems to manage the lifecycle of the object as expected. Why is it the case that server command can manage the lifecycle, but our custom command can't?

It turns out, it is not enough to register an entity whose lifecycle needs to be managed, someone needs to attach a lifecycle container to the `LifecycleEnvironment`. It is not an issue for the server command because it builds a server using `io.dropwizard.server.AbstractServerFactory#buildServer`, which in turn [attaches the container](https://github.com/dropwizard/dropwizard/blob/master/dropwizard-core/src/main/java/io/dropwizard/server/AbstractServerFactory.java#L611).

## Building a LifecycleManagedCommand
We can mimic the behavior of the server by constructing our own `ContainerLifecycle` and starting it before our command performs it's actions. This pattern can be generalized as a `LifecycleManagedCommand`.

```java
public abstract class LifecycleManagedCommand<T extends Configuration> extends EnvironmentCommand<T> {

  private final ContainerLifeCycle containerLifeCycle;

  public LifecycleManagedCommand(Application<T> application, String name, String description) {
    super(application, name, description);
    containerLifeCycle = new ContainerLifeCycle();
  }

  @Override
  protected void run(Environment environment, Namespace namespace, T configuration) throws Exception {
    environment.lifecycle().getManagedObjects().stream().forEach(mo -> containerLifeCycle.addBean(mo));
    ShutdownThread.register(containerLifeCycle);
    containerLifeCycle.start();

    runManaged(environment, namespace, configuration);

    containerLifeCycle.stop();
  }

  abstract void runManaged(Environment environment, Namespace namespace, T configuration);
}
```

This command ensures that:

- A new `ContainerLifeCycle` is built before running the command.
- Every managed object registered with the Lifecycle is added to the container.
- The container is started and registered with `ShutdownThread`, which is Dropwizard's shut down hook.
- The container is stopped after the command performs it's action.

We can now now modify `WaitCommand` to use this pattern.

```
public class WaitingCommand extends LifecycleManagedCommand<AppConfiguration> {

  public WaitingCommand(Application<AppConfiguration> application) {
    super(application, "wait", "Wait for a second.");
  }

  @Override
  protected void runManaged(Environment environment, Namespace namespace, AppConfiguration configuration) {
    Logger.getInstance(getClass()).info("Starting command");
    try {
      Thread.sleep(1000);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    Logger.getInstance(getClass()).info("Finished running command");
  }
}
```

With this change, we can see that Dropwizard correctly handles the lifecycle when the `wait` command is executed.

```
INFO  [2019-07-29 02:26:34,560] io.dropwizard.server.DefaultServerFactory: Registering jersey handler with root path prefix: /
INFO  [2019-07-29 02:26:34,563] io.dropwizard.server.DefaultServerFactory: Registering admin handler with root path prefix: /
INFO  [2019-07-29 02:26:34,569] io.sadique.dropwizard.ManagedObject: Starting managed object
INFO  [2019-07-29 02:26:34,569] io.sadique.dropwizard.WaitingCommand: Starting command
INFO  [2019-07-29 02:26:35,575] io.sadique.dropwizard.WaitingCommand: Finished running command
INFO  [2019-07-29 02:26:35,575] io.sadique.dropwizard.ManagedObject: Stopping managed object
```

The server command will of course continue to work as expected.

