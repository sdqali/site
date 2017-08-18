---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Why I am not on Facebook"
date: 2012-08-11
comments: true
categories:
- facebook
- social-network
- internet
tags:
- facebook
- social-network
- internet
---

Yesterday a colleague of mine asked me if I was on Facebook. He
was genuinely surprised by my reply that I was not and he wanted to know
 why. For the next 20 minutes or so, I explained to him why I quit
 Facebook and does not want anything to do with it.

This is not the first time I have had to explain my absence from Facebook. In this post I will explain my attitude towards Facebook in a more structured manner.

Broadly, these are the points I will touch upon:

* Narcissism
* Symmetric nature of sharing
* The social pressure to 'friend' someone
* Low signal to noise ratio

<!--more-->


## Narcissism
I have observed that Facebook makes people a lot more narcissistic than
they are in their real life. Facebook does this by providing a
convenient avenue to channel people's self-love and then use the social
pressure of the system to create incentive for people to use this
avenue.

I have an example that explains this well. I have seen people go to beautiful hill-sides and instead of enjoying
the nature around them, they start shooting photos of themselves with
the scenery in the background. This is a carefully executed ritual and
involves careful posing and choosing spots that maximises potential
**Likes** and **Comments**.

I have done this and observed a lot of people do it. Looking back, I
wish  had spent that time observing and appreciating the beauty of the
scenery around me.

At this point, one might point out that generating content as a fodder
for social networks is endemic to all social networks and no just
Facebook. This is where the lure of the **Likes** and **Comments** and the
social pressure to gather them comes in to play. Being able to generate
**Likes** and **Comments** becomes closely tied to your identity on
Facebook.

## Symmetric nature of sharing
Facebook relationships are fundamentally symmetric i.e. if **X** is your
**Friend**, then you are **X**'s **Friend** as well. This is drastically
different from the way relationship manifest in Twitter. The issue with
this symmetric relationship is that if **X** would like to consume the
content that you post to Facebook, he will have to be your **Friend**
which immediately results in you having to consume content posted by
**X**. This becomes increasingly annoying if you do not particularly like
cat pictures but Bob who likes cat pictures would likes to view the
photos you share. All of a sudden, you find yourself staring at cat
pictures from Bob.
Facebook later introduced asymmetric sharing with the concept of
**Subscribe**, but unless you were a celebrity, you still got friendship
requests from people who would like to view your posts.
There is an obvious solution to this problem - just don't accept that
friendship request from Bob. But unfortunately, this is easier said than
done, for the reason I talk about next.

## The social pressure to 'friend' someone
You get a friendship request from Alice who is a colleague. You do not
necessarily consider Alice a friend and you do not share common
interests. At that point you find yourself having to accept Alice as a **Friend** on Facebook because of the social
pressures associated with it.
You could be clever and ask Facebook to hide the updates from Alice, but
then you have to be an expert who knows where exactly Facebook decides
to hide the settings that allow you to do this.

## Low signal to noise ratio
This could be a manifestation of the large number of people on Facebook
and the relative esoteric and geeky nature of other social networks I
use, like Twitter. I have observed that my Facebook home page contained
a lot of noise compared to my Twitter stream.

I find useful content on Twitter whereas my Facebook home page showed me
a lot of obscure photo-shopped images, animated GIFs and useless FUD.

## Quitting Facebook
After suspending, deleting and re-creating my Facebook profile once I
deleted it for good in July, 2011. I let people whom I consider as
friends know that I would be available on my phone and through email. I
started calling up my friends instead of **Liking** their updates and
photos.

## Blocking Facebook
It is a well known fact that Facebook tracks people on the web using the
myriad of widgets, plugins and buttons they have managed to spread to
most of the web. My response has been to block anything to do with
Facebook. I use the cheap and simple way of using my **/etc/hosts** to
accomplish this. After many changes, this is how the Facebook related
part of it looks:

```bash
127.0.0.1 facebook.com
127.0.0.1 fbcdn.com
127.0.0.1 fbcdn.net
127.0.0.1 login.facebook.com
127.0.0.1 static.ak.connect.facebook.com
127.0.0.1 static.ak.fbcdn.com
127.0.0.1 static.ak.fbcdn.net
127.0.0.1 www.facebook.com
127.0.0.1 www.fbcdn.com
127.0.0.1 www.fbcdn.net
127.0.0.1 www.login.facebook.com
127.0.0.1 www.static.ak.connect.facebook.com
127.0.0.1 www.static.ak.fbcdn.com
127.0.0.1 www.static.ak.fbcdn.net
```
The current incarnation is adapted from
[Sajith Sasidharan](http://nonzen.in/2012/06/17/etchosts.html).

There. That is my Facebook story.
