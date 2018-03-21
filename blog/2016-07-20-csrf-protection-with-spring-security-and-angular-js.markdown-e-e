---
Categories:
- development
Description: ""
Tags:
- development
date: 2016-07-20T21:57:01-04:00
image: "images/angular-spring-boot.png"
title: CSRF Protection with Spring Security and Angular JS
---
Both Spring Security and Angular JS provide support for CSRF protection. However, getting these to work together to provide protection from CSRF requires some non-obvious configuration. This blog post explains how to add CSRF protection to an application that uses Spring Security with an Angular JS front end.
<!--more-->

Cross-Site Request Forgery (CSRF) [^1] is an attack that forces an end user to execute unwanted actions on a web application in which they're currently authenticated. This blog post implements the CSRF token part of the protection described by OWASP. The application still needs to have protection to enforce the right Origin for requests.

### Front end

For this example, we will build a simple Spring Boot application with an Angular front end. The front end is based on the application we built for the [series](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/) on authentication with JWT. The changes are in how the initial authentication is done - we will be using Basic Auth in this example to perform the initial authentication.

This involves changing the `LoginService` to this:
```javascript
(function(angular) {
  var LoginFactory = function($http) {
    return function(credentials, success, error) {
      $http({
        method: 'POST',
        url: '/login',
        headers: {
          Authorization: "Basic " + btoa(credentials.username + ":" + credentials.password)
        }
      }).then(function (resp) {
        success(resp.data, resp.headers())
      }, error);
    };
  };

  LoginFactory.$inject = ['$http'];
  angular.module('jwtDemo.services').factory('Login', LoginFactory);

  var HelloFactory = function($resource) {
    return $resource('/hello', {}, {
      hello: {
        method: 'GET'
      }
    });
  };

  HelloFactory.$inject = ['$resource'];
  angular.module('jwtDemo.services').factory('Hello', HelloFactory);}(angular));
```

And the controllers are changed to use these services.
```javascript
(function(angular) {
  var LoginController = function($scope, $localStorage, $http, $location, Login) {
    $scope.login = function(username, password) {
      new Login({username: username, password: password},
          function (data, headers) {
            $localStorage.user = data.user;
            $localStorage.authToken = headers['x-auth-token'];
            $http.defaults.headers.common['x-auth-token'] = headers['x-auth-token'];
            $location.path("/");
          }, function (error) {
            console.log(error);
          });
    };

    $scope.logout = function () {
      delete $localStorage.user;
      delete $localStorage.authToken;
      $http.defaults.headers.common = {};
    }

    $scope.logout();
  };

  LoginController.$inject = ['$scope', '$localStorage', '$http', '$location','Login'];
  angular.module("jwtDemo.controllers").controller("LoginController", LoginController);


  var ProfileController = function ($scope, $localStorage, Hello) {
    $scope.profile = $localStorage.user;
    new Hello().$hello(function (resp, headers) {
      $scope.greeting = resp.message;
    }, function (error) {
      console.log(error);
    })
  };
  ProfileController.inject = ['$scope', '$localStorage', 'Hello'];
  angular.module("jwtDemo.controllers").controller("ProfileController", ProfileController);
  }(angular));
```

It can be noted that there are no CSRF specific code in there. We will be relying on Angular's CSRF (or XSRF as Angular refers to it) protection.

### The back end

The main API returns a greeting:
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

We also have an end point that clients can authenticate against and it returns the currently authenticated user:
```java
@RestController
@RequestMapping("/login")
public class LoginController {
  @RequestMapping(method = POST,
      path = "",
      produces = APPLICATION_JSON_VALUE)
  public Map<String, Object> login(Authentication auth) {
    return Collections.singletonMap("user", auth.getName());
  }
}
```

### Security

In this example, we will be using an in-memory authentication. We will also be using a header based session instead of a Cookie based session by wiring up `HeaderHttpSessionStrategy`. Sessions are stored in-memory using `MapSessionRepository`. We also secure all end points except the front end components and the `/login` end point.
```java
@EnableWebSecurity
@Configuration
@EnableSpringHttpSession
public class SecurityConfig extends WebSecurityConfigurerAdapter {
  @Override
  protected void configure(HttpSecurity http) throws Exception {
    String[] patterns = new String[] {
        "/",
        "/login",
        "/bower_components/**/*",
        "/app/**/*",
        "/index.html",
        "/home.html",
        "/signin.html",
        "/favicon.ico"
    };

    http
        .authorizeRequests()
        .antMatchers(patterns)
        .permitAll()
        .antMatchers("/hello/**")
        .hasRole("USER")
        .and()
        .csrf()
        .disable()
        .httpBasic();
  }

  @Autowired
  public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
    auth
        .inMemoryAuthentication()
        .withUser("user").password("password").roles("USER");
  }

  @Bean
  public SessionRepository sessionRepository() {
    return new MapSessionRepository();
  }

  @Bean
  public HeaderHttpSessionStrategy sessionStrategy() {
    return new HeaderHttpSessionStrategy();
  }
}
```

