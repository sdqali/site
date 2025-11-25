---
bbissueid: 9
categories:
- code
- python
- development
comments: true
date: 2013-10-07
ghissueid: 86
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- python
- development
title: Python Hack - Dynamically override an object's attribute
---

While working with Locust [^1] recently, we ran into a situation where we had to dynamically override an attribute in a class in the Locust library so as to control what value it got assigned. After a lot of scratching our heads and reading the Python documentation, we came across the `property` function. We were able to use this to hack together a solution that ensures that every time an attribute is read, it returns the result of executing a method.

The following example demonstrates a stripped down version of this hack.

```
import random

class Foo(object):
    bar = random.random()

foo = Foo()

# Prints the value assigned when the Foo object is initialised.
print("Before override")
print(foo.bar)
print(foo.bar)

# Override
Foo.bar = property(lambda self: random.random())

print("After override")
print(foo.bar)
print(foo.bar)
```

This snippet when executed will output the following:

```
Before override
0.0373028550804
0.0373028550804
After override
0.603160033663
0.501455108419
```

It can be seen that before introducing the override, the value of the `bar` attribute is set when the class is initialised and as expected, it does not change how many ever times the attribute is read. However, after the override, the attribute is assigned a new value every time it is read.

## How does this work?

The `property()` [^2] function returns an attribute for any class. It allows the creation of Ruby's `attr_accessor` [^3] style attributes on classes so that one can write `instance.attrib` to read an attribute value and `instance.attrib= ` to set an attribute value. What line `14` in the snippet does is to re-define the `bar` attribute to be a property whose `getter` is a `lambda`. Every time the `bar` attribute is read, the `lambda` gets executed.

A more comprehensive example of this can be found in my [Python dojo repository](https://github.com/sdqali/python_dojo/blob/master/dynamic_override/dynamic_override.py) on GitHub.


[^1]: [Locust](http://locust.io/) - a modern load testing framework.
[^2]: Python's built-in functions - [property](http://docs.python.org/2/library/functions.html#property).
[^3]: Ruby's [`attr_accessor` method](http://www.ruby-doc.org/core-1.9.3/Module.html#method-i-attr_accessor).