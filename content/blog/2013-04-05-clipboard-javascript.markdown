---
categories:
- code
- development
- javascript
- browser
- flash
comments: true
date: 2013-04-05
ghcommentid: 57
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- development
- javascript
- browser
- flash
title: JavaScript, clipboard access and hidden flash widgets
---

Letting users copy text and URLs from a webpage effortlessly is one of those things that sound easy in theory, but is a pain when it comes to implementation. Browsers take great efforts to ensure that web pages are sand boxed in such a way that a web application can not read from or write to the system's clipboard without jumping through hoops. Firefox asks you to change browser configurations to give web applications access to the system clipboard, while Internet Explorer shows a modal dialog to confirm that you really want to allow the application access. This diminishes any user experience gains made by implementing this feature in the first place. Brook Novak has a very good article about JavaScript and the clipboard [here](http://brooknovak.wordpress.com/2009/07/28/accessing-the-system-clipboard-with-javascript/).

The approach taken by a number of popular applications like GitHub and Dropbox is one that Novak describes. Flash objects embedded on a page can access the system clipboard. Till Flash 9, objects could anonymously read from and write data to the clipboard without the user initiating any action. This vulnerability resulted in attacks like [this](http://news.cnet.com/8301-1009_3-10021715-83.html).
Flash still allows clipboard access, but in version 10, needs an explicit user initiated action to do so.

Libraries like [ZeroClipBoard](https://github.com/jonrohan/ZeroClipboard) provides a flash object and JavaScript bindings to access the clipboard. Applications that use this library overlay a flash object over the copy button and when the user clicks on the button, without them knowing it, they end up clicking on the Flash object.

While this greatly improves the user experience of copying text, I am not sure if hijacking the user's interaction with a button and passing it on to a flash object whose presence the user is not aware of is the right thing to do.

# An alternate approach to copying content
I have been thinking about alternate approaches to enabling the copy feature. The approach that I have zeroed in involves programmatically selecting the content that you want the user to copy and presenting this to the user. This is the approach that Google Maps uses.


This has two advantages:

* There is no clickjacking.
* This method allows the copying of richer content, for example HTML formatted content with a hyperlink. Depending on the application where the selected content is pasted, it would be treated as plain text or as rich text.

You can see this in action in the video below or the demo [here](/demos/copy_text.html):

<iframe width="420" height="315" src="http://www.youtube.com/embed/l6DGqQBBOb8" frameborder="0" allowfullscreen></iframe>