With this in place, access to the end point `/hello` is not permitted unless authenticated.

```bash
$ curl -s -X GET "http://localhost:8080/hello" | jq .
{
  "timestamp": 1469068247812,
  "status": 401,
  "error": "Unauthorized",
  "message": "Full authentication is required to access this resource",
  "path": "/hello"
}

$ curl -s -v -X POST "http://localhost:8080/login" -uuser:password | jq .
*   Trying ::1...
* Connected to localhost (::1) port 8080 (#0)
* Server auth using Basic with user 'user'
> POST /login HTTP/1.1
> Host: localhost:8080
> Authorization: Basic dXNlcjpwYXNzd29yZA==
> User-Agent: curl/7.43.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: Apache-Coyote/1.1
< X-Content-Type-Options: nosniff
< X-XSS-Protection: 1; mode=block
< Cache-Control: no-cache, no-store, max-age=0, must-revalidate
< Pragma: no-cache
< Expires: 0
< X-Frame-Options: DENY
< x-auth-token: 4ec4c614-0dc8-4e64-afa6-bd0ac03517b5
< Content-Type: application/json;charset=UTF-8
< Transfer-Encoding: chunked
< Date: Thu, 21 Jul 2016 02:31:10 GMT
<
{ [18 bytes data]
* Connection #0 to host localhost left intact
{
  "user": "user"
}

$ curl -s -X GET "http://localhost:8080/hello" -H "x-auth-token: 4ec4c614-0dc8-4e64-afa6-bd0ac03517b5" | jq .
{
  "message": "hello"
}
```

### Enabling CSRF protection

In Spring Security, CSRF protection can be enabled by replacing `csrf().disable()` with `.csrf()`.
```java
    http
        .authorizeRequests()
        .antMatchers(patterns)
        .permitAll()
        .antMatchers("/hello/**")
        .hasRole("USER")
        .and()
        .csrf()
        .and()
        .httpBasic();
```
With this in place however, we notice that all end points, including static assets and the login end point need CSRF protection tokens to access.
```bash
$ curl -s -X POST "http://localhost:8080/login" -uuser:password | jq .
{
  "timestamp": 1469068611814,
  "status": 403,
  "error": "Forbidden",
  "message": "Expected CSRF token not found. Has your session expired?",
  "path": "/login"
}
```
### Protecting URLs selectively

We want a mechanism to specify a list of URL patterns for which CSRF protection need to be turned OFF. Spring Security provides a `requireCsrfProtectionMatcher` method. With this, we will add a matcher that returns false when any of the URL patters we have matches the current request's path.
```java
http
        .authorizeRequests()
        .antMatchers(patterns)
        .permitAll()
        .antMatchers("/hello/**")
        .hasRole("USER")
        .and()
        .csrf()
        .requireCsrfProtectionMatcher(new NoAntPathRequestMatcher(patterns))
        .and()
        .httpBasic();
```

The `NoAntPathRequestMatcher` can be implemented as a combination of two request matchers provided by Spring - `NegatedRequestMatcher` and `AndRequestMatcher`:
```java
public class NoAntPathRequestMatcher implements RequestMatcher {
  private final AndRequestMatcher andRequestMatcher;

  public NoAntPathRequestMatcher(String[] patterns) {
    List<RequestMatcher> requestMatchers = Arrays.asList(patterns)
        .stream()
        .map(p -> new NegatedRequestMatcher(new AntPathRequestMatcher(p)))
        .collect(Collectors.toList());

    andRequestMatcher = new AndRequestMatcher(requestMatchers);
  }

  @Override
  public boolean matches(HttpServletRequest request) {
    return andRequestMatcher.matches(request);
  }
}
```
With this in place, we should be able to authenticate.
```bash
$ curl -s -v -X POST "http://localhost:8080/login" -uuser:password | jq .
*   Trying ::1...
* Connected to localhost (::1) port 8080 (#0)
* Server auth using Basic with user 'user'
> POST /login HTTP/1.1
> Host: localhost:8080
> Authorization: Basic dXNlcjpwYXNzd29yZA==
> User-Agent: curl/7.43.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: Apache-Coyote/1.1
< X-Content-Type-Options: nosniff
< X-XSS-Protection: 1; mode=block
< Cache-Control: no-cache, no-store, max-age=0, must-revalidate
< Pragma: no-cache
< Expires: 0
< X-Frame-Options: DENY
< x-auth-token: c5af3ea9-e3f8-4425-a6e8-de35588af0ca
< Content-Type: application/json;charset=UTF-8
< Transfer-Encoding: chunked
< Date: Thu, 21 Jul 2016 02:44:28 GMT
<
{ [18 bytes data]
* Connection #0 to host localhost left intact
{
  "user": "user"
}
```
But we do not see anything in the response that tells the client what the token allocated to it for the current session is. This is because Spring Security's CSRF protection by default provides enforcement and allocation of tokens, but it does not expose the token granted to the client out of the box.

