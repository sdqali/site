---
Categories:
- development
- java
- spring
- jwt
- spring security
Description: ""
Tags:
- development
- java
- spring
- jwt
- spring security
series:
- spring-jwt
date: 2016-07-07T23:47:53-07:00
image: "images/jwt.jpg"
title: JWT authentication with Spring Web - Part 4
---
In parts 1 through 3 of this series, we built a Spring API that can issue a JWT when a user successfully authenticates. In this blog post, we will add the capability to verify the JWT presented by the client for subsequent requests.
<!--more-->
These are the blog posts in this series:

* [Part 1](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/) - Discussion of JWT and implementation
* [Part 2](/blog/2016/07/03/jwt-authentication-with-spring-web---part-2/) - A Spring User Profiles API
* [Part 3](/blog/2016/07/05/jwt-authentication-with-spring-web---part-3/) - Issuing a token from the server
* [Part 4](/blog/2016/07/07/jwt-authentication-with-spring-web---part-4/) - Verifying the token sent back by the client
* [Part 5](/blog/2016/07/13/jwt-authentication-with-spring-web---part-5/) - Securing the front end

We will start by configuring Spring security with a filter to capture the JWT passed by the client in the `Authorization` header. We will wire up this filter to go before the `UsernamePasswordAuthenticationFilter` provided by Spring security.

```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private JwtAuthFilter jwtAuthFilter;
    // ...

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable();

        http.authorizeRequests()
                .antMatchers("/login")
                .permitAll()
                .antMatchers("/**/*")
                .hasAuthority("ROLE_USER")
                .and()
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
                // ...
    }
```

The filter captures the `Authorization` header and creates a `JwtAuthToken` and sets that as the current authentication for the request.

```java
@Component
public class JwtAuthFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {

    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest servletRequest = (HttpServletRequest) request;
        String authorization = servletRequest.getHeader("Authorization");
        if (authorization != null) {
            JwtAuthToken token = new JwtAuthToken(authorization.replaceAll("Bearer ", ""));
            SecurityContextHolder.getContext().setAuthentication(token);
        }
        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {

    }
}
```
The `JwtAuthToken` is simply a conduit to carry the token and although it implements the `Authentication` interface, it does not do much.

```java
public class JwtAuthToken implements Authentication {
    private final String token;

    public JwtAuthToken(String token) {
        this.token = token;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return null;
    }

    @Override
    public Object getCredentials() {
        return token;
    }

    @Override
    public Object getDetails() {
        return null;
    }

    @Override
    public Object getPrincipal() {
        return null;
    }

    @Override
    public boolean isAuthenticated() {
        return false;
    }

    @Override
    public void setAuthenticated(boolean isAuthenticated) throws IllegalArgumentException {

    }

    @Override
    public String getName() {
        return null;
    }
}
```

At this point, we need to tell Spring Security how to verify the tokens. This can be done by providing a custom `AuthenticationProvider`. This can be done by overriding the `configure` method.

```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired
    private JwtAuthenticationProvider jwtAuthenticationProvider;

    // ...
    @Override
    public void configure(AuthenticationManagerBuilder auth)  throws Exception {
        auth.authenticationProvider(jwtAuthenticationProvider);
    }
    // ...
}
```

The `JwtAuthenticationProvider` receives the `Authentication` instance set on the `SecurityContext`, which in our case is the `JwtAuthToken` we set using the `JwtAuthFilter`. This token is then verified using the `JwtService`. If the token is valid, we return a `JwtAuthenticatedProfile` or throw an exception if it is invalid.

```java
@Component
public class JwtAuthenticationProvider implements AuthenticationProvider {
    private final JwtService jwtService;

    @SuppressWarnings("unused")
    public JwtAuthenticationProvider() {
        this(null);
    }

    @Autowired
    public JwtAuthenticationProvider(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        try {
            Optional<MinimalProfile> possibleProfile = jwtService.verify((String) authentication.getCredentials());
            return new JwtAuthenticatedProfile(possibleProfile.get());
        } catch (Exception e) {
            throw new JwtAuthenticationException("Failed to verify token", e);
        }
    }

    @Override
    public boolean supports(Class<?> authentication) {
        return JwtAuthToken.class.equals(authentication);
    }
}
```

`JwtAuthenticatedProfile` is another implementation of `Authentication` that wraps the user's profile information:

```java
public class JwtAuthenticatedProfile implements Authentication {

    private final MinimalProfile minimalProfile;

    public JwtAuthenticatedProfile(MinimalProfile minimalProfile) {
        this.minimalProfile = minimalProfile;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"));
    }

    @Override
    public Object getCredentials() {
        return null;
    }

    @Override
    public Object getDetails() {
        return null;
    }

    @Override
    public Object getPrincipal() {
        return null;
    }

    @Override
    public boolean isAuthenticated() {
        return true;
    }

    @Override
    public void setAuthenticated(boolean isAuthenticated) throws IllegalArgumentException {

    }

    @Override
    public String getName() {
        return minimalProfile.getUsername();
    }
}
```


