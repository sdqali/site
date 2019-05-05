---
categories:
- code
- browsers
- javascript
comments: true
date: 2012-11-22
ghcommentid: 50
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- browsers
- javascript
title: How Browsers Detect If You Are Offline
---

When I saw the newly released
[Heyoffline.js](http://oskarkrawczyk.github.com/heyoffline.js/) library,
I was curious to see how it figured out if the user was online or
not. This led me to the `window.navigator.onLine` [API](https://developer.mozilla.org/en-US/docs/DOM/window.navigator.onLine) and how
different browsers implement it. Chrome, Safari and Inernet Explorer 10
make sure that the API detects if the user is connected to a network,
while Firefox changes this flag if and only if the user chooses the
`Work Offline` option. A detailed discussion of this difference in
implementation is available
[here](http://schalk-neethling.com/2011/05/navigator-online-and-the-differing-implementations-of-a-standard/).

While this is an interesting example of how despite the efforts put into
standardising specifications they get interpreted differently, I was
more interested in seeing how different browsers detect if the user is
offline or not.

I did some digging around and this is what I found:

* I expected Internet Explorer to use the [Network Connectivity Status
  Indicator](http://blog.superuser.com/2011/05/16/windows-7-network-awareness/)
  service. It looks like that is not the case. Setting the registry
  entry
  `HKEY_LOCAL_MACHINESYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet
  -> EnableActiveProbing` to `0` did not seem to have any effect on
  Explorer's ability to find if the user is online or not.
* Google Chrome on Windows uses the [Winsock API]("http://msdn.microsoft.com/en-us/library/windows/desktop/ms741641(v=vs.85).aspx") to detect if a network
  is available. The relevant source code is
  [here](http://src.chromium.org/svn/trunk/src/net/base/network_change_notifier_win.cc). Look
  for the method `GetCurrentConnectionType()`
* Google Chrome on Linux uses a wrapper around NetworkManager's D-Bus
  API. The code is
  [here](http://src.chromium.org/svn/trunk/src/net/base/network_change_notifier_linux.cc).
* Google Chrome on Mac tries to reach `0.0.0.0`. This can be seen
  [here](http://src.chromium.org/svn/trunk/src/net/base/network_change_notifier_mac.cc). Look for the method `SetInitialConnectionType()`.