### Granting CSRF Token to the client
One way to grant the client the CSRF token allocated to the current session will be to add a filter that sets the token as a Cookie once it is available. For this, we will add a filter immediately after the session is assigned by Spring Security's `SessionManagementFilter`.
```java
    http
        .authorizeRequests()
        .antMatchers(patterns)
        .permitAll()
        .antMatchers("/hello/**")
        .hasRole("USER")
        .and()
        .csrf()
        .requireCsrfProtectionMatcher(csrfProtectionMatcher(patterns))
        .and()
        .httpBasic()
        .and()
        .addFilterAfter(new CsrfGrantingFilter(), SessionManagementFilter.class);
```
The filter is implemented as follows:
```java
public class CsrfGrantingFilter implements Filter {
  @Override
  public void init(FilterConfig filterConfig) throws ServletException {}

  @Override
  public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
      throws IOException, ServletException {
    CsrfToken csrf = (CsrfToken) servletRequest.getAttribute(CsrfToken.class.getName());
    String token = csrf.getToken();
    if (token != null && isAuthenticating(servletRequest)) {
      HttpServletResponse response = (HttpServletResponse) servletResponse;
      Cookie cookie = new Cookie("CSRF-TOKEN", token);
      cookie.setPath("/");
      response.addCookie(cookie);
    }
    filterChain.doFilter(servletRequest, servletResponse);
  }

  private boolean isAuthenticating(ServletRequest servletRequest) {
    HttpServletRequest request = (HttpServletRequest) servletRequest;
    return request.getRequestURI().equals("/login");
  }

  @Override
  public void destroy() {}
}
```
The filter checks to see if the current request has a CSRF token set on it by Spring Security's `CsrfFilter` and then sets it as a Cookie on the response, if the current request was made by a client to authenticate.

With this filter in place, when we authenticate, we will see the following behavior:
```bash
$ curl -I -X POST "http://localhost:8080/login" -uuser:password
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Set-Cookie: CSRF-TOKEN=628ae2c8-f35b-49a4-acc7-04fe87bdb98e; Path=/
x-auth-token: 9444d058-eccb-471d-bc0d-460fd4c968e8
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Date: Thu, 21 Jul 2016 02:51:19 GMT
```
We can clearly see that the CSRF token is sent to the client as a Cookie. At this point, we can make changes to our front end to send this token with every subsequent request. However, it is easier to use Angular's support for CSRF tokens.

### Customizing CSRF protection for Angular
Angular's CSRF protection [^2] uses the cookie `XSRF-TOKEN` it expects from server responses and the header `X-XSRF-TOKEN` which it will send for every subsequent request, once the Cookie is found in a response. We will have to configure Spring Security to use this header and token instead of it's default header `X-CSRF-TOKEN` and Cookie name `CSRF-TOKEN`.

The first step is to pass Spring Security a custom `CsrfTokenRepository`:
```java
    http
        .authorizeRequests()
        .antMatchers(patterns)
        .permitAll()
        .antMatchers("/hello/**")
        .hasRole("USER")
        .and()
        .csrf()
        .csrfTokenRepository(csrfTokenRepository())
        .requireCsrfProtectionMatcher(csrfProtectionMatcher(patterns))
        .and()
        .httpBasic()
        .and()
        .addFilterAfter(new CsrfGrantingFilter(), SessionManagementFilter.class);

```
The `CsrfTokenRepository` is configured with the right header:
```java
  private CsrfTokenRepository csrfTokenRepository() {
    HttpSessionCsrfTokenRepository repository = new HttpSessionCsrfTokenRepository();
    repository.setHeaderName("X-XSRF-TOKEN");
    return repository;
  }
```
The next step is to set the Cookie with the right name in the `CsrfGrantingFilter`:
```java
public class CsrfGrantingFilter implements Filter {

  @Override
  public void init(FilterConfig filterConfig) throws ServletException {}

  @Override
  public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
      throws IOException, ServletException {
    CsrfToken csrf = (CsrfToken) servletRequest.getAttribute(CsrfToken.class.getName());
    String token = csrf.getToken();
    if (token != null && isAuthenticating(servletRequest)) {
      HttpServletResponse response = (HttpServletResponse) servletResponse;
      Cookie cookie = new Cookie("XSRF-TOKEN", token);
      cookie.setPath("/");
      response.addCookie(cookie);
    }
    filterChain.doFilter(servletRequest, servletResponse);
  }

  private boolean isAuthenticating(ServletRequest servletRequest) {
    HttpServletRequest request = (HttpServletRequest) servletRequest;
    return request.getRequestURI().equals("/login");
  }

  @Override
  public void destroy() {}
}
```

