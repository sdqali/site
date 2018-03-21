---
Categories:
- development
- golang
Description: ""
Tags:
- development
- golang
date: 2015-12-14T21:47:06-05:00
title: Thoughts on Open Graph tags
image: "images/ogp.png"
---
The Open Graph protocol was designed by Facebook to help content creators generate a richer preview of links to their content when they get posted in to Facebook. It was originally proposed as a simple mark up that can be adopted in platforms beyond Facebook. The Open Graph Protocol Design Decisions presentation [^1] does a very good job of enumerating the motivation and design decisions made for Open Graph. I have lately been reading and experimenting with these tags and I notice a fair bit of differences when it comes to how these tags are used by different platforms.

<!--more-->

This is by no means an exhaustive list–these are applications I use frequently use and hence encounter the usage of Open Graph tags in. I am deliberately scoping this discussion to a sub set of tags including the following which are the most common tags I have encountered:

```
og:title
og:description
og:url
og:image
```

## Facebook
I do not currently have a Facebook account with which I could test and this and Facebook‘s real name policy makes it hard to create test accounts. Facebook‘s [content sharing best practices](https://developers.facebook.com/docs/sharing/best-practices) does make it clear that they use the Open Graph tags and considering Facebook created the protocol, I would guess all the tags work as expected.

## Twitter
Twitter primarily uses it‘s [Twitter Cards](https://dev.twitter.com/cards/overview) functionality to help content creators display richer previews. Twitter Cards defines it‘s own custom tags. However, if these tags are not present in a shared page‘s markup, Twitter does [fall back](https://dev.twitter.com/cards/markup) to using the corresponding Open Graph tags.

However, one of the interesting things about sharing content through Twitter cards is that it allows the content to be attributed to the Twitter accounts of the content author and the site where the content is hosted. This is done via the Twitter Card tags `twitter:creator` and `twitter:site`. There are no equivalents in the Open Graph world and hence these needs to be explicitly specified for Twitter.
{{< mailchimp >}}

## Slack
Slack generates rich preview of content using the four Open Graph tags. Slack does this by using it‘s [Link Expanding Bot](https://api.slack.com/robots). In addition to Open Graph tags, Slack looks for oEmbed [^2] and Twitter Cards.

## GroupMe
GroupMe parses Open Graph tags and displays them in chat messages. I have been unable to find documentation as to which other tags they parse.

## Google+
Google‘s [recommended method](https://developers.google.com/+/web/snippet/) for providing metadata is Schema.org [^3] annotations. It does fall back to Open Graph tags if Schema.org annotations are not found. Google also uses schema.org microdata to generate rich snippets in their search results. Bing and Yahoo also support rich snippets through Schema.org annotations.

## Representing creator information
As we saw in the example of Twitter, linking to the creator of content is not something that can be solved purely with Open Graph tags. Open Graph does specify an `author` type [^4]. But in a world where links get shared to multiple platforms, the meaning of this tag is specific to the platform–it could be a Twitter id, a Facebook profile link, a Slack user id, etc. This does force the use of platform specific tags like `twitter:site`.

It would be interesting to see if Open Graph would one day support scoped author tags that can specify what `author:username` means for different platforms like this:

```html
<meta property="profile:username" scope=“twitter.com“ content="@sdqali" />
<meta property="profile:username" scope=“facebook.com“ content="http://facebook.com/some-profile-id" />
<meta property="profile:username" scope=“slack.com“ content="@some-slack-id" />
```

In conclusion, while Open Graph tags are used by a lot of platforms, there are specific pieces of information for which platform specific tags and annotations are needed.

[^1]: David Recordon–The Open Graph Protocol Design Decisions on [Scribd](http://www.scribd.com/doc/30715288/The-Open-Graph-Protocol-Design-Decisions).
[^2]: oEmbed–Yet another attempt to provide rich representation of URLs. You can find more information on the [official site](http://oembed.com/).
[^3]: Schema.org is an effort to create and promote schemas for structured data. The official site is [here](http://schema.org/).
[^4]: See `article:author` [spec](http://ogp.me/#type_article) and `book:author` [spec](http://ogp.me/#type_book).
