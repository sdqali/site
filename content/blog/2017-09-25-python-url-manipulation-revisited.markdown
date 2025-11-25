---
aliases:
- /blog/2017/09/25/python-url-manipulation-revisited/
bbissueid: 91
date: 2017-09-26 04:22:39
ghissueid: 132
tags:
- python
title: Python URL manipulation revisited
---

My [last blog post](/blog/2017/08/17/uploading-a-standalone-artifact-to-nexus-3/) about publishing standalone files to Nexus repositories prompted me to revisit URL manipulation in Python. When I did this [the last time](/blog/2013/09/26/decomposing-urls-in-python/), I used Python stand library's `urlparse` and it did the job. This time around, I needed to do a different kind of manipulation. Given a URL, I had to set credentials on it. 

I started at `urlparse` and soon realized that Python3 moved this module to [urllib.parse](https://docs.python.org/3/library/urllib.parse.html). That is not too bad, I thought. After playing around with it, it became clear that `urllib.parse` can't manipulate credentials in a URL.

```python
In [1]: from urllib import parse

In [2]: url = parse.urlparse('http://example.com')

In [3]: print(url)
ParseResult(scheme='http', netloc='example.com', path='', params='', query='', fragment='')

In [4]: url.username = "username"
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-4-60e52fe02603> in <module>()
----> 1 url.username = "username"

AttributeError: can't set attribute

In [5]: url.password = "password"
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-5-4f64c7192b99> in <module>()
----> 1 url.password = "password"

AttributeError: can't set attribute

In [6]: url.username == None
Out[6]: True

In [7]: url.password == None
Out[7]: True
```


After spending time with various URL manipulation libraries in Python, [furl](https://github.com/gruns/furl) was the only library that I found to be capable of this seemingly simple and common enough operation.

```python
In [1]: from furl import furl

In [2]: url = furl('http://example.com')

In [3]: url
Out[3]: furl('http://example.com')

In [4]: url.password = "password"

In [5]: url.username = "user"

In [6]: url.tostr()
Out[6]: 'http://user:password@example.com'
```