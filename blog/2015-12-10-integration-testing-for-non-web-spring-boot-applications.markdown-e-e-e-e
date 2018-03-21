---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
- spring
date: 2015-12-10T21:45:59-05:00
title: Integration testing challenges for non-web Spring applications
image: "images/spring-by-pivotal.png"
---
We are building a command line data loader application at work that uses Spring. One of the things that I took us more time that it should have to figure out was how to write an integration test that invokes the command line application with the right command line arguments. This blog post describes this scenario and a potential solution to this problem.
<!--more-->

Let's consider a simple command line application implemented using Spring Boot's `CommandLineRunner`. The main application class is fairly simple.

```java

@Configuration
@EnableAutoConfiguration
@ComponentScan
public class Application implements CommandLineRunner {
    @Autowired
    DataService dataService;

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Override
    public void run(String... args) {
        dataService.perform(args[0]);
    }
}
```

In addition to this, there is a configuration class `AppConfiguration`.

```java
@Configuration
public class AppConfiguration {
    @Bean
    public DataService dataService() {
        return new DataService();
    }
}
```

The `DataService` simply prints the argument it receives.

```java
public class DataService {
    public void perform(String arg) {
        System.out.println(arg);
    }
}
```

If we were to attempt writing an integration test for this application, it would look like this:

```java
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = {Application.class})
public class ApplicationIntegrationTest {
    @Autowired
    private Application application;


    @Rule
    public OutputCapture outputCapture = new OutputCapture();

    @Test
    public void shouldGenerateResultFiles() throws Exception {
        application.run("sampleOutPut");
        assertTrue(outputCapture.toString().contains("sampleOutput"));
    }
}
```

That test is straightforward—it loads the Spring context with all the beans, runs the application with parameters and expects the parameter to be printed to the console.
{{< mailchimp >}}

Except, it does not work. If we were to execute the above test, we will get the following error:

```bash
...
Caused by: java.lang.ArrayIndexOutOfBoundsException: 0
at in.sdqali.springapps.Application.run(Application.java:24) ~[main/:na]
...
```

What happened? It looks like the `run` method was called with out any arguments while the test configuration was loaded.


Let‘s try and understand wh
y this happens. Remember how we annotated the test with `@SpringApplicationConfiguration`? This annotation is a meta-annotation [^1] specified as:

```java
@ContextConfiguration(loader = SpringApplicationContextLoader.class)
@Documented
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface SpringApplicationConfiguration {
...
}
```

`ContextConfiguration` is an annotation that allows tests to specify the information used to load and configure the application context. From the Java doc for this annotation:

```
 * {@code @ContextConfiguration} defines class-level metadata that is used to determine
 * how to load and configure an {@link org.springframework.context.ApplicationContext
 * ApplicationContext} for integration tests.
```

This brings us to `SpringApplicationContextLoader`‘s `loadContext` method and buried deep inside are these line:

```java
application.setInitializers(initializers);
ConfigurableApplicationContext applicationContext = application.run();
return applicationContext;
```

So, regardless of how many arguments our command line application was supposed to take, this loader always call the application without any arguments.


There are two solutions I have been able to think of for this problem:

* Override the`SpringApplicationContextLoader` and pass the necessary arguments in `application.run()`. This is definitely not an elegant or easy solution.
* Use an environment variable instead of the command line argument as the input to the service. This will allow us to inject this variable using the `@IntegrationTest` annotation.

My next blog post will discuss the second approach.

[^1]: Meta annotations. [Spring documentation](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/beans.html#beans-meta-annotations). To see how to use meta-annotations to write custom annoations, see [this blog post](/blog/2015/12/06/implementing-custom-annotations-for-spring-mvc/).
