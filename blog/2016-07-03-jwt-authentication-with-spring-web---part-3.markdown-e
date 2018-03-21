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
date: 2016-07-05T22:30:53-07:00
image: "images/spring-security.png"
title: JWT authentication with Spring Web - Part 3
---
In the [previous blog post](/blog/2016/07/03/jwt-authentication-with-spring-web---part-2/), we built the Spring API that responds with Profile information. Continuing on the path to building authentication with JWT, in this blog post, we will create a login mechanism that issues a JWT when the user presents the correct credentials.

<!--more-->
These are the blog posts in this series:

* [Part 1](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/) - Discussion of JWT and implementation
* [Part 2](/blog/2016/07/03/jwt-authentication-with-spring-web---part-2/) - A Spring User Profiles API
* [Part 3](/blog/2016/07/05/jwt-authentication-with-spring-web---part-3/) - Issuing a token from the server
* [Part 4](/blog/2016/07/07/jwt-authentication-with-spring-web---part-4/) - Verifying the token sent back by the client
* [Part 5](/blog/2016/07/13/jwt-authentication-with-spring-web---part-5/) - Securing the front end

Our fist step is to configure Spring Security to allow access to the login end point we will be building. This can be done as follows:

```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().ignoringAntMatchers("/login");

        http.authorizeRequests()
                .antMatchers("/login")
                .permitAll()
                .antMatchers("/**/*")
                .denyAll();
    }
}
```
We are turning off authentication and CSRF token checking for the `/login` end point.

Next, we build a `LoginController` to issue tokens up on a user presenting valid credentials:

```java
@RestController
@RequestMapping(path = "/login")
public class LoginController {

    private final LoginService loginService;
    private final JwtService jwtService;

    @SuppressWarnings("unused")
    public LoginController() {
        this(null, null);
    }

    @Autowired
    public LoginController(LoginService loginService, JwtService jwtService) {
        this.loginService = loginService;
        this.jwtService = jwtService;
    }

    @RequestMapping(path = "",
            method = POST,
            produces = APPLICATION_JSON_VALUE)
    public MinimalProfile login(@RequestBody LoginCredentials credentials,
                                HttpServletResponse response) {
        return loginService.login(credentials)
                .map(minimalProfile -> {
                    try {
                        response.setHeader("Token", jwtService.tokenFor(minimalProfile));
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                    return minimalProfile;
                })
                .orElseThrow(() -> new FailedToLoginException(credentials.getUsername()));
    }
}
```

We use the login service to verify the credentials and it returns an `Optional<MinimalProfile>`. If there is a valid `MinimalProfile`, we ask the `JwtService` to issue a token.
{{< mailchimp >}}
The `LoginService` uses the `ProfileService` to load a profile matching the user name and the password presented by the user.

```java
@Component
public class LoginService {

    private ProfileService profileService;

    @SuppressWarnings("unused")
    public LoginService() {
        this(null);
    }

    @Autowired
    public LoginService(ProfileService profileService) {
        this.profileService = profileService;
    }

    public Optional<MinimalProfile> login(LoginCredentials credentials) {
        return profileService.get(credentials.getUsername())
                .filter(profile -> profile.getLogin().getPassword().equals(credentials.getPassword()))
                .map(profile -> new MinimalProfile(profile));
    }
}
```
Please note that in real applications, you never want to do this. You should be comparing the hashed version of the password presented by the user with the hashed version of the password stored in the database.

The `JwtService` creates a token using the profile information and an expiration date of 2 hours with the `HMASHA256` algorithm. It uses the key provided by `SecretKeyProvider`. For creating the JWT token, we use the excellent jjwt [^1] library we introduced in [part 1](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/).

