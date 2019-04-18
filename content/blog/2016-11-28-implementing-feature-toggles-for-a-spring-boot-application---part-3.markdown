---
title: Implementing feature toggles for a Spring Boot application - Part 3
date: 2016-11-28T22:50:39-07:00
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
image: "images/feature-toggles.png"
series:
- feature-toggles
aliases:
- "/blog/2016/11/28/implementing-feature-toggles-for-a-spring-boot-application---part-3/"
---
In the third part of this [series](/series/feature-toggles/) about implementing feature toggles for a Spring Boot application, we will take a look at exposing the state of feature flags as a Spring Boot management end point for monitoring and testing purposes.

<!--more-->

Spring Boot Actuator exposes a number of [end points](http://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html) to monitor and administer the application. The most commonly used of these in my experience are the `info` and `health` end points. These end points are used to communicate to load balancers that a particular instance is ready to accept traffic and to monitor the state of the application.

## Features management end point

In our case, this end point will be used by administrators, QA engineers and sometimes business stake holders to see what features are available in a particular environment running the application. Of course, we could have re-used the end point we built in the [last blog post]() for this purpose, but creating an management end point allows us to:

*   Control the HTTP end point together with other end points by using the `management.context-path` property. This will allow us to provide certain nodes in our network access to only the management end points without having to expose application behavior to them.
*   Make this information available in a more human readable form for it’s consumers. Even though the information exposed in the `/features` end point is detailed, the format was designed for consumption by code.

Because this is for human consumption, the end point will display the feature state in the following format:

```json
{
  "available": [
    "feature.hello",
    "feature.bar"
    ...
  ],
  "enabled": [
    "feature.hello"
    ...
  ]
}
```

Management end points in Spring Boot are created by implementing the `EndPoint` interface. In our case, the end point will depend on `FeatureRepository` to do the heavy lifting.

```java
public class FeatureEndpoint implements Endpoint<HashMap<String, Set<String>>> {

  public static final String ID = "features";
  private final FeatureRepository featureRepository;

  public FeatureEndpoint(FeatureRepository featureRepository) {
    this.featureRepository = featureRepository;
  }

  @Override
  public String getId() {
    return ID;
  }

  @Override
  public boolean isEnabled() {
    return true;
  }

  @Override
  public boolean isSensitive() {
    return false;
  }

  @Override
  public HashMap<String, Set<String>> invoke() {
    HashMap<String, Set<String>> map = new HashMap<>();
    map.put("enabled", featureRepository.enabledKeys());
    map.put("available", featureRepository.featureKeys());
    return map;
  }
}
```

In order to retrieve the keys for features that are toggled on, we will create an `enabledKeys` method in the repository.

```java
public class FeatureRepository {
  // ...
  public Set<String> enabledKeys() {
    return featureKeys().stream()
        .filter(f -> isOn(f))
        .collect(Collectors.toSet());
  }
}
```

With this end point in place and the `management.context-path` set to `management` in our properties, this end point will produce the following output.

```java
> curl -s "http://localhost:8080/management/features" | jq .
{
  "available": [
    "feature.foo",
    "feature.hello"
  ],
  "enabled": [
    "feature.hello"
  ]
}
```
It is important to note that our end point has it’s sensitivity flag set to false by default. You should consider the [security implications](http://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html#_security_with_healthindicators) of that before choosing to leave it false.

In the next blog post in this [series](/series/feature-toggles/), we will explore how our feature toggle mechanism so far have introduced a dependency on the application being restarted and how to eliminate this dependency.
