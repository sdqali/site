---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Configure Git's comment character"
date: 2013-04-14
comments: true
categories:
- code
- development
- tools
- git
- emacs
tags:
- code
- development
- tools
- git
- emacs
---
TL;DR -
Use the `core.commentchar` configuration to change the character Git uses to mark comment lines in commit messages.

My team has a convention of putting the number of the current Issue/Ticket/Story that we are working on at the beginning of every commit message. This is great because it lets us make sense of the history of our code by helping us answer

* What were the changes made to the code base to build a feature or fix an issue?
* Given a changeset, why was it put in place?

We use the format `#123 Foo bar` for the message where `123` is the issue number because it lets [Mingle](http://www.thoughtworks-studios.com/mingle), our project management tool track the commits made against each card.

Things work fine, except for me. I almost never use `git ci -m`. I like Git to open up an editor (almost always Emacs), and type my comment message out. But if I type the commit message according to the convention, because the line starts with a `#`, Git would treat it as a comment and the commit will be aborted.
```text
#123 Foobar
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
# On branch source
#
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
...
```

I have been getting around this issue by pre-pending a space before the message. So I was really happy to see that Git `1.8.2` ships with a new configuration `core.commentchar`. This let's you configure the characters that marks a comment in the commit message. From the [doc](http://git-scm.com/docs/git-config):
> core.commentchar
>
>    Commands such as commit and tag that lets you edit messages consider a line that begins with this character commented, and removes them after the editor returns (default #).

So with this set to `$`, I can just type in my commit message.
```text
#123 Foobar
$ Please enter the commit message for your changes. Lines starting
$ with '$' will be ignored, and an empty message aborts the commit.
$ On branch source
$
$ Changes to be committed:
$   (use "git reset HEAD <file>..." to unstage)
...
```
 This configuration is available only in versions `1.8.2` and later.
