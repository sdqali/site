---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
date: 2016-06-28T23:17:51-04:00
title: Injecting dependencies into a Spring @Configuration
image: "images/spring-by-pivotal.png"
---

This is one of those blog posts about things I wish I had known before I spent a lot of time figuring out when something was not working as expected. Recently, we have been trying to extend a `WebMvcConfigurerAdapter` to wire up an HTTP request interceptor. And things did not work as we expected it to and we learned that our understanding of how Spring behaved under this situation was wrong. This is a write up to refer back to if and when we encounter this issue again.

<!--more-->

Spring's `@Configuration` annotation allows us to create a class that provides a set of beans. Because we wanted to wire up interceptors when the application started, it felt reasonable to annotate the extended `WebMvcConfigurerAdapter` adaptor as a `@Configuration`.

So we ended up with code that looked as follows:

```java
@Configuration
public class Config extends WebMvcConfigurerAdapter {
    private HandlerInterceptor handlerInterceptor;

    @SuppressWarnings("unused")
    public Config() {
    }

    @Autowired
    public Config(HandlerInterceptor handlerInterceptor) {
        this.handlerInterceptor = handlerInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(handlerInterceptor);
        super.addInterceptors(registry);
    }
}
```

The interceptor itself is declared a `@Component` of the following form:

```java
@Component
public class SessionCheckInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if(request.getHeader("session") == null) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return false;
        } else {
            return true;
        }
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

    }
}
```

As you can see, the interceptor checks every request for a `session` header and responds with a `BAD_REQUEST (400)` in the absence of it.
{{< mailchimp >}}

This code compiles fine, but when you run it, you will be confronted with the following stack trace:

```bash
Factory method 'requestMappingHandlerMapping' threw exception; nested exception is java.lang.IllegalArgumentException: Interceptor is required
```

So, what happened? Looking at the stack trace reveals the following:

```bash
Caused by: java.lang.IllegalArgumentException: Interceptor is required
    at org.springframework.util.Assert.notNull(Assert.java:115)
    at org.springframework.web.servlet.config.annotation.InterceptorRegistration.<init>(InterceptorRegistration.java:51)
    at org.springframework.web.servlet.config.annotation.InterceptorRegistry.addInterceptor(InterceptorRegistry.java:45)
    at in.sdqali.spring.config.Config.addInterceptors(Config.java:30)
```

Evidently, the interceptor we wired up is `null`. After a spending a lot of time on this, we discovered this line on the java doc for `@Configuration`:

```
@Configuration is meta-annotated with @Component, therefore
@Configuration classes are candidates for component scanning (typically using
Spring XML's <context:component-scan/> element) and therefore may also take
advantage of @Autowired/@Inject
at the field and method level (but not at the constructor level).
```

A simple fix is to inject the interceptor through a setter as follows:

```java
@Configuration
public class Config extends WebMvcConfigurerAdapter {
    private HandlerInterceptor handlerInterceptor;

    @SuppressWarnings("unused")
    public Config() {
    }

    @Autowired
    public void setHandlerInterceptor(HandlerInterceptor handlerInterceptor) {
        this.handlerInterceptor = handlerInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(handlerInterceptor);
        super.addInterceptors(registry);
    }
}
```

It took us a lot of time debugging and stepping through Spring code before we finally figured out what the issue was, but we could have discovered it in seconds from the java doc. There is a lesson in there for us.

The example code to demonstrate this is available on [GitHub](https://github.com/sdqali/config-constructor-poc).
