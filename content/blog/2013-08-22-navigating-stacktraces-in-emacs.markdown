---
categories:
- code
- emacs
- tools
comments: true
date: 2013-08-22
ghcommentid: 75
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- emacs
- tools
title: Navigating Stacktraces in Emacs
---

I had to debug an issue today and that meant dealing with Rails stack traces. I got tired of having to constantly switch between reading the trace in the terminal and the code in Emacs to figure out what was going wrong and get more context around it. I felt that there should be an easier way of doing this. A quick search [^1] did not yield anything. But then I remembered Grep mode [^2] and it occurred to me that hijacking Grep mode's navigation feature would let me navigate the stack trace better. This is the solution I came up with.

<!--more-->

* Open the log in a buffer.
* Replace any leading file paths in the logs with the appropriate path for your local copy of the code. In the following case, I would replace all `/opt/thoughtworks/mingle` with empty string [^3].
```bash
/opt/thoughtworks/mingle/app/models/foo.rb:46:in 'compare_bar'
/opt/thoughtworks/mingle/app/controllers/foos_controller.rb:42:in 'validate_bar'
...
```
* Load the Grep mode with `M-x grep-mode`

Now I can easily press `Enter` on the lines of the stack trace and Emacs will navigate to the correct source file and line number.


[^1]: I almost wrote "quick google", but then remembered that I no longer use Google that much. [DuckDuckGo](http://duckduckgo.com) has been my preferred search engine for a while.
[^2]: Grep mode is an Emacs mode used by the [Grep](http://www.emacswiki.org/emacs/GrepMode) command to display the results of a search. It populates the buffer with file paths and line numbers that let the user navigate to lines in the code base.
[^3]: Typically logs are long and you may want to use `replace-string` instead of the default `query-replace` for searching and replacing text. The former replaces strings without asking for confirmation while the latter asks you to confirm each replace operation. The latter has it's use, but this use case calls for the former.