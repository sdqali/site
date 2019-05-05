---
categories:
- mac-osx
- emacs
- homebrew
- development
- elisp
comments: true
date: 2012-05-04
ghcommentid: 32
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- mac-osx
- emacs
- homebrew
- development
- elisp
title: Fixing Flyspell for Emacs in Mac OS X
---

I use the <a href="http://www.emacswiki.org/emacs/FlySpell">flyspell-mode</a> as a spell checking mechanism in emacs. Recently, I moved to Mac OS X, and I began to get this error whenever I started emacs:

```bash
Error enabling Flyspell mode:
(Searching for program No such file or directory aspell)
```

I had installed aspell with Homebrew. The issue seemed to be that Emacs was unable to find the aspell binary. Homebrew installs binaries in **/usr/local/bin** and it was in my $PATH. It turns out Emacs uses it's own exec path to look for binaries to execute in sub-processes. So the fix is to add the **/usr/local/bin** path to the exec-path. This is the change needed to the **~/.emacs** file:

```lisp
 '(exec-path (quote ("/usr/bin" "/bin" "/usr/sbin" "/sbin" "/usr/local/bin"))))
```

Notice the **/usr/local/bin** in there.

## Update
This does not seem to work. A better way to do this is to add the
following:

```lisp
(setenv "PATH" (concat (getenv "PATH") ":/usr/local/bin"))
(setq exec-path (append exec-path '("/usr/local/bin")))
```