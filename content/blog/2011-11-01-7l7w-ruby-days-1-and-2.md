---
title: "7L7W - Ruby Days 1 and 2"
slug: 7l7w-ruby-days-1-and-2
date: 2011-11-01T12:23:00+0000
draft: false
---

I joined a [7 langauges in 7 weeks](http://pragprog.com/book/btlang/seven-languages-in-seven-weeks) study group started by [jocranford](https://twitter.com/#!/jocranford) and others. The group started on 24th October, but I joined only on yesterday. The language for the first week is Ruby. I have done a fair bit of Ruby and consider myself fairly familiar with Ruby.  
  
I have managed to complete days 1 and 2 of Ruby. The book encourages one to Google, read the API and figure out stuff yourself. I have found this approach really nice because following this has enabled me to learn some stuff I did not know about Ruby.  
  
I have put the code for [Day 1](https://github.com/sdqali/7l7w/tree/master/ruby/Day1) and [Day 2](https://github.com/sdqali/7l7w/tree/master/ruby/Day2) on Github.  
  
Stuff I learned from Day 1 and Day2 (Mostly Day 2):  
  

* Hash sorting is funny. Hashes get converted to Arrays before being sorted. There are other ways to do stuff.
* Ruby does not have named params. I realized that I never noticed this because I used hashes.
* A symbol always have the same object id and symbols are not garbage collected.
* [Enumerable#inject](http://www.ruby-doc.org/core-1.9.2/Enumerable.html#method-i-inject) and [Enumerable#reduce](http://www.ruby-doc.org/core-1.9.2/Enumerable.html#method-i-reduce) are the same. And there is no need to pass an initial value.
* [File.owned?](http://www.ruby-doc.org/core-1.9.2/File.html#method-c-owned-3F) - Pretty useful API.

  
  
This looks like fun.