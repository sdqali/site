---
Categories:
- development
- java
Description: ""
Tags:
- development
- java
- axon
date: 2016-04-24T18:35:43-05:00
title: Deprecating domain events in Axon
image: "images/axon.png"
---
Recently at work, we had to deprecate a domain event. This event used to represent an error scenario. However, the business had since decided that this is no longer a valid error scenario. Removing the Java class is not straight forward - since there are events of this type stored in the event store, every time the aggregate associated with this event is loaded, Axon will throw errors trying to de-serialize them.

<!--more-->

Obviously, we need an Upcaster [^1] to take care of this situation. The Upcaster in this scenario will have to upcast this event to something representing the non-existence of this event, regardless of the revision. There are two ways to address this issue - Upcasting to an explicit NoOpEvent and upcasting to an empty list.

## Upcasting to a NoOpEvent
Given an event `ValidationForFirstNameFailedEvent`, an upcaster that upcasts to a `NoOpEvent` can be implemented as follows:
```java
public class DeprecateValidationForFirstNameFailedEventUpcaster extends AbstractSingleEntryUpcaster {
    @Override
    protected Object doUpcast(SerializedObject intermediateRepresentation, UpcastingContext context) {
        return new SimpleSerializedType(NoOpEvent.class.getName(), "1");
    }

    @Override
    protected SerializedType doUpcast(SerializedType serializedType) {
        return new SimpleSerializedType(NoOpEvent.class.getName(), "1");
    }

    @Override
    public boolean canUpcast(SerializedType serializedType) {
        return serializedType.getName().equals(ValidationForFirstNameFailedEvent.class.getName());
    }

    @Override
    public Class expectedRepresentationType() {
        return JsonNode.class;
    }
}
```
As expected, this upcaster does not look at the revision of the intermediate representation and simply looks at the type of the event. And it completely discards any fields in the event and returns a simple type of the `NoOpEvent` class. Note that in this case, we are serializing the event as JSON using Jackson, hence the expected representation type is `com.fasterxml.jackson.databind.JsonNode`. If we were to use Axon's default XML serialization, the expected representation type will be `org.dom4j.Document`
{{< mailchimp >}}

### Upcasting to an empty list
Upcasting to an empty list can be easily achieved by implementing `Upcaster<T>` instead of extending `AbstractSingleEntryUpcaster`.
```java
public class ValidationForFirstNameFailedEventToEmptyListUpcaster implements Upcaster<JsonNode> {
    @Override
    public boolean canUpcast(SerializedType serializedType) {
        return serializedType.getName().equals(ValidationForFirstNameFailedEvent.class.getName());
    }

    @Override
    public Class<JsonNode> expectedRepresentationType() {
        return JsonNode.class;
    }

    @Override
    public List<SerializedObject<?>> upcast(SerializedObject<JsonNode> intermediateRepresentation,
        List<SerializedType> expectedTypes, UpcastingContext context) {
        return Collections.emptyList();
    }

    @Override
    public List<SerializedType> upcast(SerializedType serializedType) {
        return Collections.emptyList();
    }
}
```

This can also be done through extending `AbstractSingleEntryUpcaster` and returning `null` from both `upcast` methods. The class in turns returns empty lists for us. This is evident if we look at the JavaDoc for the methods

```java
    /**
     * Upcasts the given <code>intermediateRepresentation</code> into zero or more other representations. The returned
     * list of Serialized Objects must match the given list of serialized types.
     * <p/>
     * This method may return <code>null</code> to indicate a deprecated object.
     *
     * @param intermediateRepresentation The representation of the object to upcast
     * @param context                    An instance describing the context of the object to upcast
     * @return the new representation of the object
     */
    protected abstract T doUpcast(SerializedObject<T> intermediateRepresentation,
                                  UpcastingContext context);
```

I posted this question in the [Axon mailing list](https://groups.google.com/forum/#!topic/axonframework/G2tlU06mRPM) as well as our internal developer mailing list and upcasting to an empty list was the more popular choice. Allard Buijze, the creator of Axon had this to say:

> by upcasting to an empty list, you're explicitly indicating that the event no longer exists. When upcasting to a NoOpEvent, you implicitly mean the same thing, as no one is interested in a NoOp event.
> So you achieve the same thing, but explicit always beats implicit in DDD ;-)

While I agree with Allard that being explicit is better than being implicit (and not just in the context of DDD), I am not convinced that upcasting to an empty list is more explicit than upcasting to an explicit type. However, we went ahead with the empty list approach as it was the consensus among my coworkers.

[^1]: Upcasting is a technique of migrating the schema of events in an event-sourced system to keep up with changes in the business requirements. The Axon documentation has a [very good primer](http://www.axonframework.org/docs/2.0/repositories-and-event-stores.html#event-upcasting) on upcasting, specifically in the context of Axon.
