---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
date: 2016-04-17T23:36:48-04:00
title: Programmable exit codes for Spring command line applications
image: "images/spring-by-pivotal.png"
---
Spring's `CommandLineRunner` provides a great mechanism to build command line applications. While this convenience is great, applications that use `CommandLineRunner` require extra effort in some areas like integration testing. Exit codes are such an area - applications that use command line runners always report their exit code as `0` even if there are exceptions thrown. This blog post explains a way to get to programmable exit codes for such applications.

<!--more-->

The following example demonstrates this problem. Here we have a simple implementation of `CommandLineRunner` that simply throws a `RuntimeException` when started.
```java
@Component
@Profile("exception")
public class WillThrow implements CommandLineRunner {
    public void run(String... args) throws Exception {
        throw new RuntimeException("This should kill the application");
    }
}

```
When this application runs, we will see that the exit code is `0`, as expected.

```
$ java -Dspring.profiles.active=exception -jar build/libs/exit-code-demo-1.0-SNAPSHOT.jar >> /dev/null 2&>1
$ echo $?
0
```

A simple way to propagate the right exit code is to use `java.lang.System#exit` and specify an error code. The following snippet shows this:

```java
@Component
@Profile("exit")
public class WillExit implements CommandLineRunner {
    public void run(String... args) throws Exception {
        System.exit(3);
    }
}
```

When run:

```
$ java -Dspring.profiles.active=exit -jar build/libs/exit-code-demo-1.0-SNAPSHOT.jar >> /dev/null 2&>1
$ echo $?
3
```

This looks straightforward and easy. However, exiting the application from within the `CommandLineRunner` makes integration testing of this application difficult. Our tests will simply stop execution at that point without giving us the opportunity to assert anything.
{{< mailchimp >}}

At work, while looking for a solution to this, we stumbled across Spring's `ExitCodeGenerator` [^1]. It is an interface whose implementations Spring uses to look up what exit code to use. There are at least two ways to make use of `ExitCodeGenerator` - one involves making the application's Exceptions implement `ExitCodeGenerator` and the other involves making the command line runners themselves implement `ExitCodeGenerator`. We will look at the first approach here.

Our new command line runner will be as:

```java
@Component
@Profile("exception")
public class WillThrow implements CommandLineRunner{
    public void run(String... args) throws Exception {
        throw new ExceptionWithExitCode("Hello");
    }
}
```
And the exception will resemble:

```java
public class ExceptionWithExitCode extends RuntimeException implements ExitCodeGenerator {
    public ExceptionWithExitCode(String message) {
        super(message);
    }

    public int getExitCode() {
        return 13;
    }
}

```

When the application runs:

```
$ java -Dspring.profiles.active=exception -jar build/libs/exit-code-demo-1.0-SNAPSHOT.jar >> /dev/null 2&>1
$ echo $?
13
```

Obviously, this is a rather simple example, but you can see how `ExitCodeGenerator` allows us to have programmable exit codes. This allows us to have tests for our applications, while giving us the flexibility to control the exit code.

We will take a look at the second approach of using `ExitCodeGenerator` in another blog post.

[^1]: `ExitCodeGenerator` is an "Interface used to generate an 'exit code' from a running command line SpringApplication.". You can find the JavaDocs [here](http://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/ExitCodeGenerator.html).
