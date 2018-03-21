---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
date: 2015-12-11T15:57:30-05:00
title: Integration testing Spring command line applications
image: "images/spring-by-pivotal.png"
---
In the [last blog post](/blog/2015/12/10/integration-testing-challenges-for-non-web-spring-applications/), I wrote about the challenges of writing an integration test for a Spring command line application. One of the solutions for this issue discussed in the blog post was to use the `@IntegrationTest` annotations to inject Java system properties and use that to run the application instead of the normal command line arguments. This blog post describes how to perform this.
<!--more-->
The first step is to rewrite our test to use the `@IntegrationTest` annotations. This will result in a test that looks as follows:

```java
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = {Application.class})
@IntegrationTest(value = "input:expectedOutput")
public class ApplicationIntegrationTest {
    @Autowired
    private Application application;

    @Rule
    public OutputCapture outputCapture = new OutputCapture();

    @Test
    public void shouldGenerateResultFiles() throws Exception {
        application.run();
        assertTrue(outputCapture.toString().contains("expectedOutput"));
    }
}
```

At this point, it is worth taking a look at what the `@IntegrationTest` annotation causes Spring to do. This is a meta-annotation [^1] that specifies a number of test listeners including `IntegrationTestPropertiesListener`.

```java
@Documented
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@TestExecutionListeners(listeners = { IntegrationTestPropertiesListener.class,
        DirtiesContextBeforeModesTestExecutionListener.class,
        DependencyInjectionTestExecutionListener.class,
        DirtiesContextTestExecutionListener.class,
        TransactionalTestExecutionListener.class, SqlScriptsTestExecutionListener.class })
public @interface IntegrationTest {
    String[] value() default {};
}
```

`IntegrationTestPropertiesListener` is an implementation of `TestExecutionListener` which is a mechanism used by Spring to react to test execution events like `beforeTestClass`, `prepareTestInstance`, `beforeTestMethod`, `beforeTestMethod` and `afterTestClass`.

For the purposes of what we are trying to achieve, the listener we are really interested in is the `beforeTestClass` of `IntegrationTestPropertiesListener`.

```java
    @Override
    public void prepareTestInstance(TestContext testContext) throws Exception {
        Class<?> testClass = testContext.getTestClass();
        AnnotationAttributes annotationAttributes = AnnotatedElementUtils
                .getMergedAnnotationAttributes(testClass,
                        IntegrationTest.class.getName());
        if (annotationAttributes != null) {
            addPropertySourceProperties(testContext,
                    annotationAttributes.getStringArray("value"));
        }
    }
```

As we can see, the value of the `value` element [^2] of our `@IntegrationTest` gets injected to the configuration of the test context.
{{< mailchimp >}}

Now that we have understood and used the `@IntegrationTest` annotation to push in configuration, it is time to make our application consume this configuration.


```java
@Configuration
@EnableAutoConfiguration
@ComponentScan
public class Application implements CommandLineRunner {
    @Autowired
    DataService dataService;

    @Value("${input}")
    String input;

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Override
    public void run(String... args) {
        dataService.perform(input);
    }
}
```

An added benefit of this approach is that this forces us to use named parameter arguments when running the application as opposed to the position based command line arguments. This of course does not solve the problem of testing if you absolutely have to use position based arguments for your application. It would be nice Spring provided a mechanism to inject the command line arguments in a test before `SpringApplicationContextLoader` [^3] took over. But I suspect that this is not a common enough use case of Spring that users have asked the Spring team to implement it.

[^1]: Meta annotations are Spring annotations that can modify and act up on other annotations. For an example of customizing behavior using meta annotations, see [this blog post](/blog/2015/12/06/implementing-custom-annotations-for-spring-mvc/).
[^2]: The tendency of programmers to name the default element of an annotation `value` is one of my least favorite aspects of Java annotations. In most cases, there is another name that conveys the intent of the element better. I plan to write my thoughts about this in a blog post soon.
[^3]: See the previous blog post to see how `SpringApplicationContextLoader` executes the application without arguments.
