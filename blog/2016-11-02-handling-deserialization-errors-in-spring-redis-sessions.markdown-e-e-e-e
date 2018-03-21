---
Categories:
- development
- java
- spring
- redis
Description: ""
Tags:
- development
- java
- spring
- redis
date: 2016-11-02T13:10:33-07:00
image: "img/redis-spring-boot.png"
title: Handling Deserialization errors in Spring Redis Sessions
---
One of the challenges of using storing spring sessions in Redis is that the objects that gets stored as part of a session often undergoes changes as the application evolves and these changes cause de-serialization exceptions to be thrown after a deployment when a session created before the deployment is presented to the application. This blog post discusses a method to work around this issue.

<!--more-->

## The issue
Consider an application that uses a custom authentication service to validate credentials presented by a client. To achieve this, we will wire up a custom authentication provider which creates an object `Customer` as the authenticated user in session.
```java
public class Customer extends User {
  public Customer(String name) {
    super(name, "", Collections.singletonList(new SimpleGrantedAuthority("USER")));
  }
}
```
Things work great, but after a while the team decides to store the logged in user's email address in the session. To achieve this, we change the `Customer` type to:
```java
public class Customer extends User {
  private String email;

  public Customer(String name, String email) {
    super(name, "", Collections.singletonList(new SimpleGrantedAuthority("USER")));
    this.email = email;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }
}
```
When this code is deployed and a user tries to access a protected resource by presenting a session created before the deployment, an exception is thrown.
```
org.springframework.data.redis.serializer.SerializationException: Cannot deserialize; nested exception is org.springframework.core.serializer.support.SerializationFailedException: Failed to deserialize payload. Is the byte array a result of corresponding serialization for DefaultDeserializer?; nested exception is java.io.InvalidClassException: in.sdqali.spring.vo.Customer; local class incompatible: stream classdesc serialVersionUID = 5161850915957547690, local class serialVersionUID = 1045726772100761661
```
This happens because the serialized object in the session and the current structure of the session differ.
{{< mailchimp >}}
## Solutions
This issue was raised on the Spring Session issue tracker [^1] and there were a lot of work-arounds discussed. Of the work arounds, wrapping the session repository offers the least disruption to the end user.
This approach ensures that every time a de-serialization error is thrown while trying to read an object from the session, that object is deleted, preventing subsequent errors.

```java
public class SafeDeserializationRepository<S extends ExpiringSession> implements SessionRepository<S> {
  private final SessionRepository<S> delegate;
  private final RedisTemplate<Object, Object> redisTemplate;

  private static final String BOUNDED_HASH_KEY_PREFIX = "spring:session:sessions:";
  private static final Logger logger = getLogger(SafeDeserializationRepository.class);

  public SafeDeserializationRepository(SessionRepository<S> delegate,
                                       RedisTemplate<Object, Object> redisTemplate) {
    this.delegate = delegate;
    this.redisTemplate = redisTemplate;
  }

  @Override
  public S createSession() {
    return delegate.createSession();
  }

  @Override
  public void save(S session) {
    delegate.save(session);
  }

  @Override
  public S getSession(String id) {
    try {
      return delegate.getSession(id);
    } catch(SerializationException e) {
      logger.info("Deleting non-deserializable session with key {}", id);
      redisTemplate.delete(BOUNDED_HASH_KEY_PREFIX + id);
      return null;
    }
  }

  @Override
  public void delete(String id) {
    delegate.delete(id);
  }
}
```
However, it is not easy to wire up this repository in the configuration. Since Spring Redis Session is auto configured, the only way to override beans for Redis Session is to extend `RedisHttpSessionConfiguration` and specify beans. Ideally, we want to override the method `RedisHttpSessionConfiguration#sessionRepository`. This would mean that `SafeDeserializationRepository` inherits from `RedisOperationsSessionRepository`. That does not sound too complicated till you realize that `RedisOperationsSessionRepository#getSession(java.lang.String)` returns `RedisSession` which is a final class declared inside `RedisOperationsSessionRepository`.

On closer look, the repository is hooked in to `SessionRepositoryFilter` and it is indeed possible to override the `SpringHttpSessionConfiguration#springSessionRepositoryFilter` method to create a new filter that takes our `SafeDeserializationRepository`.

```java
@Configuration
public class RedisSessionConfig extends RedisHttpSessionConfiguration {
  @Autowired
  RedisTemplate<Object, Object> redisTemplate;

  @Bean
  @Override
  public <S extends ExpiringSession> SessionRepositoryFilter<? extends ExpiringSession> springSessionRepositoryFilter(SessionRepository<S> sessionRepository) {
    return super.springSessionRepositoryFilter(new SafeDeserializationRepository<>(sessionRepository, redisTemplate));
  }
}
```


[^1]: [SerializationFailedException after re-deploying with changed session object #280](https://github.com/spring-projects/spring-session/issues/280).
