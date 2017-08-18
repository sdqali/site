---
image: /images/threaded-blue-on-black-cropped.jpg
title: "GetCache - A Chrome plugin to view cached version of the current page"
date: 2012-11-28
comments: true
categories:
- code
- development
- chrome
- plugin
- javascript
tags:
- code
- development
- chrome
- plugin
- javascript
---

>Download the plugin
[here](/downloads/GetCache.crx)

On numerous occasions, I have ran in to the situation where I had to
look up how to load Google's cached version of a particular page. This
happens often when I follow a link from Hacker News or Reddit to a blog
post and the blog has went down due to the great avalanche of traffic
from HN and Reddit.

After struggling to remember and having to Google how to get the cached
version, I decided to finally solve this issue. I wrote `GetCache`, a
dead simple Google Chrome plugin that loads Google's cached version of
the current page.

## Installing
You can download the plugin
[here](/downloads/GetCache.crx). In order to install it, open your
Extensions page (`Window -> Extensions`) and drag the downloaded `CRX`
file to the page.

<!--more-->
## Usage

On any page, click on the GetCache icon to load the cached page.

![GetCache icon](/images/get_cache_icon.png "GetCache icon")


Or you could right click on the page and select `View Google's cache`.

![GetCache context menu](/images/get_cache_context_menu.png "GetCache context menu")

## Source Code
The source code for the plugin is dead simple. All it does is to append
`http://webcache.googleusercontent.com/search?q=cache:` to the beginning
of the current URL and ask chrome to load the new URL in the same
tab. The interesting bit of the code is below:

```javascript
(function () {
  var navigateToCachedPage = function (tab) {
    var gCacheUrlPrefix = "http://webcache.googleusercontent.com/search?q=cache:";
    var currentUrl = tab.url;
    var cacheUrl = gCacheUrlPrefix + currentUrl;
    chrome.tabs.update(tab.id, {url: cacheUrl});
  };

  chrome.browserAction.onClicked.addListener(function(tab) {
    navigateToCachedPage (tab);
  });

  chrome.contextMenus.create({
    title: "View Google's cache",
    contexts:["all"],
    onclick: function (clickData, tab) {
      navigateToCachedPage (tab);
    }
  });
}) ();
```

I used this
[beautiful icon](http://www.iconfinder.com/icondetails/7065/128/cache_icon)
by Sergio Sanchez Lopez. Since it comes with a GPL license, the plugin
is also licensed under GPL.

The source code for the plugin is on [Github](https://github.com/sdqali/GetCache).

## Why is this not on the Chrome store?

I wanted to push it to the Google Chrome web store. But it looks like I
need to verify my developer account by paying a sum of USD 5.0. Even
worse, I have to create a Google Wallet acount. At this
point, I am not so keen to be on the Webstore. In the future, I might
get a verified developer account.
