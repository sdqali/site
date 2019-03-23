---
title: Understanding trailing @ processing in SAS input
date: 2019-03-23T12:46:08-07:00
tags:
- SAS
- development
---

One of the first things I noticed when I started poking around in SAS code is that the `input` statement is very powerful, flexible and hence sometimes hard to understand. It can read pretty much anything in to a dataset as long as you tell it what to do.

The use of trailing `@`s to take control of how SAS advances the input pointer is a powerful technique to read from input files where the data is laid out in non-standard formats. In this blog post, we will try to understand how trailing `@` processing works with the help of some `infile` statement options and the `putlog` statement to write to the SAS log.

Let's take this example from the excellent paper _The Input Statement: Where It's @_ [^1] - given an put file where the first variable has to be read beginning from a particular column in the input line based on the value of the second variable.

```
Age  Type
23   1
  44 2
```


[^1]: The Input Statement: Where It's @. Paper 253-29, SUGI 29 Proceedings.
