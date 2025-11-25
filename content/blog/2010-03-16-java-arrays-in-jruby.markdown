---
bbissueid: 93
categories:
- code
- jruby
- ruby
- java
- development
comments: true
date: 2010-03-16
ghissueid: 20
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- jruby
- ruby
- java
- development
title: Java Arrays in JRuby
---

Recently my team encountered a frustrating thing while working with a Java library in JRuby. It took us long to figure out what was going wrong. This is an attempt to write down what was happening.

You are in Ruby world, a world of weak typing, no type casting and pure bliss in coding. You forget that some languages care about the type of elements in an Array. And you end up spending a lot of time figuring out why you are staring at a stupid looking exception.

I will be using a dummy example for describing the problem.

The following code snippet tries to compare two arrays in JRuby using Java Arrays' equals method. In JRuby world, one would expect this to work. Actually, one should not, but Ruby really gets into you.

```ruby
require 'java'
import 'java.util.Arrays'

puts "Arrays equal" if Arrays.equals([1, 2, 3], [1, 2, 3])
```

Well, it does not. You get an error:

```bash
no equals with arguments matching [class org.jruby.RubyArray, class org.jruby.RubyArray] on object Java::JavaUtil::Arrays (NameError)
```

This error message is informative. In our case, our unit tests threw an error that was very difficult to make any sense of. The reason why this fails is obvious.

Java does care about the Type of things that form an Array. So you need to cast it to the correct type.

Here is the code that actually works:

```ruby
require 'java'
import 'java.util.Arrays'

puts "Arrays equal" if Arrays.equals([1,2,3].to_java(java.lang.Integer),
                                     [1,2,3].to_java(java.lang.Integer))
```

The `to_java` method casts the elements of the Ruby array into Java array with elements of type specified.