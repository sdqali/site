---
aliases:
- /blog/2018/03/22/a-jackson-and-freebuilder-quirk/
bbissueid: 100
date: 2018-03-23 05:21:42
ghissueid: 134
tags:
- jackson
- freebuilder
- java
title: A Jackson and FreeBuilder quirk
---

Jackson is a great tool to have in your tool set if you deal with JSON or XML. It facilitates easy serialization and de-serialization to and from Java classes with a convenient annotation based interface. With the same set of annotations, we can achieve both XML and JSON serialization and de-serialization. With Jackson's `data-format-xml` it is even possible to give the same Class a different JSON and XML representation. 
<!--more-->

```java
@JacksonXmlRootElement(localName = "user-account")
@JsonRootName("user")
public class Account {
  private String name;
  private String emailAddress;

  @JsonProperty("name")
  @JacksonXmlProperty(localName = "name")
  public String getName() {
    return name;
  }

  @JsonProperty("email_address")
  @JacksonXmlProperty(localName = "email-address")
  public String getEmailAddress() {
    return emailAddress;
  }

  // ...
}
```

When this gets used, it does the serialization and de-serializaion to and from XML and JSON in different forms:

```java
jsonMapper = new ObjectMapper();
jsonMapper.configure(WRAP_ROOT_VALUE, true);
jsonMapper.configure(UNWRAP_ROOT_VALUE, true);
xmlMapper = new XmlMapper();

// ...

Account account = new Account("John Doe", "john@example.com");

String jsonString = jsonMapper.writeValueAsString(account);
System.out.println(jsonString);
Account deSerializedAccount = jsonMapper.readValue(jsonString, Account.class);
assertEquals(account, deSerializedAccount);

String xmlString = xmlMapper.writeValueAsString(account);
System.out.println(xmlString);
deSerializedAccount = xmlMapper.readValue(xmlString, Account.class);
assertEquals(account, deSerializedAccount);
```

```shell
{"user":{"name":"John Doe","email_address":"john@example.com"}}
<user-account><name>John Doe</name><email-address>john@example.com</email-address></user-account>
```

Things get really interesting when we introduce [FreeBuilder](http://freebuilder.inferred.org/). FreeBuilder supports Jackson and we will be able to do serialization correctly. However, XML de-serialization does not work as expected.
```java
cksonXmlRootElement(localName = "user-account")
@JsonRootName("user")
@FreeBuilder
@JsonDeserialize(builder = Account.Builder.class)
public interface Account {
  @JsonProperty("name")
  @JacksonXmlProperty(localName = "name")
  String getName();

  @JsonProperty("email_address")
  @JacksonXmlProperty(localName = "email-address")
  String getEmailAddress();

  class Builder extends Account_Builder {}
}
```
```java
Account account = new Account.Builder()
    .setEmailAddress("john@example.com")
    .setName("John Doe")
    .build();

String jsonString = jsonMapper.writeValueAsString(account);
System.out.println(jsonString);
Account deSerializedAccount = jsonMapper.readValue(jsonString, Account.class);
assertEquals(account, deSerializedAccount);

String xmlString = xmlMapper.writeValueAsString(account);
System.out.println(xmlString);
deSerializedAccount = xmlMapper.readValue(xmlString, Account.class);
assertEquals(account, deSerializedAccount);
```
This will cause Jackson to throw an error while de-serializing XML, even though de-serializing to JSON works as expected. 
```shell
{"user":{"name":"John Doe","email_address":"john@example.com"}}
<user-account><name>John Doe</name><email-address>john@example.com</email-address></user-account>

com.fasterxml.jackson.databind.exc.UnrecognizedPropertyException: Unrecognized field "email-address" (class in.sdqali.json.Account$Builder), not marked as ignorable (3 known properties: "emailAddress", "email_address", "name"])
 at [Source: (StringReader); line: 1, column: 83] (through reference chain: in.sdqali.json.Account$Builder["email-address"])
 ```
After digging around, it turns out that FreeBuilder [keeps only](https://github.com/inferred/FreeBuilder/blob/master/src/main/java/org/inferred/freebuilder/processor/JacksonSupport.java#L40) the `@JsonProperty` annotation on methods that it finds. This in turn causes the object created by the builder to have methods whose `@JacksonXmlProperty` annotations are stripped of, which in turn causes Jackson to look for the camel-cased versions of the attribute names. I have opened a new [GitHub issue](https://github.com/inferred/FreeBuilder/issues/294) for this. 

Until this is resolved, if you use FreeBuilder and need to have different XML and JSON representation, you will have to write a custom Jackson [Serializer](https://github.com/FasterXML/jackson-docs/wiki/JacksonHowToCustomSerializers) and Deserializer.