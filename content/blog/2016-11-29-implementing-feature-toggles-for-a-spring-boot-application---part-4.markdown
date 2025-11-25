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
- /blog/2016/11/29/implementing-feature-toggles-for-a-spring-boot-application---part-4/
- /blog/2016/11/29/implementing-feature-toggles-for-a-spring-boot-application-part-4/
bbissueid: 121
date: 2016-11-30 05:50:42
ghissueid: 130
image: images/feature-toggles.png
series:
- feature-toggles
title: Implementing feature toggles for a Spring Boot application - Part 4
---

In the fourth part of this [series](/series/feature-toggles/) about implementing [feature toggles](/blog/2016/11/21/implementing-feature-toggles-for-a-spring-boot-application-part-1/) for a Spring Boot application, we will take a look at how our implementation so far introduced a dependency on the application being restarted for changes to take place.

<!--more-->

In [part 1](/blog/2016/11/21/implementing-feature-toggles-for-a-spring-boot-application-part-1/), we modified the `FeatureToggle` annotation to support toggling beans and decided to use that for toggling features at the controller level. If we had a system capable of providing the feature toggle information to the application without restarts, the change in the state of the controller level toggles will have no effect because the controller is not going to be re-wired for request mapping, unless the application is restarted.

This raises the interesting question - Are bean level switches really feature toggles, considering that they can never be altered without application restarts? A better approach would be to consider bean switches as purely configurations and use facades that route commands to either of the beans based on a feature flag. In the example configuration provided, is treating the choice between storing sessions in-memory / Redis an actual feature, considering it does not provide any value to the end-user?

To ensure that we are not tying feature toggling to restarts, we will remove the meta-annotation we introduced to `FeatureToggle` in [part 1](/blog/2016/11/21/implementing-feature-toggles-for-a-spring-boot-application-part-1/).

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface FeatureToggle {
  String feature();

  boolean expectedToBeOn() default true;
}
```
With this change, we no longer have the ability to toggle off an entire controller. Having to annotate all handler methods in a controller is going to be a painful, error-prone approach. In order to provide the ability to toggle entire controllers, we can modify the `FeatureInterceptor` to look for annotations present on the controller class in addition to annotations present on the handler methods.
```java
public class FeatureInterceptor implements HandlerInterceptor {
  private final FeatureRepository featureRepository;

  public FeatureInterceptor(FeatureRepository featureRepository) {
    this.featureRepository = featureRepository;
  }

  @Override
  public boolean preHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object handler) throws Exception {
    HandlerMethod handlerMethod = (HandlerMethod) handler;
    if (handleMethodAnnotation(handlerMethod) &&
        handleTypeAnnotation(handlerMethod.getBeanType()))  {
      return true;
    }
    httpServletResponse.setStatus(HttpServletResponse.SC_NOT_FOUND);
    return false;
  }

  private boolean handleTypeAnnotation(Class<?> controllerType) {
    FeatureToggle controllerTypeAnnotation = controllerType.getAnnotation(FeatureToggle.class);
    return checkFeatureState(controllerTypeAnnotation);
  }

  private boolean handleMethodAnnotation(HandlerMethod handlerMethod) {
    FeatureToggle methodAnnotation = handlerMethod.getMethodAnnotation(FeatureToggle.class);
    return checkFeatureState(methodAnnotation);
  }

  private boolean checkFeatureState(FeatureToggle methodAnnotation) {
    if (methodAnnotation == null) {
      return true;
    }

    if(featureRepository.isOn(methodAnnotation.feature()) == null) {
      return true;
    }

    if(methodAnnotation.expectedToBeOn() == featureRepository.isOn(methodAnnotation.feature())) {
      return true;
    }
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
This will correctly intercept requests routed to handler methods even if the annotation is at the controller level instead of the method level.
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

Now that we have a feature toggling mechanism in place that no longer depends on application restarts, in the next part, we will look at providing this information to the application from a source that does not require restarts.