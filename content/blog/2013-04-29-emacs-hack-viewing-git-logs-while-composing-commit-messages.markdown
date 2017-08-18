---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Emacs hack: Viewing Git logs while composing commit messages"
date: 2013-04-29
comments: true
categories:
- code
- development
- elisp
- emacs
- git
- tools
tags:
- code
- development
- elisp
- emacs
- git
- tools
---
I use Emacs as my editor to compose Git commit messages. I almost never commit from the terminal with `git commit -m`. This approach has two advantages: I get a chance to verify what is being committed and get to compose the message using a proper editor complete with spell checking provided by *flyspell mode*. One thing I wish I had access to while composing commit messages is the git log. This is useful to refer to work items and encourages one to use a consistent style in the messages. This was easier in the terminal as one could do something like `git log -n 3` and then commit with the `-m` flag.

I decided to fix this today and some tinkering later came up with a hack tp do this.

* Git commit messages are stored in the `COMMIT_EDITMSG` file under `.git/`. So the first thing to do is to ensure that this file always gets loaded with a custom minor mode. This can be done as follows:

```cl
(add-to-list 'auto-mode-alist '("\\COMMIT_EDITMSG\\'" . load-magit-log-when-committing-mode))
```

The minor mode does not need to do anything. The definition would be like this:

```cl
(define-minor-mode load-magit-log-when-committing-mode
  "dummy")
```

* Next step is to add a custom hook that gets run after loading the minor mode. This hook calls the function to load git logs. The code for this is:

```cl
(add-hook 'load-magit-log-when-committing-mode-hook 'show-magit-log-hook)
```

* The actual function to load git logs. It calls `magit-log` to load the logs and then opens the original `COMMIT_EDITMSG` in the other frame.

```cl
(defun show-magit-log-hook ()
  (cd "..")
  (magit-log)
  (switch-to-buffer-other-window "COMMIT_EDITMSG"))
```

This is how Emacs looks while committing with this hack in place:

!["Screenshot showing git commit log"](/images/screenshot_git_commit_log.png "Screenshot showing git commit log")

If you want to use this, copy the following snippet to your `init.el`.

```cl
;; load-magit-log-when-committing-mode
(define-minor-mode load-magit-log-when-committing-mode
  "dummy")

;; the hook
(defun show-magit-log-hook ()
  (cd "..")
  (magit-log)
  (switch-to-buffer-other-window "COMMIT_EDITMSG"))

;; add the hook
(add-hook 'load-magit-log-when-committing-mode-hook 'show-magit-log-hook)

;; load the mode for commit message
(add-to-list 'auto-mode-alist '("\\COMMIT_EDITMSG\\'" . load-magit-log-when-committing-mode))
```
