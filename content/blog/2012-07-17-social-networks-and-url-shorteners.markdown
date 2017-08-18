---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Social Networks and their URL Shorteners"
date: 2012-07-17
comments: true
categories:
- social-network
- twitter
- internet
- google+
tags:
- social-network
- twitter
- internet
- google+
---
I have been noticing lately that much of the traffic that my blog
receives comes from Twitter's **t.co** domain or Google+'s
**plus.url.google.com** domain. I don't receive much traffic and I don't
particularly care about the amount of traffic. However, when I
see traffic from Google+ or Twitter, I know that somebody is discussing
or sharing my posts and I am curious to know who is doing that. But if I
look at where the traffic comes from, with the hope that I will be able
to find Tweets or Google+ updates where people are talking about my
content, all I would be able to see is a **t.co** or **plus.url.google.com**
URL that redirects to my page. While it is mildly frustrating, I have
been thinking why both Twitter and Google+ replace every URL users share
on their network and replace it with their own URLs that does a redirect
to the original content being shared.

<!--more-->

I think I finally understand why. Data about user's sharing content is
of huge interest to a lot of people, most importantly marketers. URL
shortening services like [bit.ly](http://bitly.com") have been able to
come up with some interesting analysis about content sharing trends. The
difference now is that the social networks themselves have taken over
URL shortening and by way of that capturing and hiding user's sharing
habits.

Consider this scenario. You find something interesting on the web that
you would like your followers and friends to see. It could be a new interesting
startup, a programmer's rant, a tutorial, a new framework or the
Internet's most favourite thing - cat pictures. You have a browser
plugin that nicely shortens the rather long URL and gives you a new
**bit.ly** URL. You share it on Twitter. Twitter does not post the nice
**bit.ly** URL. Instead, it converts it into a **t.co** URL that redirects
to the **bit.ly** URL. From that point onwards, all **bit.ly** knows is that
a lot of people are sharing a particular **t.co** URL. Unless they figure
out where the **t.co** URL redirects to or does a Twitter search for the
URL, they don't have a clear idea of who shared the URL.

To understand the impact of this, lets look at another
scenario. [Francis Keogh](https://twitter.com/HonestFrank), a journalist
with the BBC shares a piece of Football transfer news on Twitter:

!["Screenshot of tweet saying 'West Ham close on deal to sign Mali striker Modibo Maiga'"](http://i.imgur.com/e2tqA.png "Screenshot of tweet saying 'West Ham close on deal to sign Mali striker Modibo Maiga'")

He obviously uses a shortened URL generated with BBC's **bbc.in**
shortener. BBC, being the media company they are have huge interest in
knowing who shares their content, when and where. But all that their
analytics system setup around **bbc.in** will be able to tell is that a
lot of traffic is coming from the URL [http://t.co/a0Sh34av](http://t.co/a0Sh34av) which is not of much use to
them because it strips the _who_ and _where_ aspects of the act of
sharing.

Now here comes the money part of it. There is somebody who has full
knowledge of this sharing - Twitter. They know who, when and where the
content was shared by. If media companies and others want to figure out
who shares their content, you have to ask Twitter. And it looks like to
me that Twitter won't give that information away easily. Twitter could
charge these companies and I would think that there will be a lot of
companies interested in buying this data.

While I showed an example of how Twitter does this, Google+ does
something very similar. And I would assume Facebook does the same with
its **fb.me** URL shortener. I am not sure, and I can not verify because I
don't have a Facebook account.

In a nutshell, social networks that are about sharing hides knowledge
about the content people share behind a system that only they have
access to and can potentially make a lot of money from that data. Pretty
clever of them, if you ask me.
