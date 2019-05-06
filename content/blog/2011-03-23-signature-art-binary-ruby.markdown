---
bbcommentid: 109
categories:
- code
- ruby
- development
comments: true
date: 2011-03-23
ghcommentid: 22
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- ruby
- development
title: Binary Signature Art
---

I was reading this very interesting [thread](http://forums.xkcd.com/viewtopic.php?f=7&t=11765) on the xkcd forum when I noticed a post from a user with the following signature in binary:

```bash
01001101 01100001 01100100 01100101 00100000 01011001 01101111 01110101 00100000 01001100 01101111 01101111 01101011 00100001"
```

At first, that did not particularly entice me, mostly because the topic being discussed was really interesting, but it did come back to my focus when I saw that another user had quoted the signature, along with the comment `Yeah, you know it. LOL :-)`. I had to find what the original message was.

So couple of minutes of Ruby later, I figured it out. His message was simple - `Made You Look!`. Yeah, he sure did!

Here is the rather simple Ruby code snippet that did the trick:

```ruby
code = "01001101 01100001 01100100 01100101 00100000 01011001 01101111 01110101 00100000 01001100 01101111 01101111 01101011 00100001"

parts = code.split " "

text = parts.map do |p|
  p.to_i(2).chr
end.to_s

puts text
```