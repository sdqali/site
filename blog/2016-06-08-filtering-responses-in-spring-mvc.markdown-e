---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
- spring
date: 2016-06-08T13:23:16-04:00
title: Filtering responses in Spring MVC
image: "images/spring-by-pivotal.png"
---

Yesterday my colleague [Imdad](https://twitter.com/imdhmd) asked if there was a mechanism to add filtering to a Spring MVC end point that responded with JSON. We both started looking at it and this blog post explores a way to do it, albeit for a specific type of responses that was relevant to our discussions.

<!--more-->
For the purposes of this blog post, the response of the end point will be a collection of repositories, taken from the GitHub API for the end point `https://api.github.com/users/rails/repos`. This has the following structure.

```json
[
  {
    "id": 20544,
    "name": "account_location",
    "full_name": "rails/account_location",
    "owner": {
      ...
    },
    ...
    "watchers_count": 70,
    "language": "Ruby",
    "has_issues": false,
    "has_downloads": true,
    "has_wiki": false,
    "has_pages": false,
    "forks_count": 12,
    "mirror_url": null,
    "open_issues_count": 0,
    "forks": 12,
    "open_issues": 0,
    "watchers": 70,
    "default_branch": "master"
  }
  ...
  ...
]
```

We have a simple end point that reads a file with this response and responds with a JSON representation of it.

```java
@RestController
public class ReposController {
    @RequestMapping(path = "/repos", method = GET)
    public List repos() throws URISyntaxException, IOException {
        URL url = this.getClass().getClassLoader().getResource("repos.json").toURI().toURL();

        ObjectMapper objectMapper = new ObjectMapper();

        return objectMapper.readValue(url, List.class);
    }
}
```

What we want to do is to provide a convenient mechanism so that this end point can respond for request made with url parameters which it uses to filter repositories. For example, we expect the request to `http://localhost:8080/repos?fork=true&language=Ruby` to have a JSON response with an array containing only those repositories that are forks and have Ruby as their primary language. Of course, it is worth pointing out that in actual system, you would want to do these kind of filtering at the data layer instead of the web layer, but this is an exercise to see how we could do it at the Spring layer.
{{< mailchimp >}}
We want our mechanism to be easy to use and I came with annotation that we would use as follows:

```java
public class ReposController {
    @RequestMapping(path = "/repos", method = GET)
    @JsonFilter(keys = {"fork", "language"})
    public List repos() throws URISyntaxException, IOException {
      // ...
    }
}
```

The annotation itself takes the following form:

```java
@Target(ElementType.METHOD)
@Documented
@Retention(RetentionPolicy.RUNTIME)
public @interface JsonFilter {
    // JSON keys that will be used for filtering
    String[] keys() default {};
}
```

Spring MVC provides a `ResponseBodyAdvice` [^1] to customize the response immediately after the execution of a controller method, which is exactly what we want in this situation. The interface expects us to implement two methods.

```java
@ControllerAdvice
public class JsonFilterAdvice implements ResponseBodyAdvice<List> {
    @Override
    public boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType) {
        return true;
    }

    @Override
    public List beforeBodyWrite(List body, MethodParameter returnType, MediaType selectedContentType, Class<? extends
    HttpMessageConverter<?>> selectedConverterType, ServerHttpRequest request, ServerHttpResponse response) {
        return body;
    }
}

```

For our case, we want the advice to modify response only if the controller method has the `@JsonFilter` annotation. This is possible with the following implementation of the `supports` method:

```java
    @Override
    public boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType) {
        List<Annotation> annotations = Arrays.asList(returnType.getMethodAnnotations());
        return annotations.stream().anyMatch(annotation -> annotation.annotationType().equals(JsonFilter.class));
    }
```

The actual filtering of the response itself involves filtering the `List` for only those entries where every filter key has values provided in the incoming request. The following implementation achieves this:

```java
    @Override
    public List beforeBodyWrite(List body, MethodParameter returnType, MediaType selectedContentType, Class<? extends
            HttpMessageConverter<?>> selectedConverterType, ServerHttpRequest request, ServerHttpResponse response) {
        List<Map<String, Object>> values = (List<Map<String, Object>>) body;

        // Identify keys we are interested in.
        JsonFilter annotation = returnType.getMethodAnnotation(JsonFilter.class);
        List<String> possibleFilters = Arrays.asList(annotation.keys());

        HttpServletRequest servletRequest = ((ServletServerHttpRequest) request).getServletRequest();

        List<Map<String, Object>> result = values.stream().filter(map -> {
            boolean match = true;
            Enumeration<String> parameterNames = servletRequest.getParameterNames();
            while (parameterNames.hasMoreElements()) {
                String parameterName = parameterNames.nextElement();
                if(possibleFilters.contains(parameterName)) {
                    String parameterValue = servletRequest.getParameter(parameterName);
                    Object valueFromMap = map.get(parameterName);
                    match = (valueFromMap != null) && valueFromMap.toString().equals(parameterValue.toString());
                }
            }
            return match;
        }).collect(Collectors.toList());
        return result;
    }
```
For every entry in the list, we compare query parameter values in the request's URL to the one in the map and filter out only those entries where every combination matches. This is probably not the most efficient way of doing it, but for a quick hack, I am okay with it. Please feel free to take this and improve it. The code for this example is available on [GitHub](https://github.com/sdqali/spring-json-filter).

PS: Imdad may or may not have asked me to credit him for this blog post. ;-)

[^1]: `ResponseBodyAdvice` is an interface that can be wired with a `@ControllerAdvice` annotation to customize the response of controller methods. See the documentation [here](http://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/servlet/mvc/method/annotation/ResponseBodyAdvice.html).
