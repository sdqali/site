---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
date: 2016-04-19T22:29:12-04:00
title: Programmable exit codes for spring command line applications - 2
image: "images/spring-by-pivotal.png"
---
In the last [blog post](/blog/2016/04/17/programmable-exit-codes-for-spring-command-line-applications/), we took a look at how to implement programmable exit codes for spring command line applications by using exceptions that implement `ExitCodeGenerator`. This time, we will take a look at how to achieve the same without having to depend on an exception.

<!--more-->

This approach depends on the command line runner implementing the `ExitCodeGenerator`. This does require the usage of `System.exit`, but instead of it being invoked from different command line runners, it will be used in a single place as follows:

```java
public class Application  {
    public static void main(String[] args) {
        ConfigurableApplicationContext ctx = SpringApplication.run(Application.class, args);
        System.exit(SpringApplication.exit(ctx));
    }
}
```
The command line runner will now implement `ExitCodeGenerator`:
{{< mailchimp >}}

```java
@Component
@Profile("hello")
public class HelloWorld implements CommandLineRunner, ExitCodeGenerator {

    public void run(String... args) throws Exception {
        System.out.println("Hello World!");
    }

    public int getExitCode() {
        return 45;
    }
}
```
This is how the application behaves when run:

```bash
$ java -Dspring.profiles.active=hello -jar build/libs/exit-code-demo-1.0-SNAPSHOT.jar > /dev/null 2>&1
$ echo $?
45
```

This allows us to delegate how the application should exit to the command line runners themselves, without having to throw exceptions.
