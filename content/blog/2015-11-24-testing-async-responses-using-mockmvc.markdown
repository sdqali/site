---
Categories:
- development
- java
Description: ''
Tags:
- development
- spring
- mockmvc
- java
date: 2015-11-24 10:45:06
ghcommentid: 101
image: images/spring-by-pivotal.png
title: Testing async responses using MockMvc
---

There are times when a Spring MVC end point performs asynchronous operations. Testing these end points using MockMvc can be tricky because of the asynchronous nature in which the result of the operation is eventually returned. This blog post describes how to write tests in such scenarios.

<!--more-->

Let's take a look at the following example. In this example, we have a simple end point that responds with a JSON object when invoked.

```java
@RestController
@RequestMapping("/test")
class ExampleController {
    @RequestMapping(value = "/hello",
            method = GET,
            consumes = APPLICATION_JSON_VALUE,
            produces = APPLICATION_JSON_VALUE)
    @ResponseStatus(OK)
    public Map<String, Object> hello(){
        return helloMessage();
    }

    private Map<String, Object> helloMessage() {
        return Collections.singletonMap("message", "hello");
    }
}
```

Writing a MockMvc test for this controller is fairly simple. The following test invokes the end point and asserts that the end point returns:

* The right HTTP response code `200`
* The right Content-Type `application/json`
* The right JSON message

```java
@RunWith(MockitoJUnitRunner.class)
public class ExampleControllerTest {

    public static final String CONTENT_TYPE = "Content-Type";
    private ExampleController controller;
    private MockMvc mockMvc;

    @Before
    public void setUp() {
        controller = new ExampleController();
        mockMvc = MockMvcBuilders
                .standaloneSetup(controller)
                .build();
    }

    @Test
    public void shouldHaveAMessageInResponse() throws Exception {
        mockMvc
                .perform(get("/test/hello")
                        .contentType(APPLICATION_JSON))
                .andDo(print())
                .andExpect(status().isOk())
                .andExpect(header().string(CONTENT_TYPE, APPLICATION_JSON_VALUE))
                .andExpect(jsonPath("message").value("hello"));
    }
}

```

Now, lets try and write a similar test for an end point uses `DeferredResult` to do asynchronous request processing. The end point in this example just wraps the JSON structure in `DeferredResult` and returns, whereas there will be a long running asynchronous process in a more useful case. But the idea remains the same.

```java
    @RequestMapping(value = "/deferred",
            method = GET,
            consumes = APPLICATION_JSON_VALUE,
            produces = APPLICATION_JSON_VALUE
    )
    @ResponseStatus(OK)
    public DeferredResult<Map> deferred() {
        DeferredResult<Map> deferredResult = new DeferredResult<>();
        deferredResult.setResult(helloMessage());
        return deferredResult;
    }
```

If our test for this end point were to use the same mechanism as the previous test, we will start observing an interesting error.

```java
    @Test
    public void shouldHaveAMessageInDeferredResponse() throws Exception {
        mockMvc
                .perform(get("/test/deferred")
                        .contentType(APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(header().string(CONTENT_TYPE, APPLICATION_JSON_VALUE))
                .andExpect(jsonPath("message").value("hello"));
    }
```

```bash
Response header Content-Type expected:<application/json> but was:<null>
```

This happened because MockMvc did not wait for the asynchronous process to finish. The solution to this involves using MockMvc's `asyncDispatch`. AsyncDispatch creates a new request that continues from the result of a previous MockMvc request that started the asynchronous process.
The test re-written using `asyncDispatch` would be as follows:

```java
    @Test
    public void shouldHaveAMessageInDeferredResponseWithAsyncDispatch() throws Exception {
        MvcResult result = mockMvc
                .perform(get("/test/deferred")
                        .contentType(APPLICATION_JSON))
                .andReturn();

        mockMvc
                .perform(asyncDispatch(result))
                .andExpect(status().isOk())
                .andExpect(header().string(CONTENT_TYPE, APPLICATION_JSON_VALUE))
                .andExpect(jsonPath("message").value("hello"));
    }
```

The same approach can be employed to test when controllers use Java 8's `CompletableFuture`.