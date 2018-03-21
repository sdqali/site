---
Categories:
- development
- java
- spring
Description: ""
Tags:
- development
- java
- spring
- logstash
date: 2016-06-30T19:43:07-04:00
image: "images/spring-by-pivotal.png"
title: JSON logging for Spring applications
---
<meta content="logstash spring boot example" name="keywords">
If you have an application that writes logs, there are many reasons to make it write the log in JSON format. It makes it easier to search and analyze them when using tools such as the ELK Stack [^1]. JSON formatted logs make it easier to look at them when looking at how the app is behaving in real time using tools like jq [^2]. This blog post documents how to format logs as JSON in a Spring application.

<!--more-->

We will be using the `logstash-logback-encoder` [encoder](https://github.com/logstash/logstash-logback-encoder) from Logstash. This can be added to the application with the following Maven dependency:

```xml
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>4.7</version>
</dependency>
```

The next step is to configure logback to log using the new encoder. This can be done by placing a `logback.xml` configuration file in the application's class path - for example in the `main/resources` directory.
{{< mailchimp >}}

If we want the application to log to the console in JSON format, we will use a `ConsoleAppender` with the encoder as follows:

```xml
<configuration>
    <appender name="consoleAppender" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
    </appender>
    <logger name="jsonLogger" additivity="false" level="DEBUG">
        <appender-ref ref="consoleAppender"/>
    </logger>
    <root level="INFO">
        <appender-ref ref="consoleAppender"/>
    </root>
</configuration>
```

If we wanted the application to log to a file with the logs being rotated, we will configure a `RollingFileAppender` with the encoder, as follows:
```xml
<configuration>
    <property name="LOG_PATH" value="/tmp/json-log.json" />
    <appender name="jsonAppender" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <File>${LOG_PATH}</File>
        <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
        <rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
            <maxIndex>1</maxIndex>
            <fileNamePattern>${LOG_PATH}.%i</fileNamePattern>
        </rollingPolicy>
        <triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
            <MaxFileSize>1MB</MaxFileSize>
        </triggeringPolicy>
    </appender>
    <logger name="jsonLogger" additivity="false" level="DEBUG">
        <appender-ref ref="jsonAppender"/>
    </logger>
    <root level="INFO">
        <appender-ref ref="jsonAppender"/>
    </root>
</configuration>
```

With this configuration in place, we can tail the logs to observe the application in a much more readable manner:

```
$ tail -f /tmp/json-log.json  | jq .
{
  "@timestamp": "2016-06-30T20:01:59.651-04:00",
  "@version": 1,
  "message": "Mapped \"{[/error],produces=[text/html]}\" onto public org.springframework.web.servlet.ModelAndView org.springframework.boot.autoconfigure.web.BasicErrorController.errorHtml(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse)",
  "logger_name": "org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping",
  "thread_name": "main",
  "level": "INFO",
  "level_value": 20000,
  "HOSTNAME": "somehostname"
}
{
  "@timestamp": "2016-06-30T20:01:59.677-04:00",
  "@version": 1,
  "message": "Mapped URL path [/webjars/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]",
  "logger_name": "org.springframework.web.servlet.handler.SimpleUrlHandlerMapping",
  "thread_name": "main",
  "level": "INFO",
  "level_value": 20000,
  "HOSTNAME": "somehostname"
}
...
```
The Logstach encoder also provides for a [variety of customizations](https://github.com/logstash/logstash-logback-encoder#custom_field_names) to the way the logs are written.

A sample application with these configurations is available in [this repository](https://github.com/sdqali/json-log).

[^1]: ELK - ElasticSearch, Logstash, Kibana is a toolset for analyzing logs. An introduction to ELK can be found [here](https://www.elastic.co/webinars/introduction-elk-stack).
[^2]: [jq](https://stedolan.github.io/jq/) is a command line JSON processor. If you work with JSON, jq is a must have tool.
