---
aliases:
- /2012/01/why-your-project-should-have-getting.html
bbissueid: 77
categories:
- code
- rails
- best-practices
- learn
- development
comments: true
date: 2012-01-17
ghissueid: 29
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- rails
- best-practices
- learn
- development
title: Why your project should have a Getting Started guide.
---

My new team at work is writing a bunch of Rails applications. This is one of those codebases that one would call "legacy" without much argument. Most of these apps have their own patched, vendorized Rails versions.

Getting up and running was an absolute pain. This project existed before Bundler and the list of gem dependencies are not checked in. I got the output of running `gem list` on a colleague's box, wrote a Ruby script to generate a shell script that installs all the gems. When I tried running the tests in one of those apps, I got a nice error.

It looked obvious that we were using patched Rails versions. Surprisingly, theses were not checked in to the `vendor/` directory. This was proving to be a pain, and today I sat with a team member and wrote a developer guide to get started on the project. We actually had to pull patched Rails tar balls from a remote box and untar them to `vendor/` directory. I was really surprised that these patches had not been checked in. We checked in all the patches. Apart from the Rails patches, there was a gem that had to be checked in.

This is why I think every project needs a Getting Started guide:

1. As a developer joining a new team, I want to look at the code as soon as I can. For me, this involves reading and running the tests.
2. Due to various reasons, a project may have patches and dependencies. Being very specific to the project, there is no way a new developer on the team would figure out these hidden dependencies.
3. There needs to be a single place where all the dependencies are specified.
4. While spoon-feeding someone may not be the best way to get them started, a little bit of hand-holding will not do anyone any harm.

One of the biggest problems I see with things like these guides is that as the application and it's dependencies evolve, the guides are not updated to reflect these changes. The only possible time the guide will be updated is when a new developer joins the team, follows these instructions and finds the need to update the guide.