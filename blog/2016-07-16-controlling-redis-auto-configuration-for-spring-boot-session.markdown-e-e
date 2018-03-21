---
Categories:
- development
- spring
- java
- redis
Description: "This blog post describes how to control the auto-configuration of Redis in a Spring Boot application using Spring Session, thereby making it possible to use the default in-memory session store in environments where Redis is not present. This is useful in Continuous Integration environments and development environments."
Tags:
- development
- spring
- java
- redis
date: 2016-07-16T15:42:05-07:00
image: "/images/redis-spring-boot.png"
title: Controlling Redis auto-configuration for Spring Boot Session
---
If you have been using Spring Boot, chances are that you are using the Spring Session library to handle sessions. Spring Session has the ability to persist the sessions to various data stores, including Redis. The default behaviors of Spring Boot when combined with Spring Session is to start using Redis as the session store the moment `spring-session-data-redis` is detected in the class path, thereby making it hard to conditionally turn Redis support ON and OFF. This blog post explores why this is the default behavior and presents a solution to control this behavior.
<!--more-->
### The application
The application we will be using to demonstrate this behavior is a Spring Boot 1.3.6 application with a single controller.
```java
@RestController
@RequestMapping("/hello")
public class HelloController {
  @RequestMapping(method = GET,
      path = "",
      produces = APPLICATION_JSON_VALUE)
  public Map<String, String> hello() {
    return Collections.singletonMap("message", "hello");
  }
}
```
The application also has Spring Security configured to allow authentication for a single user named `user`.
```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
  @Override
  protected void configure(HttpSecurity http) throws Exception {
    http
        .authorizeRequests()
        .antMatchers("/hello/**").hasRole("USER")
        .and()
        .httpBasic();
  }

  @Autowired
  public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
    auth
        .inMemoryAuthentication()
        .withUser("user").password("password").roles("USER");
  }

  @Bean
  public HeaderHttpSessionStrategy sessionStrategy() {
    return new HeaderHttpSessionStrategy();
  }
}
```
This forces clients to authenticate for access to resources under `/hello` and configures an in memory user `user` with password `password`. In this example, we will also be using `HeaderHttpSessionStrategy` [^1] to pass the session value between client and server using the `x-auth-token` header instead of a Cookie.

