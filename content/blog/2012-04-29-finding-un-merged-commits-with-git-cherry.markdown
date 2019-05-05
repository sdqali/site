---
aliases:
- /2012/04/finding-un-merged-commits-with-git.html
categories:
- code
- git
- scm
- story-branching
- development
comments: true
date: 2012-04-29
ghcommentid: 31
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- git
- scm
- story-branching
- development
title: Finding un-merged commits with git cherry
---

In a project that I was a part of in the recent past, we used Story Branching. While it afforded us flexibility in pulling and pushing stories in and out of releases, it has given us some scares in the past. Somebody makes commits against a story, but the commit does not get merged to the correct release branch where it is supposed to go or gets merged to another release. The solution was to hunt down the commits that are missing or have creeped in.

This is where the [git cherry](http://linux.die.net/man/1/git-cherry) command is useful. Git cherry finds commits not merged from a branch to another. From the man page:

> Every commit that doesn't exist in the upstream branch has its id (sha1) reported, prefixed by a symbol. The ones that have equivalent change already in the upstream branch are prefixed with a minus (-) sign, and those that only exist in the head branch are prefixed with a plus (+) symbol"

<!--more-->

Consider the following example. I have two branches - `master` and `release-23`.

```bash
┌─[sdqali][bihzad][±][master ✓][~/src/play/git_cherry_sandbox]
└─➞  git branch
* master
  release-23
```

The branch `release-23` has three commits:

```bash
┌─[sdqali][bihzad][±][release-23 ✓][~/src/play/git_cherry_sandbox]
└─➞  git checkout release-23
Already on 'release-23'
┌─[sdqali][bihzad][±][release-23 ✓][~/src/play/git_cherry_sandbox]
└─➞  git log
commit f06e4df25724ad0dd51702a10f075d39368e1963
Author: Sadique Ali <sdqali@bihzad.(none)>
Date:   Sun Apr 29 16:51:14 2012 +0530

    Added zoom

commit 2a446b1a19253a69c4bb133eedb311c14b2906e8
Author: Sadique Ali <sdqali@bihzad.(none)>
Date:   Sun Apr 29 16:49:25 2012 +0530

    Added bar

commit 1afda04ccbf2f834663ca8ec3eaf6e3b917581fb
Author: Sadique Ali <sdqali@bihzad.(none)>
Date:   Sun Apr 29 16:48:05 2012 +0530

    Added foo
```

The branch `master` have two commits:

```bash
┌─[sdqali][bihzad][±][release-23 ✓][~/src/play/git_cherry_sandbox]
└─➞  git checkout master
Switched to branch 'master'
┌─[sdqali][bihzad][±][master ✓][~/src/play/git_cherry_sandbox]
└─➞  git log
commit 8c71e1b2232c1a524e1de20553180676fb971f86
Author: Sadique Ali <sdqali@bihzad.(none)>
Date:   Sun Apr 29 16:49:25 2012 +0530

    Amended. This was Added bar

commit 1afda04ccbf2f834663ca8ec3eaf6e3b917581fb
Author: Sadique Ali <sdqali@bihzad.(none)>
Date:   Sun Apr 29 16:48:05 2012 +0530

    Added foo
```

* Commit `1afda04ccbf2f834663ca8ec3eaf6e3b917581fb (Added foo)` is present in both branches.
* Commit `2a446b1a19253a69c4bb133eedb311c14b2906e8 (Added bar)` in the release-23 branch was merged to master, but the commit message was later ammended and its sha became `8c71e1b2232c1a524e1de20553180676fb971f86 (Amended. This was Added bar)`.
* Commit `f06e4df25724ad0dd51702a10f075d39368e1963 (Added zoom)` is present only in the release-23 branch.

If we do a `git cherry` now with master as the upstream and `release-23` as head:

```bash
┌─[sdqali][bihzad][±][master ✓][~/src/play/git_cherry_sandbox]
└─➞  git cherry master release-23 -v
- 2a446b1a19253a69c4bb133eedb311c14b2906e8 Added bar
+ f06e4df25724ad0dd51702a10f075d39368e1963 Added zoom
<script src="https://gist.github.com/2549897.js?file=gistfile1.sh"></script>
```

This tells us that

1. An equivalent of commit `2a446b1a19253a69c4bb133eedb311c14b2906e8 (Added bar)` is present in the master branch, as indicated by the (-) sign.
2. Commit `f06e4df25724ad0dd51702a10f075d39368e1963 (Added zoom)` is present only in the release-23 branch, as indicated by the (+) sign.

If we were to do `<b>git cherry</b>` the other way around, ie. with release-23 as the upstream and master as the head:

```bash
┌─[sdqali][bihzad][±][master ✓][~/src/play/git_cherry_sandbox]
└─➞  git cherry release-23 master -v
- 8c71e1b2232c1a524e1de20553180676fb971f86 Amended. This was Added bar
```

This tells us that

* An equivalent of commit `8c71e1b2232c1a524e1de20553180676fb971f86 (Amended. This was Added bar)` is present in the master branch, as indicated by the (-) sign.
* There are no commits in `master` that are not present in `release-23`.

That is pretty much what the `git cherry` command does.