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
date: 2016-07-03T09:22:53-07:00
image: "images/spring-security.png"
title: JWT authentication with Spring Web - Part 2
---
In the [previous blog post](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/) in this series, we looked at the basics of JWT. We will move on to building the Spring API that we will use JWT for authentication in this blog post.

<!--more-->
These are the blog posts in this series:

* [Part 1](/blog/2016/07/02/jwt-authentication-with-spring-web---part-1/) - Discussion of JWT and implementation
* [Part 2](/blog/2016/07/03/jwt-authentication-with-spring-web---part-2/) - A Spring User Profiles API
* [Part 3](/blog/2016/07/05/jwt-authentication-with-spring-web---part-3/) - Issuing a token from the server
* [Part 4](/blog/2016/07/07/jwt-authentication-with-spring-web---part-4/) - Verifying the token sent back by the client
* [Part 5](/blog/2016/07/13/jwt-authentication-with-spring-web---part-5/) - Securing the front end

## The API

The API we will be using in the example gives access to user profiles. It has the following end points:

* GET /profiles/{:username}
* GET /profiles/details/{:username}

The profiles that we use for this example were generated using the [Random User Generator](https://randomuser.me/) and stored in a JSON file, for convenience for this example. In the real world, you never want to store user information in a file. All the code for this example is available on [GitHub](https://github.com/sdqali/jwt-demo).

## Structure of the User Profile

For this example, I specifically generated 500 random profiles with only a subset of fields - `name`, `email`, `login` and `picture`. With these fields, a profile has the following structure:

```json
{
  "name": {
    "title": "mr",
    "first": "matt",
    "last": "hahn"
  },
  "email": "matt.hahn@example.com",
  "login": {
    "username": "greenostrich307",
    "password": "darkange",
    "salt": "V5xi38lN",
    "md5": "cba0d5fb77ae3e0dbe177b9624df5ceb",
    "sha1": "5f22fdcc79affdef604d89b64b7db599ed454c5e",
    "sha256": "23afb0983e874169669f96cd72b69234aef4cf54a86f89a25e14e91941ac95a2"
  },
  "picture": {
    "large": "https://randomuser.me/api/portraits/men/20.jpg",
    "medium": "https://randomuser.me/api/portraits/med/men/20.jpg",
    "thumbnail": "https://randomuser.me/api/portraits/thumb/men/20.jpg"
  }
}
```
At this point, you can see the password and hash in there. As I explained above, you _do not_ want to do this in a real application. As such, this example focuses on JWT and we are doing this purely for convenience.

## The data models

The models for representing the data provided from the random user generator are as follows. We will be using the Lombok [^1] `@Data` annotation to stay away from having to write explicit setters and getters.

### Profile
```java
import lombok.Data;

@Data
public class Profile {
    private Name name;
    private String email;
    private Login login;
    private Picture picture;
}
```

### Name
```java
@Data
public class Name {
    private String title;
    private String first;
    private String last;
}
```

### Login
```java
@Data
public class Login {
    String username;
    String password;
    String salt;
    String md5;
    String sha1;
    String sha256;
}
```

### Picture
```java
@Data
public class Picture {
    private URL large;
    private URL medium;
    private URL thumbnail;
}
```

We will also create two other data models that expose a minimal set of profile information without the credentials.

### MinimalProfile
```java
@Data
public class MinimalProfile {
    private final String username;
    private final Name name;
    private final URL thumbnail;

    public MinimalProfile(Profile profile) {
        name = profile.getName();
        username = profile.getLogin().getUsername();
        thumbnail = profile.getPicture().getThumbnail();
    }
}
```

### DetailedProfile
```java
@Data
public class DetailedProfile {

    private final Picture picture;
    private final Name name;
    private final String email;
    private final String username;

    public DetailedProfile(Profile profile) {
        name = profile.getName();
        email = profile.getEmail();
        picture = profile.getPicture();
        username = profile.getLogin().getUsername();
    }
}
```


## The Controllers

The code for the API's controller is as follows:

```java
@RestController
@RequestMapping(path = "/profile")
public class ProfileController {

    private final ProfileService profileService;

    @SuppressWarnings("unused")
    public ProfileController() {
        this(null);
    }

    @Autowired
    public ProfileController(ProfileService profileService) {
        this.profileService = profileService;
    }

    @RequestMapping(path = "/{username}",
            method = GET,
            produces = APPLICATION_JSON_VALUE)
    public MinimalProfile minimal(@PathVariable String username) {
        return profileService.minimal(username)
                .orElseThrow(() -> new ProfileNotFoundException(username));
    }

    @RequestMapping(path = "/details/{username}",
            method = GET,
            produces = APPLICATION_JSON_VALUE)
    public DetailedProfile details(@PathVariable String username) {
        return profileService.detailed(username)
                .orElseThrow(() -> new ProfileNotFoundException(username));
    }
}
```
It delegates querying for profiles to the `ProfileService` and throws exceptions if a Profile is not present. Notice the use of Java's `Optional` to throw exceptions.
{{< mailchimp >}}
### The ProfileService

```java
@Component
public class ProfileService {
    private final List<Profile> profiles;

    private final Path PROFILES_FILE = Paths.get(this.getClass().getResource("/profiles.json").toURI());

    public ProfileService() throws IOException, URISyntaxException {
        ObjectMapper objectMapper = new ObjectMapper();
        profiles = objectMapper.readValue(PROFILES_FILE.toFile(), new TypeReference<List<Profile>>() {
        });
    }

    protected Optional<Profile> get(String username) {
        return profiles.stream()
                .filter(profile -> profile.getLogin().getUsername().equals(username))
                .findFirst();
    }

    public Optional<MinimalProfile> minimal(String username) {
        return get(username).map(profile -> new MinimalProfile(profile));
    }

    public Optional<DetailedProfile> detailed(String username) {
        return get(username).map(profile -> new DetailedProfile(profile));
    }
}
```

### Exception Handling

We will also need to wire up a `ControllerAdvice` to handle exceptions appropriately:

```java

@ControllerAdvice
public class GlobalExceptionHandler {
    @ResponseStatus(NOT_FOUND)
    @ExceptionHandler(ProfileNotFoundException.class)
    public void profileNotFound() {
    }
}
```

With this, you should have a profile service up and running.

### Minimal profile
```
$ curl -s "http://localhost:8080/profile/yellowfrog347" | jq .
{
  "username": "yellowfrog347",
  "name": {
    "title": "ms",
    "first": "sofia",
    "last": "hansen"
  },
  "thumbnail": "https://randomuser.me/api/portraits/thumb/women/71.jpg"
}
```

### Detailed Profile
```
$ curl -s "http://localhost:8080/profile/details/yellowfrog347" | jq .
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

The code for the application so far can be found [here](https://github.com/sdqali/jwt-demo/tree/4f1da432a51fb8c88fc21a6fad895e03ca3611d9). In the next blog post of the series, we will wire up Spring Security and build a login feature that issues a JWT after successful login.

[^1]: [Project Lombok](https://projectlombok.org/index.html) is a Java library that helps minimize boiler plate code by replacing them with a set of convenient annotations. I tend to use it when I have to build data objects.
