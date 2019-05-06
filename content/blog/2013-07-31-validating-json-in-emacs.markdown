---
bbcommentid: 16
categories:
- code
- json
- emacs
- tools
- development
comments: true
date: 2013-07-31
ghcommentid: 65
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- json
- emacs
- tools
- development
- validation
title: Validating JSON in Emacs
---

<meta content="validate" name="keywords">
At work, I have to deal with Amazon CloudFormation [^1] templates a fair bit. These templates are JSON files. More and more members of our team are moving away from TextMate to Emacs which makes me really happy. We would like to validate these CloudFormation templates in Emacs. Today we set this up and I hope this turns out to be of help to some one else trying to do the same.

<!--more-->

* Grab jsonlint. It is a command line utility that validates JSON. There seems to be two flavors of jsonlint available. A pure JavaScript implementation [^2] that runs on the Node.js runtime and a native Mac OS X [^3] version. We use the Node.js version.
* Ensure that your Emacs can find the jsonlint binary. This can be done by adding the following snippet in your Emacs configuration:
```cl
(setenv "PATH" (concat (getenv "PATH") ":/usr/local/share/npm/bin"))
(setq exec-path (append exec-path '("/usr/local/share/npm/bin")))
```
Of course, the path you add will depend on where your installation process put the binary.

* Install `flymake-json` [^4], using your Emacs package manager.
* Bind a key to `flymake-json-load` which is the command to perform jsonlint on the current file. This can be done with the following snippet:
```cl
(global-set-key (kbd "C-c j v") 'flymake-json-load)
```

Enjoy!

[^1]: [CloudFormation](http://aws.amazon.com/cloudformation/)
[^2]: [zaach/jsonlint](https://github.com/zaach/jsonlint)
[^3]: [atomicbird/jsonlint](https://github.com/atomicbird/jsonlint)
[^4]: [A flymake handler for json using jsonlint](http://marmalade-repo.org/packages/flymake-json)