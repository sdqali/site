---
Categories:
- development
- code
- feature-toggles
- java
- spring
Description: ""
Tags:
- development
- code
- feature-toggles
- java
- spring
date: 2016-11-21T17:03:03-08:00
image: "images/feature-toggles.png"
series:
- feature-toggles
title: Implementing feature toggles for a Spring Boot application - Part 1
---
In one of our recent projects at work, we implemented feature toggles for a Spring MVC / Angular JS code base and this [series of blog posts](/series/feature-toggles) discusses our motivations and requirements, the approach we took and what we learned from it.
<!--more-->
## Introduction
Feature Toggles are a mechanism to change the behavior of software without having to re-deploy code. Pete Hogdson has a comprehensive [blog post](http://martinfowler.com/articles/feature-toggles.html) explaining the complexities of feature toggles.

![Feature toggles](/images/feature-toggles.svg "Feature toggles")

## Requirements
Our application is a Spring Boot web application that gets deployed in a Tomcat instance. The application is deployed via Chef and chef sets up the appropriate configuration parameters for the application as Tomcat [Environment](https://tomcat.apache.org/tomcat-8.0-doc/config/context.html#Environment_Entries) entries. Since feature toggles are ultimately application parameters [^1], we started by setting them as Tomcat environment variables. Having considered this, we identified the following requirements:

* The ability to toggle dependency injection. For example, in some environments, we wanted to use Redis to store our sessions, while in some test environments, they were to be stored in memory.
* Ability to toggle entire Spring Controllers or individual controller methods.
* The ability to expose the state of feature toggles to our front end so that Angular JS components can use the feature toggles.

## Our initial approach
### Toggling dependency injection.
We started by using configuration parameters with the `feature` prefix to toggle features. With this convention in place, we started using the `@ConditionalOnProperty` annotation in our configuration classes to toggle the beans that got wired up. For example, to toggle between Redis and in-memory store for sessions, we ended up with the following configuration:
```java
@Configuration
public class AppConfig {
  @Bean
  @ConditionalOnProperty(value = "feature.redis.session.store", havingValue = "false")
  public SessionRepository mapSessionRepository() {
    return new MapSessionRepository();
  }

  @Bean
  @ConditionalOnProperty(value = "feature.redis.session.store", havingValue = "true")
  public SessionRepository redisSessionRepository(RedisConnectionFactory factory) {
    return new RedisOperationsSessionRepository(factory);
  }
}
```

### Toggling individual controller methods
In order to prevent end points defined by controllers and controller methods that are toggled off from being accessed, we decided to configure a `HandlerInterceptor` [^2] to intercept requests to these end points.
```java
public class FeatureInterceptor implements HandlerInterceptor {
  private final FeatureRepository featureRepository;

  public FeatureInterceptor(FeatureRepository featureRepository) {
    this.featureRepository = featureRepository;
  }

  @Override
  public boolean preHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object handler) throws Exception {
    HandlerMethod handlerMethod = (HandlerMethod) handler;
    FeatureToggle methodAnnotation = handlerMethod.getMethodAnnotation(FeatureToggle.class);
    if (methodAnnotation == null) {
      return true;
    }

    if(featureRepository.isOn(methodAnnotation.feature()) == null) {
      return true;
    }

    if(methodAnnotation.expectedToBeOn() == featureRepository.isOn(methodAnnotation.feature())) {
      return true;
    }

    httpServletResponse.setStatus(HttpServletResponse.SC_NOT_FOUND);
    return false;
  }

  @Override
  public void postHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, ModelAndView modelAndView) throws Exception {

  }

  @Override
  public void afterCompletion(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, Exception e) throws Exception {

  }
}
```
This feature interceptor uses the `FeatureToggle` looks for the annotation, and the looks at a feature repository to see if the state of the feature flag is set to what the annotation expects and if it does not, returns a 404. The annotation has two attributes - `isOn` and `feature`.
```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface FeatureToggle {
  String feature();

  boolean expectedToBeOn() default true;
}
```
This annotation can be used on a controller method as follows:
```java
@RestController
@RequestMapping("/hello")
public class MessageController {
  @RequestMapping("")
  @FeatureToggle(feature = "feature.hello")
  public Map hello() {
    return Collections.singletonMap("message", "hello world!");
  }
}
```
The `FeatureRepository` has to look at all the properties that are available in the applications environment and filter out the ones that start with `feature.`.
{{< mailchimp >}}
Collecting all the properties available in an environment is [surprisingly complex](https://stackoverflow.com/questions/23506471/spring-access-all-environment-properties-as-a-map-or-properties-object), owing to the number of ways properties can be injected. Based on the approach discussed in that question, we can create a `FeatureRepository` as follows:
```java
public class FeatureRepository {
  private static final String FEATURE_PREFIX = "feature.";
  private final Environment env;

  public FeatureRepository(Environment env) {
    this.env = env;
  }

  public Set<String> featureKeys() {
    Map<String, Object> map = new HashMap();
    for(Iterator it = ((AbstractEnvironment) env).getPropertySources().iterator(); it.hasNext(); ) {
      PropertySource propertySource = (PropertySource) it.next();
      if (propertySource instanceof MapPropertySource) {
        map.putAll(((MapPropertySource) propertySource).getSource());
      }
    }
    return map.keySet().stream()
        .filter(k -> k.startsWith(FEATURE_PREFIX))
        .collect(Collectors.toSet());
  }

  public Boolean isOn(String key) {
    return allFeatures().get(key);
  }

  public Map<String, Boolean> allFeatures() {
    return featureKeys().stream().collect(Collectors.toMap(k -> k, k -> Boolean.parseBoolean(env.getProperty(k))));
  }
}
```

### Toggling entire controllers
Since Spring controllers are wired up as beans, the `ConditionalOnProperty` annotation can be used to toggle on entire controllers.
```java
@RestController
@RequestMapping("/foo")
@ConditionalOnProperty(value = "feature.foo", havingValue = "true")
public class FooController {
  @RequestMapping("")
  public Map hello() {
    return Collections.singletonMap("message", "hello foo!");
  }
}
```
However, now we have two different mechanisms to toggle methods and controllers. It will be nice to consolidate them and doing so will allow us to use the same mechanism for toggling beans. This can be done by annotating `FeatureToggle` with the [meta annotation](/blog/2015/12/06/implementing-custom-annotations-for-spring-mvc/) `Conditional` that looks up the state of feature toggles using the custom condition `FeatureCondition`. This will change `FeatureToggle` to:
```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Conditional(FeatureCondition.class)
public @interface FeatureToggle {
  String feature();

  boolean expectedToBeOn() default true;
}
```
The `FearureCondition` uses the meta annotation attributes provided to it and the environment to decide the state to be returned:
```java
public class FeatureCondition implements Condition {
  @Override
  public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata annotatedTypeMetadata) {
    if(annotatedTypeMetadata.isAnnotated(FeatureToggle.class.getCanonicalName())) {
      Map<String, Object> annotationAttributes = annotatedTypeMetadata
          .getAnnotationAttributes(FeatureToggle.class.getCanonicalName());
      String feature = (String) annotationAttributes.get("feature");
      boolean expectedToBeOn = Boolean.parseBoolean(String.valueOf(annotationAttributes.get("expectedToBeOn")));
      boolean isOn = Boolean.parseBoolean(conditionContext.getEnvironment().getProperty(feature));
      return expectedToBeOn == isOn;
    }
    return true;
  }
}
```
Now that we have a unified mechanism to toggle controllers, beans and controller methods, we can use this annotation. The `FooController` would now look like this:
```java
@RestController
@RequestMapping("/foo")
@FeatureToggle(feature = "feature.foo")
public class FooController {
  @RequestMapping("")
  public Map hello() {
    return Collections.singletonMap("message", "hello foo!");
  }
}
```
And our `AppConfig` will be like this:
```java
@Configuration
public class AppConfig extends WebMvcConfigurerAdapter {
  @Autowired
  Environment env;

  @Bean
  @FeatureToggle(feature = "feature.redis.session.store", expectedToBeOn = false)
  public SessionRepository mapSessionRepository() {
    return new MapSessionRepository();
  }

  @Bean
  @FeatureToggle(feature = "feature.redis.session.store")
  public SessionRepository redisSessionRepository(RedisConnectionFactory factory) {
    return new RedisOperationsSessionRepository(factory);
  }

  @Override
  public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(new FeatureInterceptor(new FeatureRepository(env)));
    super.addInterceptors(registry);
  }
}
```
In the second part of [this series](/series/feature-toggles), we will explore how the feature toggle can be exposed to the front end and how to consume this and use it for toggling features in the Angular components.

[^1]: While feature toggles are just like any other application parameter, treating them as such in our stack resulted in errors, which we address later in this series.
[^2]: HandlerInterceptor
