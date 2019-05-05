---
categories:
- internet
- web
- html
- accessibility
comments: true
date: 2013-08-11
ghcommentid: 70
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- internet
- web
- html
- accessibility
title: When Link titles were for the early adopters
---

While doing some reading up on the comparative merits of using footnotes and hyperlinks in web pages, I came across an article [^1] from 1998 by Jakob Nielsen [^2] about using the then nascent [^3] _title_ attribute on hyperlinks to inform users as to where clicking on a URL is going to take them. It is a very interesting read and makes passionate if not compelling arguments in favour of using the title attribute to improve the usability of a web page.

There is something interesting in the article that made me think about the evolution of the web. To quote:

> ## Early Adoption of Link Titles Recommended
> Normally, I advise against using new Web technologies for the first year after they have been introduced. In most cases, using anything new is asking for trouble and will alienate users with older browsers.

> Link titles are an exception to the need to wait a year. First, their use does not hurt users with browsers that don't display link titles (assuming you follow the guideline to keep the link anchor understandable when the link title is not displayed). Second, a browser that does not understand link titles will simply skip them. Since the title is not a new tag or otherwise intended to influence the layout of the page, the page will look exactly the same whether or not the browser does anything with the link titles. The only downside is that link titles will add approximately 0.1 seconds to the download time for a typical Web page over a modem connection. This is a rather harsh penalty, but worth paying because of the increased navigation usability for those users who do get to see the link titles.

<!--more-->

Think of that again. This was written when the _title_ attribute was a new addition to the specification and the attribute was available to only a small percentage of internet users [^4]. The fact that this was written in 1998 shows how young the web really is, and how fast it has grown. Nielsen advises people to adopt the new technology, putting aside his usual reservation for adopting new technologies which may break the web for people with older browsers. The care people paid to backward compatibility and usability is amazing.

The second paragraph highlights the importance of not breaking things when you want to take things forward. Sure, there are cases when you want to push technologies forward with such passion and aggression that the only way you would take the web forward involves breaking some things. In this case, title being an attribute made sure that old browsers would continue to render pages like they used to while new browsers would push the envelop, even if by a very small margin.

A short and rather unscientific survey of some of my favourite websites shows me that today, not many use the title attribute. The Guardian does not use the attribute, while The Hindu uses the attribute to show a user when an article was first published and when it was last edited.

![The Hindu adds a title with time stamps of when an article was created and edited](/images/the_hindu_title_tooltip.png "The Hindu shows title for hyperlinks")

None of the other websites I frequent seems to use it. Nielsen's own website does a great job of utilising it.

![Nielsen's blog Alertbox adds a title for links](/images/nielsen_title_tooltip_original_size.png "Nielsen's blog Alertbox shows title for hyperlinks")

Of course, the title attribute is not exactly a panacea. XMLPlease [^5] makes some compelling arguments against the title attribute [^6]. The argument that the title attribute is rendered in small fonts is a very important one. For some reason, browsers even today choose to render tooltips that are used to display the titles as yellow boxes and does not respect font sizes, styles or zooming preferences. This can be demonstrated on Nielsen's own website, viewing the same page shown in the previous image, but with a high zoom level. Despite the high zoom level, the tool tip and hence the title are displayed in small fonts. [^7]

![Tooltip boxes does not change size when a web page is zoomed in](/images/nielsen_title_tooltip_zoom.png "Nielsen's Alertbox shows tooltip boxes does not change size when a web page is zoomed in.")

Another important thing the quote includes is the _0.1 seconds_ penalty a title attribute adds to the load time for a website. I have not checked the state of this now, but I doubt if it has any non-negligible effect on the load time. The web has made great progress. But I digress.

I personally have come to like footnotes. They make the pages look organised, and let's the author provide enough details about a topic with out having to drag the entire article towards that topic. Does this mean that we should make all links footnotes? I like this idea on some level, but I am continuing to read more about this topic and will write about it in a later post.

[^1]: [Using Link Titles to Help Users Predict Where They Are Going.](http://www.nngroup.com/articles/using-link-titles-to-help-users-predict-where-they-are-going/)
[^2]: Jakob Nielsen, Ph.D. is one of the pioneers of web usability. He publishes his thoughts around the subject on his blog [Alertbox](http://www.nngroup.com/articles/).
[^3]: The title attribute was proposed in RFC 1866, [section 5.7.3](https://tools.ietf.org/html/rfc1866#section-5.7), in 1995. [Internet Explorer 4.0B1](http://www.blooberry.com/indexdot/html/supportkey/a.htm) which was released in April, 1997 was the first browser to implement the attribute.
[^4]: In April, 1997, when the attribute was first used by Internet Explorer 4.0B1, Netscape Navigator had _81.13 %_ of the browser market share, while Internet Explorer was far behind at _12.13 %_. By April, 1998, around the time Nielsen wrote his article, Internet Explorer had grown to _22.7 %_ of the market share, while Netscape Navigator had been pegged back to _70 %_. Both data points are from Wikipedia's' [summary](https://en.wikipedia.org/wiki/Usage_share_of_web_browsers#Reports_from_before_year_2000) of the [_GVU WWW user surveys_](http://www.cc.gatech.edu/gvu/user_surveys/) from January, 1994 to October, 1998.
[^5]: [XMLPlease](http://www.xmlplease.com/) is a collection of articles and tutorials around XML technologies by Jesper Tverskov.
[^6]: Why the title attribute is 99% bad. From [The benefits of footnotes in webpages - XMLPlease](http://www.xmlplease.com/footnotes#s1.)
[^7]: Both screen shots were taken with the page rendered on Safari 6.0.5 (8536.30.1) on Mac OS X.