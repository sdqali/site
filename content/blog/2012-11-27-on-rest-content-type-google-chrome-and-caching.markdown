---
categories:
- code
- development
- rest
- http
- chrome
- caching
- content-type
comments: true
date: 2012-11-27
ghcommentid: 51
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- development
- rest
- http
- chrome
- caching
- content-type
title: On REST, Content-Type, Google Chrome and Caching
---

Representational State Transfer (REST) is a style of software
architecture for distributed systems that has replaced technologies like
[SOAP](http://en.wikipedia.org/wiki/SOAP) as the predominant Web service
design model. Originally proposed by Roy Fielding in his [Doctorate
dissertation](http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm),
REST puts a lot of emphasis on resources, their representations and states. Basically a URL indicates a
single resource; the HTTP method (GET, POST, PUT, DELETE) indicates what
action should be performed on that resource; and the ACCEPT header indicates the format that the resource should be presented in.

## Chrome and Content-Type

Having seen this, one would assume that if you have a resource, say a
`User` on your system and there were two representations of that
resource - HTML and JSON. Let's assume that the HTML representation does
an AJAX call to fetch the JSON representation and renders it. While this
sounds simple enough, Google Chrome, one of the world's most popular
browsers
[totally breaks this](https://code.google.com/p/chromium/issues/detail?id=108766). A
good example of this weird behaviour can be seen [here](http://chrome-json-bug.heroku.com/docs).
<!--more-->
I ran in to this issue while playing around with [Express JS](http://expressjs.com/).
Now, the interesting thing here is that the Chrome developers seem to
have closed the issue without providing any convincing answers or
indicating whether they would fix this.

## Vary: Accept to the rescue?

One of the
[solutions](https://code.google.com/p/chromium/issues/detail?id=108766#c6)
suggested in the bug discussion is to use the `Vary: Accept`
header. According to the
[specs](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.44),
"while the response is fresh, whether a cache is permitted to use the
response to reply to a subsequent request without revalidation". In
other words, specifying `Vary: Accept` tells the client that if there is
a change in the `Accept` field, the resource in the cache must
be-revalidated. After trying that out and still having to stare at naked
JSON, I was convinced that telling Chrome to
re-validate the resource was the only way to get around this issue. This
leads us to another interesting bug in Chrome.

## Chrome ignores the no-cache directive

Reading the specs lead me to the
[Cache-Control](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9.4)
header. According to the specs, "If the no-cache directive does not
specify a field-name, then a cache MUST NOT use the response to satisfy
a subsequent request without successful revalidation with the origin
server.". That is exactly what I wanted.
But setting that header did not change anything, I still had naked JSON
when hitting the back button. This led me to
[yet another bug](https://code.google.com/p/chromium/issues/detail?id=28035)
on Chrome. Chrome seems to completely ignore the `no-cache`
directive. One of the [suggestions](https://code.google.com/p/chromium/issues/detail?id=28035#c3) in the discussion was to use the
`no-store` directive. That seemed to fix the issue.

But the
[spec](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9.2)
says `no-store` directive should be used to prevent the client from
caching any sensitive information. What that means is that the client
will never cache the resource.

The end result is that you would end up with a system with lot of end
points that are not cache-able because if you make them cache-able, Google
Chrome will leave your users staring at naked JSON.

## Possible solutions

* Use different URLs for different representations. In my case, that
  would mean I have `/users/sdqali.html` and `/users/sdqali.json` as
  URLs for the same resource. This somewhat violates the REST principle.

* Do not cache JSON end points at all. While this would work well for my
  small app, this is not an effective solution in the general case.