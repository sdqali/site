---
categories:
- code
- development
- chrome
- plugin
- javascript
comments: true
date: 2012-11-29
ghcommentid: 53
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- development
- chrome
- plugin
- javascript
title: 'My first Firefox plugin: GetCache - View cached version of the current page'
---

I released my [first Firefox plugin](https://addons.mozilla.org/en-US/firefox/addon/getcache-ff/) today. It
is awaiting review, but if you are adventurous, you can install it right
now. Go on, try it.

After I had written the [Chrome version](/blog/2012/11/28/getcache-a-chrome-plugin-to-view-cached-version-of-the-current-page/) yesterday, [Manish](https://twitter.com/ManishChaks) suggested
that I should write one for Firefox. There already exist Firfox plugins
that does exactly what GetCache does, but I decided to go ahead and write it
for fun. And of course, the fact that I could publish it without having
to sign up with my Credit Card information was enticing.

<!--more-->

There are three approaches to write a Firefox plugin:

* [Traditional extensions](https://developer.mozilla.org/en-US/docs/XUL_School/Introduction) - Uses JAvaScript and XUL.
* [Jetpacks](https://addons.mozilla.org/en-US/developers/builder) - Uses
  HTML, CSS and JavaScript.
* [Bootstrapped extensions](https://developer.mozilla.org/en-US/docs/Extensions/Bootstrapped_extensions)

<!--more-->
I decided to go the Jetpack because the development process and
technologies were similar to Chrome plugins. And I had no prior
experience with XUL. Once I had downloaded the SDK and set it up, things
were pretty easy. The
[API](https://addons.mozilla.org/en-US/developers/docs/sdk/latest/) is
well documented.

## The API
The bulk of the code is JavaScript. The API is easy to use. The
following snippet adds a widget to the Addon toolbar at the bottom of
the Firefox window:

```javascript
    var createWidget = function () {
      new Widget({
        id: "sdqali-getcache",
        label: "Get Google's cached version of the current page..",
        contentURL: self.data.url ("images/icon.png"),
        onClick: function(event) {
          loadCachedPage ();
        }
      });
    };
```

## Adding context menu entries
While things were pretty smooth overall, I ran in to a weird edge
case. I wanted a context menu entry that would load the Google cache
page, and I wanted this entry to be available regardless of whether the
user has selected some text in the page or not. The API uses the notion
of
[`Contexts`](https://addons.mozilla.org/en-US/developers/docs/sdk/latest/packages/addon-kit/context-menu.html)
o decide when the menu entry will be available. While the API says that
I can use an arrays of `Contexts`, I had no success with it. I ended up
creating two context menu entries, one attached to the `PageContext` and
one attached to the `SelectionContext`.

## Source
I used this
[beautiful icon](http://www.iconfinder.com/icondetails/7065/128/cache_icon)
by Sergio Sanchez Lopez. Since it comes with a GPL license, the plugin
is also licensed under GPL.
I have put the source code on [Github](https://github.com/sdqali/getcache-ff).