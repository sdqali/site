---
Categories:
- development
- java
- camel
Description: ""
Tags:
- development
- camel
- java
- spring
date: 2015-12-16T01:07:01-05:00
title: Authentication for Apache Camel HTTP components
image: "images/apache-camel.png"
---
My team at work has been lately working on a data transformer that pushes information from an external system in to platform. For historical reasons the information is passed to us in the form of flat files. We have been working on a data transformer that reads information from the file and posts it into an HTTP end point.
Apache Camel [^1] makes a natural choice as the base for implementing such a data transformer. The presence of ready to use components that can read files and post information to HTTP end points and the availability of a nice D.S.L. [^2] makes implementation easy and straightforward. One of the things we had to spend time figuring out was how to ensure that we authenticate correctly against our target HTTP end point. This blog post takes a look at various methods we explored.

<!--more-->
Camel's HTTP component allows http resources to be added as Camel end points. These end points can be consuming information from routes or producing information which are then passed on to routes. For example, the following route takes information from the `direct:start` end point, tokenizes it into lines and sends each line into an HTTP url.

```java
public class FileToApiRoute extends RouteBuilder {

    public static final String UTF_8 = "UTF-8";
    public static final String CONTENT_TYPE = "Content-Type";
    public static final String APPLICATION_JSON = "application/json";
    public static final String TARGET = "http://localhost:8080/ingest";

    @Override
    public void configure() throws Exception {
        from("direct:start")
                .marshal()
                .string(UTF_8)
                .split(body().tokenize())
                .streaming()
                .setHeader(CONTENT_TYPE, simple(APPLICATION_JSON))
                .to(TARGET);
    }
}
```

Once this route has been registered, it can be used to send data by placing information on the `direct:start` end point. The following service does it by passing the contents of a file to a `ProducerTemplate`:

```java
public class DataStreamService {

    private final ProducerTemplate producerTemplate;

    @Autowired
    public DataStreamService(ProducerTemplate producerTemplate) {
        this.producerTemplate = producerTemplate;
    }

    public void stream() {
        producerTemplate.sendBody("direct:start",
                ExchangePattern.InOnly,
                new File("src/main/resources/yelp.business.json"));
    }
}
```

Our challenge is to ensure that this continue to work when the HTTP end point in question requires authentication. For the purposes of this blog post, we will be restricting our discussion to Basic Authentication. There are three ways to do this authentication–through Camel authentication query parameters, through the use of the `Authorization` header and by overriding the `HttpConfiguration` in the current Camel context.
{{< mailchimp >}}

### Camel authentication query parameters

Camel allows consumers to specify authentication parameters in the http end point. For example, three parameters required for Basic Authentication are `authMethod`, `authUsername` and `authPassword`. The route rewritten with these parameters will be as follows:

```java
    public static final String TARGET_WITH_AUTH = "http://localhost:8080/ingest" +
            "?authMethod=Basic&authUsername=test&authPassword=test";

    @Override
    public void configure() throws Exception {
        from("direct:start")
                .marshal()
                .string(UTF_8)
                .split(body().tokenize())
                .streaming()
                .setHeader(CONTENT_TYPE, simple(APPLICATION_JSON))
                .to(TARGET_WITH_AUTH);
    }
```
It is odd to be adding authentication parameters to a URL, but here the URL has multiple purposes–this is a URL to which information is going to be sent to, it also represents a logical end point. These three parameters (and other authentication parameters) get stripped from the HTTP URL before Camel makes the HTTP request. [^3] This still will cause issues in odd cases where the HTTP A.P.I. you are integrating with expects these parameters to be sent.

### Setting Authorization headers

Camel allows the addition of headers to messages that it processes and if the message ultimately gets routed to a Camel HTTP end point, these headers get converted to HTTP headers. This allows us to use authentication by setting the `Authorization` header. This example demonstrates this:

```java
    public void configure() throws Exception {
        from("direct:start")
                .marshal()
                .string(UTF_8)
                .split(body().tokenize())
                .streaming()
                .setHeader(CONTENT_TYPE, simple(APPLICATION_JSON))
                .setHeader("Authorization", simple("Basic dGVzdDp0ZXN0"))
                .to(TARGET);
    }
```

### Overriding HttpConfiguration

Camel provides a mechanism to override it‘s Context‘s configuration before the context gets created. In the following example, we get a reference to the `HttpComponent` and set a new `HttpConfiguration` with the right authentication. This allows us to separate the authentication configurations from the route definitions. However, if your Camel context is responsible for talking to different HTTP end points with different authentication mechanisms or parameters, this will not solve the issue.

```java
    @Bean
    CamelContextConfiguration contextConfiguration() {
        return camelContext -> {
            HttpComponent http = (HttpComponent) camelContext.getComponent("http");
            http.setHttpConfiguration(httpConfiguration());
        };
    }

    private HttpConfiguration httpConfiguration() {
        HttpConfiguration httpConfiguration = new HttpConfiguration();
        httpConfiguration.setAuthMethod(authScheme);
        httpConfiguration.setAuthUsername(authUsername);
        httpConfiguration.setAuthPassword(authPassword);
        return httpConfiguration;
    }
```

In the end, the method you choose will depend on the unique constraints of the systems you are integrating with.

[^1]: [Apache Camel](https://camel.apache.org/) is a Java integration framework.
[^2]: Camel's Domain Specific Language in Java allows integration routes to be defined as fluent specifications.
[^3]: Stripping of these parameters is done inside `org.apache.camel.component.http.HttpComponent`‘s `createHttpClientConfigurer` [method](https://github.com/apache/camel/blob/f7f0b18f6924fe0b01f32a25ed1e38e29b1bf8e5/components/camel-http/src/main/java/org/apache/camel/component/http/HttpComponent.java#L66).
