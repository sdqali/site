---
bbcommentid: 19
categories:
- ruby
- code
- regexp
- python
- javascript
comments: true
date: 2013-09-29
ghcommentid: 81
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- ruby
- code
- regexp
- python
- javascript
title: Named Capture Groups in Regular Expressions
---

I will admit that I find regular expressions somewhat hard to parse. While the thinking process needed to write a regular expression is iterative and hence results in the correct expression suitable for the situation, once it is written it lacks readability. I have faced that pain of trying to grok a complex regular expression written years ago. So I was pleasantly surprised when I saw [this example](https://news.ycombinator.com/item?id=6463144) from Hacker News user *WestCoastJustin*. I found it very easy to understand because of the names he had assigned to each capture group in the expression.

## Ruby

Ruby has supported named capture groups since version 1.9. Each match group is named by using `?<name>` inside the match group and these matches are made available has a hash and each match can be accessed by using the match group name as the key.

*WestCoastJustin*'s example will look like this in Ruby:

```ruby
#!/usr/bin/env ruby

test_string = "Today's date is: 9/28/2013."

match = test_string.match /(?<month>\d{1,2})\/(?<day>\d{1,2})\/(?<year>\d{4})/
puts match.inspect
puts match[:month]
puts match[:day]
puts match[:year]
```

This is much easier to understand because looking at it, it makes it clear that the intent of matching the first group of 1 or 2 digits is to look for the **month** in the date. Similarly, the intent of the *day* and *year* matches are easier to understand.

This will result in:
```bash
> ruby /tmp/named_matches.rb
#<MatchData "9/28/2013" month:"9" day:"28" year:"2013">
9
28
2013
```

##Python
Python's `re` module supports named match groups using the `?P<name>` pattern. After a pattern search, the results are placed in a `dict`.

```python
#!/usr/bin/env ruby

import re

test_string = "Today's date is: 9/28/2013."
pattern = re.compile(r"(?P<month>\d{1,2})\/(?P<day>\d{1,2})\/(?P<year>\d{4})")
match_dict = pattern.search(test_string).groupdict()
print(match_dict)
```

JavaScript does not support named capture groups. There are a lot of [hacks](http://trentrichardson.com/2011/08/02/javascript-regexp-match-named-captures/) aimed at providing this functionality. The XRegExp library [supports](http://xregexp.com/syntax/#namedCapture) named capture groups.