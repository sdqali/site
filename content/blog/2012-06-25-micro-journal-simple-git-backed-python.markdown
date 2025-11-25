---
bbissueid: 81
categories:
- python
- code
- development
comments: true
date: 2012-06-25
ghissueid: 39
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- python
- code
- development
title: Micro Journal - simple Git-backed journal in Python
---

Today, I pushed out [Microjournal](https://github.com/sdqali/microjournal), a simple and lightweight journal. I wrote Microjournal to reduce the pain of typing a number of commands to create and maintain my daily journal which I type out in Emacs and use Git to store. It is a single file Python script.

Microjournal does not do much on it's own. It creates a Git repository for you, and then you can write down entries whenever you feel like. It opens the entry for the day in your $EDITOR. It adds the current date and time to the entry so that you don't have to manually enter it.

This was also an experiment in
[Readme driven development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html). The act of writing your README beforehand makes you think about how the user would interact with the tool.

You can find the code [here](https://github.com/sdqali/microjournal). If you
don't want to bother with cloning the repo, you can grab a [tarball](https://github.com/sdqali/microjournal/tarball/master) or a [zip](https://github.com/sdqali/microjournal/zipball/master).

As always, feedback and pull requests are welcome.