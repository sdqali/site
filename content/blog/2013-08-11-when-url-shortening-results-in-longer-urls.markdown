---
bbissueid: 27
categories:
- technology
- internet
- twitter
comments: true
date: 2013-08-11
ghissueid: 71
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- technology
- internet
- twitter
title: When URL shortening results in longer URLs
---

I have previously [written](/blog/2012/07/17/social-networks-and-url-shorteners/) about [how social networks](/blog/2012/08/23/dear-content-creator-your-url-shortener-is-pointless/) use URL shortening as a way of obscuring and swallowing information about sharing of content on their platform. In Twitter's case, this means that all URLs are automatically 'shortened' with their _t.co_ domain. All their official clients take this shortening into account when you create a Tweet so as to avoid a round trip across the network to figure out if the tweet is short enough. But what happens if you are posting a URL that does not require any shortening? Something interesting happens.

<!--more-->

Remember how tweets are of 140 characters each? Similarly, all URLs piped through _t.co_ are of 22 characters. That means when you post a tweet that has a URL in it, 22 characters get used for the URL. This catch-all shortening results in scenarios like the following:

!["Twitter client shortening qz.com"](/images/aggressive_url_shortening.gif "Twitter client shortening qz.com")

Typing the 6 characters in _qz.com_ resulted in number of characters left to go from `107` to `85`.

There you have it. A URL of 6 characters gets 'shortened' to 22 characters. This once again shows how Twitter, like other social networking sites want to control the data about how URLs get shared.