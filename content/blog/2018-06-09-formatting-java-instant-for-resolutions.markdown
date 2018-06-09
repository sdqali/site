---
title: Formatting Java Instant for resolutions
date: 2018-06-09T11:55:23-07:00
tags:
  - java
  - time
---
I have had to look up how to format Java's Instant with a given resolution - for example in microseconds or nanoseconds. After fiddling with various formatters, I was happy to finally get this right.
<!--more-->

```java
@Test
public void shouldFormatWith7Decimals() {
  int resolution = 7;
  DateTimeFormatter dateTimeFormatter = new DateTimeFormatterBuilder()
    .appendInstant(resolution)
    .toFormatter();
  Instant instant = Instant.now();
  System.out.println(dateTimeFormatter.format(instant));
}
```
