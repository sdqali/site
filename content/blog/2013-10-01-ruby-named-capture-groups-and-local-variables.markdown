---
bbcommentid: 12
categories:
- ruby
- code
- regexp
comments: true
date: 2013-10-01
ghcommentid: 84
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- ruby
- code
- regexp
title: Ruby, Named Capture Groups and Local Variables
---

Ruby's regular expressions support [named capture groups](/blog/2013/09/29/named-capture-groups-in-regular-expressions/), since 1.9. However, there is a weird behaviour while using named capture groups with the `Regexp#=~` method. When named capture groups are used with `=~`, the captured values are placed in local variables with the same name as the capture group. The following example demonstrates this:

```ruby
#!/usr/bin/env ruby

month = "January"
test_string = "Today's date is: 9/28/2013."
/(?<month>\d{1,2})\/(?<day>\d{1,2})\/(?<year>\d{4})/ =~ test_string
puts month.inspect
```

This when executed will print `9`.

The official documentation [^1] says:

> When named capture groups are used with a literal regexp on the left-hand side of an expression and the =~ operator, the captured text is also assigned to local variables with corresponding names.

This local variable assignment does not happen if the regular expression is on the right-hand side of the expression or the regular expression contains a variable interpolation.

### Regexp on right-hand side

```ruby
#!/usr/bin/env ruby

month = "January"
test_string = "Today's date is: 9/28/2013."
test_string =~ /(?<month>\d{1,2})\/(?<day>\d{1,2})\/(?<year>\d{4})/
puts month.inspect
```

This will print `January`.

### Regexp with interpolation
```ruby
#!/usr/bin/env ruby

month = "January"
DAY = "day"
test_string = "Today's date is: 9/28/2013."
/(?<month>\d{1,2})\/(?<#{DAY}>\d{1,2})\/(?<year>\d{4})/ =~ test_string
puts month.inspect
```

This will print `January`.

This behaviour is present only for the `Regexp#=~` method and not for `Regexp#match`. So it is safer to use the latter without worrying about unintended side effects.

PS: Hat tip to [Tejas](http://www.nilenso.com/people.html#gja) for telling me about this quirk.

[^1]: Ruby docs for [Class: Regexp (Ruby 1.9.3)](http://www.ruby-doc.org/core-1.9.3/Regexp.html#label-Capturing).