With these configurations in place, the front end is able to authenticate and obtain a token Cookie which Angular will pass for every subsequent request.

### Configuring order of enforcement
The only drawback to the configurations we have developed so far is that when a client makes a request to a protected end point with out Authentication and CSRF token, it will receive a `403 Forbidden` instead of a `401 Unauthorized`.
```bash
$ curl -I -X GET "http://localhost:8080/hello"
HTTP/1.1 403 Forbidden
Server: Apache-Coyote/1.1
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
x-auth-token: a0abe09c-94cb-4966-9ee6-a5327f3bd939
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Date: Thu, 21 Jul 2016 03:16:01 GMT
```

This happens because by default, when CSRF protection is enabled, `CsrfFilter` appears in the filter chain before `FilterSecurityInterceptor`. For this example, this is the order:
```
0 = {WebAsyncManagerIntegrationFilter@7344}
1 = {SecurityContextPersistenceFilter@7343}
2 = {HeaderWriterFilter@7342}
3 = {CsrfFilter@7339}
4 = {LogoutFilter@7382}
5 = {BasicAuthenticationFilter@7381}
6 = {RequestCacheAwareFilter@8965}
7 = {SecurityContextHolderAwareRequestFilter@8964}
8 = {AnonymousAuthenticationFilter@8963}
9 = {SessionManagementFilter@8962}
10 = {CsrfGrantingFilter@8978}
11 = {ExceptionTranslationFilter@9333}
12 = {FilterSecurityInterceptor@9334}
```
If this is not the behavior desirable for your application, we can disable the default CSRF protection and enable the required filters, enforcing the right order. This is achieved with the following configuration:
```java
    http
        .authorizeRequests()
        .antMatchers(patterns)
        .permitAll()
        .antMatchers("/hello/**")
        .hasRole("USER")
        .and()
        .csrf()
        .disable()
        .httpBasic()
        .and()
        .addFilterAfter(csrfFilter(patterns), FilterSecurityInterceptor.class)
        .addFilterAfter(new CsrfGrantingFilter(), CsrfFilter.class);

```

The CSRF filter is built with the right repository and URL matchers:

```java
  private Filter csrfFilter(String[] patterns) {
    CsrfFilter csrfFilter = new CsrfFilter(csrfTokenRepository());
    csrfFilter.setRequireCsrfProtectionMatcher(csrfProtectionMatcher(patterns));
    return csrfFilter;
  }

  private NoAntPathRequestMatcher csrfProtectionMatcher(String[] patterns) {
    return new NoAntPathRequestMatcher(patterns);
  }

  private CsrfTokenRepository csrfTokenRepository() {
    HttpSessionCsrfTokenRepository repository = new HttpSessionCsrfTokenRepository();
    repository.setHeaderName("X_XSRF_TOKEN");
    return repository;
  }
```
This will result in the right order of errors:

```bash
$ curl -I -X GET "http://localhost:8080/hello"
HTTP/1.1 401 Unauthorized
Server: Apache-Coyote/1.1
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
WWW-Authenticate: Basic realm="Realm"
x-auth-token: 08a06acd-3398-4fc4-af25-23d3f4155a2b
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Date: Thu, 21 Jul 2016 03:27:58 GMT

```
This is the end of this blog post. In this example, we built an application with CSRF protection that works well with Angular JS. The code for this blog post is available [on GitHub](https://github.com/sdqali/csrf-demo).

[^1]: For a detailed explanation, see Cross-Site Request Forgery (CSRF) [on OWASP](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)).
[^2]: See section _Cross Site Request Forgery (XSRF) Protection_ in [the official documentation](https://docs.angularjs.org/api/ng/service/$http).
