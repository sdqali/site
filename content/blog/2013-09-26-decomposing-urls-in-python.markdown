---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Decomposing URLs in Python"
date: 2013-09-26
comments: true
categories:
- python
- code
tags:
- python
- code
---
Python's `urlparse` module breaks down URLs in to components. It supports all the URL schemes specified in RFC 3986 [^1].

```bash linenos:false
>>> import urlparse
>>>
>>> urlparse.urlparse("https://example.com/foo?param=bar")
ParseResult(scheme='https', netloc='example.com', path='/foo', params='', query='param=bar', fragment='')
>>>
>>> urlparse.urlparse("file://example.com/etc/fstab")
ParseResult(scheme='file', netloc='example.com', path='/etc/fstab', params='', query='', fragment='')
>>>
>>> urlparse.urlparse("news:comp.infosystems.www.misc")
ParseResult(scheme='news', netloc='', path='comp.infosystems.www.misc', params='', query='', fragment='')
```

[^1]: IETF - RFC for [Uniform Resource Identifier (URI): Generic Syntax](https://tools.ietf.org/html/rfc3986).