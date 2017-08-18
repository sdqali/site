---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Looking up Compiler params used to compile a Ruby version"
date: 2013-09-08
comments: true
categories:
- code
- development
- ruby
tags:
- code
- development
- ruby
---
Today [Kashyap](https://twitter.com/kgrz) asked how one can identify the compiler parameters passed when compiling a Ruby version. I was curious how to achieve this and like any confused developer started searching for and looking in the Ruby documentation. Searching for **compiler parameters in ruby** did not yield any interesting results and the group of constants with the `RUBY_` prefix [^1] loaded in Ruby did not include anything related to compiler flags. Then I came across this blog post [^2] by [Jan Lelis](https://twitter.com/happycode) and I was curious what else `RbConfig::CONFIG` contains. This hash contains all the compiler flags used to compile the current Ruby VM.

This code snippet prints the hash.
```ruby
#! /usr/bin/env ruby

require "rbconfig"

RbConfig::CONFIG.each do |k, v|
  puts "#{k} - #{v}"
end
```
When this is executed under Ruby 1.9.3p194  under OS X, a section of the output will look like this:

```bash
target_vendor - apple
target_os - darwin12.2.1
CC - gcc-4.2
CFLAGS -  -O3 -ggdb -Wextra -Wno-unused-parameter -Wno-parentheses -Wno-long-long -Wno-missing-field-initializers -Werror=pointer-arith -Werror=write-strings -Werror=declaration-after-statement -Werror=shorten-64-to-32 -Werror=implicit-function-declaration -I/Users/sdqali/.rvm/usr/include -fno-common -pipe
LDFLAGS - -L. -L/Users/sdqali/.rvm/usr/lib -L/usr/local/lib
```

[^1]: These constants are `RUBY_COPYRIGHT`, `RUBY_DESCRIPTION`, `RUBY_ENGINE`, `RUBY_PATCHLEVEL`, `RUBY_PLATFORM`, `RUBY_RELEASE_DATE`, `RUBY_REVISION` and `RUBY_VERSION` on Ruby 1.9.3p194.
[^2]: Jan Lelis: [How to properly check for your Ruby interpreter, version and OS](http://rbjl.net/35-how-to-properly-check-for-your-ruby-interpreter-version-and-os)
