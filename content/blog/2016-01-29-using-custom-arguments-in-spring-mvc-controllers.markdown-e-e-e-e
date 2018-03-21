---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
date: 2016-01-29T17:41:49-08:00
title: Using custom arguments in Spring MVC controllers
image: "images/spring-by-pivotal.png"
---
<meta content="spring, arguments, handlermethodargumentresolver, spring mvc, spring boot" name="keywords">
Most of the Spring controllers in the real world accept a lot of different types of parameters - Path variables, URL parameters, request headers, request body and sometimes even the entire HTTP Request object. This provides a flexible mechanism to create APIs. Spring is really good at parsing these parameters in to Java types as long as there is an ObjectMapper (like Jackson) configured to take care of the de-serialization.

However, there are situations where you want methods to receive a parameter of a particular type that has to resolved from a set of parameters–for example, an API can expect consumers to send meta data about a request in the form of headers and need a custom type to hold this information. Spring provides a convenient way to provide such custom arguments. This blog post explores this feature and how to implement it and test it.

<!--more-->
## Argument Resolvers

Spring uses argument resolvers to determine how to parse a particular argument required by a controller method from HTTP request body, the URL, URL parameters and HTTP headers. For example when a method expects a request header as in the following example, Spring uses a particular resolver named `RequestHeaderMethodArgumentResolver` to resolve this argument. All argument resolvers implement the `HandlerMethodArgumentResolver` interface whose contract is:

```java
public interface HandlerMethodArgumentResolver {
    boolean supportsParameter(MethodParameter parameter);
    Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer,
            NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception;
}
```
The `supportsParameter` method determines if this resolver is capable of parsing a given parameter and `resolveArgument` specifies how it‘s value should be computed. Notice how this method has the web `NativeWebRequest` argument passed to it to allow the look up of request parameters like body, url and headers.

For this example, the MetaData that we are interested in can be represented as a type:

```java
public class MetaData {
    @JsonProperty("data")
    private Map<String, String> map  = new HashMap<>();

    private MetaData() {
    }

    public MetaData(Map<String, String> map) {
        this.map = map;
    }

    public String get(String key) {
        return map.get(key);
    }
}
```

An argument resolver to compute this from the incoming request can be written as follows:

```java
public class MetaDataResolver implements HandlerMethodArgumentResolver {
    private static final String TRANSACTION_ID = "TRANSACTION-ID";
    private static final String ACCESS_KEY = "ACCESS-KEY";
    private List<String> metaDataHeaderNames = Arrays.asList(TRANSACTION_ID, ACCESS_KEY);

    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        return parameter.getParameterType().equals(MetaData.class);
    }

    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) throws Exception {
        HashMap<String, String> map = new HashMap<>();
        metaDataHeaderNames.forEach(name -> {
            if (webRequest.getHeader(name) != null) {
                map.put(name, webRequest.getHeader(name));
            }
        });
        return new MetaData(map);
    }
}
```
This resolver will try and compute the value for the argument if the arguments type is `MetaData`. It computes it by extracting all the headers representing the meta data from the request.
{{< mailchimp >}}

## Using in a controller method

This parameter can be accessed in a controller method as follows:

```java
@RestController
@RequestMapping("/profiles")
public class ProfileController {
    @Autowired
    ProfileService profileService;

    @RequestMapping(path = "/",
    method = RequestMethod.POST)
    public Map<String, String> create(@RequestBody Profile profile, MetaData metaData) {
        profileService.create(profile, metaData);
        System.out.printf(metaData.toString());
        return Collections.singletonMap("message", "success");
    }
}
```

If we were to run this app and make a request with the following headers, we will see that the MetaData instance did not get constructed with the right parameters.

## Wiring up the custom resolver
For this resolver to work, it needs to be added to the chain of resolvers that Spring uses. This can be done by extending `WebMvcConfigurerAdapter`‘s `addArgumentResolvers` method as follows:

```java
@Configuration
public class Config extends WebMvcConfigurerAdapter {
    @Override
    public void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers) {
        argumentResolvers.add(new MetaDataResolver());
    }
}
```

## Testing using MockMvc
 In order to test the behavior of a controller in the presence of a custom argument resolver using MockMvc, the resolver need to be added to the list of resolvers that MockMvc is going to use.
 An example test for the above class is as follows:

```java
@RunWith(MockitoJUnitRunner.class)
public class ProfileControllerTest extends TestCase {

    private ProfileController profileController;
    private MockMvc mockMvc;
    private ObjectMapper objectMapper;

    @Mock
    private ProfileService profileService;

    @Before
    public void setUp() {
        objectMapper = new ObjectMapper();
        profileController = new ProfileController(profileService);
        mockMvc = MockMvcBuilders
                .standaloneSetup(profileController)
                .setCustomArgumentResolvers(new MetaDataResolver())
                .build();
    }

    @Test
    public void shouldCreateAProfile() throws Exception {
        Profile profile = new Profile("foo", "foo@bar.com");
        MetaData metaData = new MetaData(Collections.singletonMap("TRANSACTION-ID", "foo"));

        mockMvc.perform(post("/profiles/")
                .content(objectMapper.writeValueAsBytes(profile))
                .contentType(MediaType.APPLICATION_JSON)
                .header("TRANSACTION-ID", "foo"))
                .andExpect(status().isOk());
        Mockito.verify(profileService).create(eq(profile), eq(metaData));
    }
}
```

This test is self-explanatory–we wire up the argument resolver, make a request with one of the meta data headers and expect the profile service to be invoked with the right parameters.