### The issue
This is an issue only when using Spring Boot 1.3 or greater. If we are to follow the instructions provided at the [official documentation](http://docs.spring.io/spring-session/docs/1.2.1.RELEASE/reference/html5/guides/boot.html) from Spring Session [^2], we end up with the following configuration.
```java
@EnableRedisHttpSession
public class RedisSessionConfig {
}
```
With this in place, authentication works as we expect. The application allows the user to obtain a session and authenticates correctly when presented with the session token.
```bash
$ curl -i -s -X GET "http://localhost:8080/hello" -uuser:password  | grep "x-auth-token"
x-auth-token: c0fbb47d-d19f-44b1-a8d7-44e4837f403d
$ curl -s -X GET "http://localhost:8080/hello" --header "x-auth-token: c0fbb47d-d19f-44b1-a8d7-44e4837f403d" | jq .
{
  "message": "hello"
}
```
We can monitor the interactions the application performs with Redis by running Redis monitor:
```bash
$ redis-cli monitor
```
This is great. Now, let's attempt to modify our configuration to use Redis only in some environments and use the in-memory session store in others. We start by making `RedisSessionConfig` conditional on the value of the property `use.redis.session.store` being `true`:
```java
@ConditionalOnProperty(name = "use.redis.session.store", havingValue = "true")
@EnableRedisHttpSession
public class RedisSessionConfig {
}
```
We will create a new configuration that sets up the in-memory session store if `use.redis.session.store` is false or missing.
```java
@Configuration
@EnableSpringHttpSession
@ConditionalOnProperty(name = "use.redis.session.store", havingValue = "false", matchIfMissing = true)
public class MapSessionConfig {
  @Bean
  public SessionRepository sessionRepository() {
    return new MapSessionRepository();
  }
}
```
Let's set the property to `false` so that we do not have to depend on Redis in the local environment.
```
use.redis.session.store=false
```
With this in place, we expect that there are no interactions with Redis server. If we were to start the server, we will get the following error:
```
...
Caused by: java.net.ConnectException: Connection refused
    at java.net.PlainSocketImpl.socketConnect(Native Method) ~[na:1.8.0_45]
    at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:345) ~[na:1.8.0_45]
    at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206) ~[na:1.8.0_45]
    at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188) ~[na:1.8.0_45]
    at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392) ~[na:1.8.0_45]
    at java.net.Socket.connect(Socket.java:589) ~[na:1.8.0_45]
    at redis.clients.jedis.Connection.connect(Connection.java:158) ~[jedis-2.7.3.jar:na]
...
```
It appears that the application is trying to make connections to Redis, even though we configured it not to. What is going on? It looks like some where along the chain, some configuration with the annotation `@EnableSpringHttpSession` is being loaded. Why could that happen?

### Spring Boot Autoconfig
Like a lot of Spring Boot applications, we are using the `@SpringBootApplication` annotation in our application. This is a meta-annotation [^3] that takes the following form:
```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@Configuration
@EnableAutoConfiguration
@ComponentScan
```
The `@EnableAutoConfiguration` annotation is interesting because it wires up most of the default configuration that makes Spring Boot great for development. The annotation itself and the supporting mechanism that automatically loads configurations are present in the `org.springframework.boot:spring-boot-autoconfigure` library. One of these configurations is `SessionAutoConfiguration` which was introduced in Spring Boot `1.3.0`. It has the following code in version `1.3.6`:
```java
@Configuration
@ConditionalOnClass(Session.class)
@AutoConfigureAfter(RedisAutoConfiguration.class)
public class SessionAutoConfiguration {

    @EnableConfigurationProperties
    @ConditionalOnClass(RedisConnectionFactory.class)
    @ConditionalOnWebApplication
    @ConditionalOnMissingBean(RedisHttpSessionConfiguration.class)
    @EnableRedisHttpSession
    @Configuration
    public static class SessionRedisHttpConfiguration {

        @Autowired
        private ServerProperties serverProperties;

        @Autowired
        private RedisOperationsSessionRepository sessionRepository;

        @PostConstruct
        public void applyConfigurationProperties() {
            Integer timeout = this.serverProperties.getSession().getTimeout();
            if (timeout != null) {
                this.sessionRepository.setDefaultMaxInactiveInterval(timeout);
            }
        }

        @Configuration
        @ConditionalOnMissingBean(value = ServerProperties.class, search = SearchStrategy.CURRENT)
        // Just in case user switches off ServerPropertiesAutoConfiguration
        public static class ServerPropertiesConfiguration {

            @Bean
            // Use the same bean name as the default one for any old webapp
            public ServerProperties serverProperties() {
                return new ServerProperties();
            }

        }

    }

}
```
And this is where things get interesting. We can clearly see that `SessionRedisHttpConfiguration` is annotated with `@EnableRedisHttpSession`. This class will be applied by Spring the moment it's parent class `SessionAutoConfiguration` is applied. The third annotation on the parent class `@AutoConfigureAfter(RedisAutoConfiguration.class)` instructs Spring to apply this configuration after `RedisAutoConfiguration`. This configuration has the following:
```java
@Configuration
@ConditionalOnClass({ JedisConnection.class, RedisOperations.class, Jedis.class })
@EnableConfigurationProperties
public class RedisAutoConfiguration {
// ...
// ...
}
```
This configuration will be applied if and only if the classes `JedisConnection`, `RedisOperations` and `Jedis` are present in the class path and by adding `spring-session-data-redis` as a dependency, we are causing exactly that to happen.

### A solution
We can prevent this from occurring by configuring our application to not attempt to apply this auto configuration class. This can be done by specifying this class to be excluded from the application.
```java
@SpringBootApplication(exclude = {SessionAutoConfiguration.class})
public class RedisSessionApplication {
    public static void main(String[] args) {
        SpringApplication.run(RedisSessionApplication.class, args);
    }
}
```
With this is place, if we run the application, it will no longer encounter the connection error previously saw. Authentication works as before, except that it now uses the in-memory session store.

```bash
$ curl -i -s -X GET "http://localhost:8080/hello" -uuser:password  | grep "x-auth-token"
x-auth-token: d0962e39-6423-46b3-b815-8979950e063a
$ curl -s -X GET "http://localhost:8080/hello" --header "x-auth-token: d0962e39-6423-46b3-b815-8979950e063a" | jq .
{
  "message": "hello"
}
```

[^1]: HeaderHttpSessionStrategy allows the use of a header to transmit the session between client and server. The default header is `x-auth-token`, but this can be configured. See the documentation [here](http://docs.spring.io/spring-session/docs/current/api/org/springframework/session/web/http/HeaderHttpSessionStrategy.html).
[^2]: This example uses the default configurations for Redis connection to localhost on port 6379.
[^3]: Meta annotations are annotations that can act up on other annotations by modifying and overriding their attributes. For a discussion on how to implement custom annotations using meta annotations, please refer to [this blog post](/blog/2015/12/06/implementing-custom-annotations-for-spring-mvc/).
