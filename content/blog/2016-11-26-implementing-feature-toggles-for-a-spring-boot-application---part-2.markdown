---
Categories:
- development
- code
- feature-toggles
- java
- spring
Description: ''
Tags:
- development
- code
- feature-toggles
- java
- spring
aliases:
- /blog/2016/11/26/implementing-feature-toggles-for-a-spring-boot-application---part-2/
- /blog/2016/11/26/implementing-feature-toggles-for-a-spring-boot-application-part-2/
bbissueid: 118
date: 2016-11-27 05:48:48
ghissueid: 128
image: images/feature-toggles.png
series:
- feature-toggles
title: Implementing feature toggles for a Spring Boot application - Part 2
---

In the second part of this [series](/series/feature-toggles/) about implementing feature toggles for a Spring Boot application, we will look at exposing the features to the Angular front-end so that features can be toggled in UI components.

<!--more-->

## Toggling at the front end

We decided to use the [angular-feature-flags](https://github.com/mjt01/angular-feature-flags) library to toggle features at the front end because it provided us the three features that we were looking for:

*   The ability to load the state of feature flags [from an HTTP end point](https://github.com/mjt01/angular-feature-flags#setting-flag-data) instead of having to generate JS code through templates.
*   The ability to toggle entire html components through the `feature-flag` attribute directive.
*   The ability to expose these features to services and components to make if-else decisions through `featureFlagsProvider`.

## Features end point

The library expects feature flags to be provided to `featureFlagsProvider` in the following format:

```json
[
    { "key": "...", "active": "...", "name": "...", "description": "..." },
    ...
]
```

The `FeatureController` will use the `FeatureRepository` to expose this will look like this:

```java
@RestController
@RequestMapping("/features")
public class FeatureController {
  @Autowired
  FeatureRepository featureRepository;

  @RequestMapping("")
  public List<Map> features() {
    return featureRepository.allFeatures()
        .entrySet()
        .stream()
        .map(entry -> new HashMap<String, Object>() {
          {
            put("key", entry.getKey());
            put("active", entry.getValue());
            put("name", entry.getKey());
            put("description", entry.getKey());
          }
        })
        .collect(Collectors.toList());
  }
}
```

We are using the double brace initialization technique to construct the map representing each feature. Initializing a map given a set of keys and values is still an exercise that requires a bunch of [boiler plate](https://minborgsjavapot.blogspot.com/2014/12/java-8-initializing-maps-in-smartest-way.html) code in Java. You can get around this by using the convenient ImmutableMap.of() provided by [Google Collections](https://mvnrepository.com/artifact/com.google.collections/google-collections/1.0).

It is also important to change our `AppConfig` to initialize the instance of `Featurerepository` as a bean.

```java
@Configuration
public class AppConfig extends WebMvcConfigurerAdapter {
  @Autowired
  Environment env;

  // ...

  @Bean
  public FeatureRepository featureRepository() {
    return new FeatureRepository(env);
  }
}
```

With this configuration, we can get the feature state from the end point:

```bash
> curl -s "http://localhost:8080/features" | jq .
[
  {
    "name": "feature.foo",
    "active": false,
    "description": "feature.foo",
    "key": "feature.foo"
  },
  {
    "name": "feature.hello",
    "active": true,
    "description": "feature.hello",
    "key": "feature.hello"
  }
]
```
For our use case, we were comfortable re-using the feature key as the name and description of the feature. You may want to capture these meta data in your application configuration and expose this using Spring Boot’s [ConfigurationProperties](http://docs.spring.io/spring-boot/docs/1.1.7.RELEASE/api/org/springframework/boot/context/properties/ConfigurationProperties.html). You can find an example of how use structured configurations in [my example project](https://github.com/sdqali/config-properties).

In the next part of this [series](/series/feature-toggles/), we will take a look at how to expose the feature information as an [admin end point](http://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html).