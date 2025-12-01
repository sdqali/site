---
title: "quoteNtweet bookmarklet"
slug: quotentweet-bookmarklet
date: 2010-03-04T18:56:00+0000
draft: false
---

A week ago, I was running Ubuntu 9.10 on my laptop, and had a great [bookmarklet](http://en.wikipedia.org/wiki/Bookmarklet) that let me select any text from a webpage and post the quoted text to Twitter along with the URL to the page. The page was even shortened with tinyurl.com.  

Over the last weekend, I installed Fedora 11, and in the process lost this great bookmarklet. I could not find it, after some time googling. So I decided to write my own. One of the modifications that I wanted to make was to use [bit.ly](http://bit.ly/) URL shortening instead of tinyurl.com. The small saving in the length of the URL generated is a real boon if you happen to do a lot of 'Quote and Tweet' like me.  
  
Here is the code:  
  

```
javascript:
var shortUrl;
var txt=window.getSelection()||document.getSelection()||document.selection.createRange().text;
var head=document.getElementsByTagName('head')[0];
var script=document.createElement('script');
script.setAttribute('type', 'text/javascript');
script.setAttribute('charset', "utf-8");
script.setAttribute('src', "http://bit.ly/javascript-api.js?version=latest&login=sdqali&apiKey=R_f2d4d52225ef4a86f908cddc15a8e6d0");
head.appendChild(script);
BitlyCB.shortenResponse=function(data){
    var firstResult;
    for(var r in data.results){
        firstResult = data.results[r];
        break;
    };
    shortUrl=firstResult['shortUrl'];
};
BitlyClient.shorten(window.location.href, 'BitlyCB.shortenResponse');

var statusMessage=txt+" "+shortUrl;
loc="http://twitter.com/?status="+statusMessage;
twitterWindow=window.open(loc,'quoteNtweet','width=700,height=500,toolbar=no,menubar=no,scrollbars=yes,resizable=no,status=no,minimized=no');
twitterWindow.focus();
```

  
  
This is the expanded code. When the bookmarklet is put on the browser as a bookmark, it is better to use the version of code with no whitespace.  
  
And here it is:  
  

```
javascript:var shortUrl;var txt=window.getSelection()||document.getSelection()||document.selection.createRange().text;var head=document.getElementsByTagName('head')[0];var script=document.createElement('script');script.setAttribute('type', 'text/javascript');script.setAttribute('charset', "utf-8");script.setAttribute('src', "http://bit.ly/javascript-api.js?version=latest&login=your_id&apiKey=your_key");head.appendChild(script);BitlyCB.shortenResponse=function(data){var firstResult;for(var r in data.results){firstResult = data.results[r];break;};shortUrl=firstResult['shortUrl'];};BitlyClient.shorten(window.location.href, 'BitlyCB.shortenResponse');var statusMessage=txt+" "+shortUrl;
loc="http://twitter.com/?status="+statusMessage;
twitterWindow=window.open(loc,'quoteNtweet','width=700,height=500,toolbar=no,menubar=no,scrollbars=yes,resizable=no,status=no,minimized=no');
twitterWindow.focus();
```

  
To use the bookmarklet,  
  

1. Register for an account at [bit.ly](http://bit.ly/),
2. Go to the Account page, where you will find the api key for your bit.ly user id. In the code given above,
3. Replace 'your\_id' with your chosen user id and replace 'your\_key' with your actual bit.ly API key.
4. Copy the code to clipboard
5. Go to your browser, choose Add Bookmark
6. Set Name to something like quoteNtweet
7. Paste the copied code to the URL/Location field

  
Now, on any webpage, select any text and click on the bookmarklet. A new window will open with Twitter home page, and the selected text and URL posted to it. All that is left is to click  'update'. Go quote and Tweet and have fun!  
  
