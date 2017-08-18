---
image: /images/threaded-blue-on-black-cropped.jpg
title: "My Tinfoil setup"
date: 2013-08-17
comments: true
categories:
- internet
- technology
- browsers
tags:
- internet
- technology
- browsers
---

I try to be careful when I use the internet. This is not because I do illegal stuff—I just don't like the idea of random websites tracking me across the web, recording everything I do, and then serving me advertisements. I don't like the idea of technocracies like Facebook collecting and storing data about me, even after I have explicitly quit their colourful walled garden. [^1] I don't like Google tracking what websites I read by pretending to provide a service to the creators of those websites in the form of CDN and Analytics. [^2] I don't want marketing optimisation services to track me and put me in their funnel, unless I explicitly want to.

This means that when I browse the web, I treat cookies, javascript code and third party content with suspicion. Over the years, my setup has evolved in to something that makes my internet use safe, all the while being useful. These are some of the things I do to ensure that sites are not tracking me.

<!--more-->

## Use different browsers as sandboxes
I run at least 5 browsers. I use Firefox as my primary browser to read and access email. I run Safari to access my work email, our Mingle [^3] instance, our in-house knowledge sharing network etc. I run Chromium when I am working on JavaScript and CSS because I find the development tools nothing short of a joy to use. I also have to use Google Chrome from time to time because that is what a lot of our customers use to access our product and sometimes I have to test our systems on Google Chrome. This separation of browsing into sandboxes makes it easy to control your usage patterns on a website. I have my Firefox set up to use DuckDuckGo as the search engine.

## An aggressive /etc/hosts
I have a long (5731 lines) _/etc/hosts_ file. [^4] I use this method to filter out stuff because it is a text file and it is easy to make sense of what it does. I adopted it from [Duke Leto's Util](https://github.com/leto/Util) repository. His file blocks a wide variety of website and over time I have added all the domains for social networks, advertising networks and marketing automation sites that I have come across to it. This ensures that when I navigate to a website and it has a bunch of tracking code from Facebook in the form of Like/Share buttons, my system won't even load these resources.

## Disable third party cookies
Third party cookies are great for tracking people across websites, often without the their knowledge or permission. My observation is that in my every day use of the web, there is nothing beneficial to me arising from websites' use of third party cookies. I block third party cookies on browsers. Most browsers allow third party cookies by default, but make it reasonably easy to block them. [^5]

## Ghostery
[Ghostery](https://www.ghostery.com/) is a browser plugin that blocks a large number of advertising, marketing and banner content on web pages. Ghostery is available for all the major browsers. While setting up Ghostery, one has to be careful to choose settings in such a way that all sites in Ghostery's available list of dodgy websites get blocked, because the default settings allow some sites.

## NoScript
[NoScript](http://noscript.net/) is a browser plugin for the Mozilla suite that allows users to verify the content being loaded by webpages and execute them if and only if the user trusts the content. It works really well and allows you to configure exceptions for the websites you absolutely trust. The only flipside of this is that a large percentage of the web is dependent on JavaScript and plugins and when you browse the web with NoScript, it appears way different to you from the one without NoScript. But at this point, I am willing to make that compromise.


## Self destructing cookies
Self destructing cookies is a Firefox plugin that destroys cookies and LocalStorage the moment you close a tab associated with a site.  It allows whitelists, so you can configure exceptions for sites you trust. The [plugin's profile](https://addons.mozilla.org/en-US/firefox/addon/self-destructing-cookies/) has a more comprehensive story on why you should use it.


## Tor Bundle
This goes without saying. If you read articles of political nature on the web, please install the Tor bundle [^6] and do your reading there. Tor has a community behind it and actively patches it against vulnerabilities. The project's F.A.Q. [^7] is a good starting point to learn more about Tor and how to use it.


## Disclaimer
I am in no way claiming that you would be saved from tracking if you use this setup. This is not the perfect setup. I am sure Google knows to some extent I do on the web. I am sure Facebook still has a lot of data about me. However, this is a good starting point.


[^1]: I [deleted my Facebook account](/blog/2012/08/11/why-i-am-not-on-facebook/) over two year ago. But it is [now known](http://www.zdnet.com/firm-facebooks-shadow-profiles-are-frightening-dossiers-on-everyone-7000017199/) that Facebook keeps a dossier on people, even the ones that does not have an account, simply because they happen to be in the address books of people who give Facebook access to their address, falling for Facebook's cajoling.
[^2]: Google provides a [Content Delivery Network](https://developers.google.com/speed/libraries/devguide) for the popular JavaScript libraries. They also have a free analytics service.
[^3]: Mingle is the best project management tool out there. You don't have to take my word for it, [try it for yourself](http://www.thoughtworks.com/mingle).
[^4]: The hosts file is used by the networking stack on a system to map hostnames to IP addresses. This allows a user to block domains by looping them back to 127.0.0.1. Wikipedia, as always have a [good article](https://en.wikipedia.org/wiki/Hosts_%28file%29) about it.
[^5]: CNET - [Disable third-party cookies in IE, Firefox, and Google Chrome](http://howto.cnet.com/8301-11310_39-20042703-285/disable-third-party-cookies-in-ie-firefox-and-google-chrome/).
[^6]: The Tor Bundle is a fork of Firefox configured to enhance anonymity and prevent tracking. It comes configured to use the [Tor network](https://www.torproject.org/)
[^7]: [Tor F.A.Q.](https://www.torproject.org/docs/faq.html.en), on Tor Project's website.