Next, we implement the verify functionality in `JwtService`.

```java
    public Optional<MinimalProfile> verify(String token) throws IOException, URISyntaxException {
        byte[] secretKey = secretKeyProvider.getKey();
        Jws<Claims> claims = Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token);
        return profileService.minimal(claims.getBody().getSubject().toString());
    }
```
When we generated the JWT, we had set the username as the JWT subject.

The last thing to do is to ensure that we handle exceptions that occur during token verification gracefully. Since the token verification is happening outside controllers, we won't be able to leverage `ControllerAdvice` to handle exceptions. This is where Spring Security's `AuthenticationEntryPoint` comes in to play. We will configure a custom `AuthenticationEntryPoint` as follows:

```java
        http.authorizeRequests()
                .antMatchers("/login", "/bower_components/**/*", "/app/**/*", "/index.html")
                .permitAll()
                .antMatchers("/**/*")
                .hasAuthority("ROLE_USER")
                .and()
                .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
                .exceptionHandling()
                .authenticationEntryPoint(jwtAuthEndPoint);

```

Our entry point, sets the HTTP status to `403`, and sets the response body to a JSON showing the error.

```java
@Component
public class JwtAuthenticationEntryPoint implements AuthenticationEntryPoint {
    @Override
    public void commence(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, AuthenticationException e)
            throws IOException, ServletException {
        httpServletResponse.setStatus(SC_FORBIDDEN);
        httpServletResponse.setContentType(MediaType.APPLICATION_JSON_VALUE);

        String message;
        if(e.getCause() != null) {
            message = e.getCause().getMessage();
        } else {
            message = e.getMessage();
        }
        byte[] body = new ObjectMapper()
                .writeValueAsBytes(Collections.singletonMap("error", message));
        httpServletResponse.getOutputStream().write(body);
    }
}
```

With this configuration in place, we can request a token and make a subsequent request with the received JWT.

```
$ curl -i -X POST "http://localhost:8080/login" -d '{"username":"greenrabbit948", "password":"celeste"}' --header "Content-Type: application/json"
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJncmVlbnJhYmJpdDk0OCIsImV4cCI6MTQ2ODE0MDg1MiwiaXNzIjoiaW4uc2RxYWxpLmp3dCJ9.t9pqrOmYfaVkzuAQgo4D4VbN2PibQuHPuPA6RKYU-keTzbFAX58l77hQTc4Cq28HpjFOeiDvNpNEgilNHFOfVA
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Date: Sun, 10 Jul 2016 06:54:12 GMT

{"username":"greenrabbit948","name":{"title":"miss","first":"dionaura","last":"rodrigues"},"thumbnail":"https://randomuser.me/api/portraits/thumb/women/78.jpg"}

$ curl -s "http://localhost:8080/profile/details/yellowfrog347" --header "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJncmVlbnJhYmJpdDk0OCIsImV4cCI6MTQ2ODE0MDg1MiwiaXNzIjoiaW4uc2RxYWxpLmp3dCJ9.t9pqrOmYfaVkzuAQgo4D4VbN2PibQuHPuPA6RKYU-keTzbFAX58l77hQTc4Cq28HpjFOeiDvNpNEgilNHFOfVA" | jq .
{
  "picture": {
    "large": "https://randomuser.me/api/portraits/women/71.jpg",
    "medium": "https://randomuser.me/api/portraits/med/women/71.jpg",
    "thumbnail": "https://randomuser.me/api/portraits/thumb/women/71.jpg"
  },
  "name": {
    "title": "ms",
    "first": "sofia",
    "last": "hansen"
  },
  "email": "sofia.hansen@example.com",
  "username": "yellowfrog347"
}
```

If we were to make a request with an invalid JWT, we will receive an error:

```
$ curl -s "http://localhost:8080/profile/details/yellowfrog347" --header "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJncmVlbnJhYmJpdDk0OCIsImV4cCI6MTQ2ODE0MDg1MiwiaXNzIjoiaW4uc2RxYWxpLmp3dCJ9.t9pqrOmYfaVkzuAQgo4D4VbN2PibQuHPuPA6RKYU-keTzbFAX58l77hQTc4Cq28HpjFOeiDvNpNEgilNHFOfVAAAAAA" | jq .
{
  "error": "JWT signature does not match locally computed signature. JWT validity cannot be asserted and should not be trusted."
}

```

In the next blog post, the fifth is this series, we will move on to building the front end with Angular JS and managing authentication from the front end. The source code for this example for the progress made from part 1 through part 4 is available on [GitHub](https://github.com/sdqali/jwt-demo/tree/verify_tokens).
