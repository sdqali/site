---
categories:
- python
- code
- development
- ruby
- heredoc
comments: true
date: 2012-07-04
ghcommentid: 40
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- python
- code
- development
- ruby
- heredoc
title: Heredocs in Ruby and Python
---

I have been doing some coding in Python recently. While playing around with some code, I noticed that the way [heredocs](http://en.wikipedia.org/wiki/Here_document) are used in Python is different from Ruby.

## Python
Consider the following snippet:

```python
# test.py

print "some text in single line"

print """
As opposed to
some text
written as
heredoc
"""
print "and then another single line"
```

When run, this would result in this:
```bash
bash-3.2$ python test.py
some text in single line

As opposed to
some text
written as
heredoc

and then another single line
```
Notice how there is a preceding and trailing linebreak around the string printed using heredoc.

<!--more-->

I spent a lot of time trying to figure out how and why this was happening. Finally, help came from `@dibb` on `#python`. Looks like I was doing it wrong. In Python, the useful part of the heredoc starts immediately after the `"""`. So if you don't want those excess linebreaks, you should write something like this:
```python
# test2.py

print "some text in single line"

print """As opposed to
some text
written as
heredoc"""

print "and then another single line"
```
When run, this would print the text without the extra line breaks:
```bash
bash-3.2$ python test2.py
some text in single line
As opposed to
some text
written as
heredoc
and then another single line
```

If you don't want to write the string just after the `"""`, you could use a `\` to remove the linebreaks, like this:
```python
# test3.py

print """\
As opposed to
some text
written as
heredoc\
"""
```


## Ruby
I come from the Ruby world, where the heredocs behave in a slightly different way. The equivalent code in Ruby would look like this:
```ruby
# test.rb

puts "some text in single line"

puts <<-STR
As opposed to
some text
written as
heredoc
STR

puts "and then another single line"
```
Notice how the actual content of the heredoc begins only on the line after `<<-STR`

I hope being aware of this detail saves you some time.