```java
@Component
public class JwtService {
    private static final String ISSUER = "in.sdqali.jwt";
    private SecretKeyProvider secretKeyProvider;

    @SuppressWarnings("unused")
    public JwtService() {
        this(null);
    }

    @Autowired
    public JwtService(SecretKeyProvider secretKeyProvider) {
        this.secretKeyProvider = secretKeyProvider;
    }

    public String tokenFor(MinimalProfile minimalProfile) throws IOException, URISyntaxException {
        byte[] secretKey = secretKeyProvider.getKey();
        Date expiration = Date.from(LocalDateTime.now().plusHours(2).toInstant(UTC));
        return Jwts.builder()
                .setSubject(minimalProfile.getUsername())
                .setExpiration(expiration)
                .setIssuer(ISSUER)
                .signWith(SignatureAlgorithm.HS512, secretKey)
                .compact();
    }
}
```

The `SecretKeyProvider` in this example will simply load the secret key from a file, where it is stored in plain text. In a real application, you may store and encrypted version of it and decrypt it when required.

```java
@Component
public class SecretKeyProvider {
    public byte[] getKey() throws URISyntaxException, IOException {
        return Files.readAllBytes(Paths.get(this.getClass().getResource("/jwt.key").toURI()));
    }
}
```

With this code, a client can authenticate and receive a JWT. When request is made with correct username and password:

```
$ curl -v -X POST "http://localhost:8080/login" -d '{"username":"greenrabbit948", "password":"celeste"}' --header "Content-Type: application/json"   | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying ::1...
* Connected to localhost (::1) port 8080 (#0)
> POST /login HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.43.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 51
>
} [51 bytes data]
* upload completely sent off: 51 out of 51 bytes
< HTTP/1.1 200 OK
< Server: Apache-Coyote/1.1
< X-Content-Type-Options: nosniff
< X-XSS-Protection: 1; mode=block
< Cache-Control: no-cache, no-store, max-age=0, must-revalidate
< Pragma: no-cache
< Expires: 0
< X-Frame-Options: DENY
< Token: eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqd3QtZGVtbyIsImV4cCI6MTQ2Nzc2Njk3MSwiaXNzIjoiaW4uc2RxYWxpLmp3dCJ9.eu_OuBIkc4BfcTsTu4t_6TCwyLkH4HcuQzvWIMzNQYdxXiWA77SfvwCe4mdc7C17mXdtBAsvFGDj7A9fzI0M1w
< Content-Type: application/json;charset=UTF-8
< Transfer-Encoding: chunked
< Date: Wed, 06 Jul 2016 06:02:51 GMT
<
{ [164 bytes data]
100   211    0   160  100    51  15071   4804 --:--:-- --:--:-- --:--:-- 16000
* Connection #0 to host localhost left intact
{
  "username": "greenrabbit948",
  "name": {
    "title": "miss",
    "first": "dionaura",
    "last": "rodrigues"
  },
  "thumbnail": "https://randomuser.me/api/portraits/thumb/women/78.jpg"
}
```
We can see the `Token` header has value `eyJhbGciOiJIUzUxMiJ9.
eyJzdWIiOiJqd3QtZGVtbyIsImV4cCI6MTQ2Nzc2Njk3MSwiaXNzIjoiaW4uc2RxYWxpLmp3dCJ9.
eu_OuBIkc4BfcTsTu4t_6TCwyLkH4HcuQzvWIMzNQYdxXiWA77SfvwCe4mdc7C17mXdtBAsvFGDj
7A9fzI0M1w`.

If we were to present invalid credentials, the API will return a `401`:

```
$ curl -i -X POST "http://localhost:8080/login" -d '{"username":"greenrabbit948", "password":"wrongpassword"}' --header "Content-Type: application/json"
HTTP/1.1 401 Unauthorized
Server: Apache-Coyote/1.1
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Content-Length: 0
Date: Wed, 06 Jul 2016 06:05:46 GMT
```

In the next blog post, the fourth is this series, we will move on to verifying the token presented by the client for subsequent requests. The source code for this example for the progress made from part 1 through part 3 is available on [GitHub](https://github.com/sdqali/jwt-demo/tree/09b02336e4b7c746cb4c134dc020243aef827b66).

[^1]: jjwt - Java JWT: JSON Web Token for Java and Android, available on [GitHub](https://github.com/jwtk/jjwt).
