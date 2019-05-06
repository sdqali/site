---
bbcommentid: 33
categories:
- code
- python
- development
comments: true
date: 2013-08-15
ghcommentid: 72
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- python
- development
title: Python's bool type
---

Python does not have a true boolean type. The `True` and `False` built-in values in Python are wrappers around the integers `1` and `0`. This results in some interesting results involving True and False.

```python
>>> True == 1
True
>>> False == 0
True
>>> True + 9
10
>>> False - 1
-1
>>> str(True)
'True'
>>> repr(True)
'True'
```

The Python bool implementation got formalised in PEP 285 [^1] in 2002 by Guido van Rossum. The specification gives a lot of insight into von Rossum's insistence on maintaining backward compatibility and the Python way. It also touches up on another aspect of truthness in Python. In Python, almost all objects can be used to represent truth values. This means an empty list is false and a non-empty list is true.

So this
```python
if []:
    print "Truth"
else:
    print "Falsehood"

```
will print "Falsehood" and the following
```python
if [1, 2, 3]:
    print "Truth"
else:
    print "Falsehood"

```
will print "Truth".

[^1]: [Adding a bool type](http://www.python.org/dev/peps/pep-0285/) by Guido van Rossum.