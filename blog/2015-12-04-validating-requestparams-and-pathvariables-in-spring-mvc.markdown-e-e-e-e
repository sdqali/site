---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
- spring
- jsr-303
- validation
- request-parameters
date: 2015-12-04T22:50:24-08:00
title: Validating RequestParams and PathVariables in Spring MVC
image: "images/spring-by-pivotal.png"
---
<meta content="spring, validate, request, parameters, @requestparam, spring mvc, param, validation" name="keywords">
Spring MVC provides a convenient way to validate inputs to API end points through the use of `JSR-303` annotations. While this mechanism works great for end points that consume a `RequestBody` (as is the case with most `POST` and `PUT` requests), it is not easy to achieve the same effect for end points that consume primitives in the form of path variables or request parameters (as is the case with most `GET` requests).

<!--more-->

Let's take a look at how to validate RequestBody inputs using JSR-303.

```java
    @RequestMapping(method = RequestMethod.POST,
            consumes = MediaType.APPLICATION_JSON_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    @ResponseStatus(HttpStatus.OK)
    public Map register(@RequestBody @Valid EmailRequest emailRequest) {
        return registrationService.register(emailRequest);
    }
```

The value object `EmailRequest` is annotated with the appropriate constraint annotations.

```java
public class EmailRequest {
    @Email
    public String email;

    private EmailRequest() {
    }

    public String getEmail() {
        return email;
    }
}
```


If we were to attempt a similar approach for a `GET` end point that accepts a `RequestParam`, the validation would simply not happen.

```java
    @RequestMapping(method = RequestMethod.GET,
            consumes = MediaType.APPLICATION_JSON_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    @ResponseStatus(HttpStatus.OK)
    public Map search(@Email
                   @Valid
                   @RequestParam("email")
                   String email) {
        return emailMessage(email);
    }
```
{{< mailchimp >}}

This is where Spring's `@Validated` annotation is useful. With `@Validated`, we can validate request parameters and path variables.

```java
@RestController
@Validated
public class RegistrationController {
    @RequestMapping(method = RequestMethod.GET,
            consumes = MediaType.APPLICATION_JSON_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    @ResponseStatus(HttpStatus.OK)
    public Map search(@Email
                   @RequestParam("email")
                   String email) {
        return emailMessage(email);
    }
}
```

An important thing to note here is that using `@Valid` annotation results in `MethodArgumentNotValidException` being thrown when validation fails, but `@Validated` results in `ConstraintViolationException` being thrown. Since these exceptions have different ways of abstracting the error messages associated with validation, it is important to have different error handlers for both of these. An example pattern using `ExceptionHandler` will be as follows:

```java
@ControllerAdvice
@Component
public class GlobalExceptionHandler {
    @ExceptionHandler
    @ResponseBody
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map handle(MethodArgumentNotValidException exception) {
        return error(exception.getBindingResult().getFieldErrors()
                .stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.toList()));
    }


    @ExceptionHandler
    @ResponseBody
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map handle(ConstraintViolationException exception) {
        return error(exception.getConstraintViolations()
                .stream()
                .map(ConstraintViolation::getMessage)
                .collect(Collectors.toList()));
    }

    private Map error(Object message) {
        return Collections.singletonMap("error", message);
    }
}

```
