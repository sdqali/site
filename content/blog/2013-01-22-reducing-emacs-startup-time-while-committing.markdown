---
categories:
- code
- development
- emacs
- mac-osx
comments: true
date: 2013-01-22
ghcommentid: 56
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- development
- emacs
- mac-osx
title: Reducing Emacs startup time while committing
---

I use Emacs as my primary text editor and I use it to edit
commit messages for Git. I almost never use the `-m`
option with `git commit`. Since I have a fairly customised Emacs
configuration based around Sam Aaron's
[Emacs Live](https://github.com/overtone/emacs-live), this means that
for every commit, there is a visible delay for Emacs to start up for the
commit message. I was looking for ways to reduce this and figured out that
running Emacs in `daemon` mode and using `emacsclient` as the
`GIT_EDITOR` would solve this.

# Running an Emacs daemon at start up on Mac OS X
The recommended way of running an application at start up on Mac OS X is
to use [launchd](http://en.wikipedia.org/wiki/Launchd). Launchd
configurations are written as XML files created in
`~/Library/LaunchAgents` or `/Library/LaunchAgents` depending on whether
the app needs to be run for the current user or for all users.
Here is the plist file for Emacs at `~/Library/LaunchAgents/gnu.emacs.daemon.plist`, taken from
[EmacsWiki](http://www.emacswiki.org/emacs/EmacsAsDaemon):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>gnu.emacs.daemon</string>
    <key>ProgramArguments</key>
    <array>
      <string>/Applications/Emacs.app/Contents/MacOS/Emacs</string>
      <string>--daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>ServiceDescription</key>
    <string>Gnu Emacs Daemon</string>
    <key>UserName</key>
    <string>YOUR USER NAME</string>
  </dict>
</plist>
```
This is loaded by running
```bash
sudo launchctl load -w ~/Library/LaunchAgents/gnu.emacs.daemon.plist
```

# Using Emacs client as the editor

This is done by adding
```bash
export EDITOR="/Applications/Emacs.app/Contents/MacOS/bin/emacsclient"
export GIT_EDITOR="/Applications/Emacs.app/Contents/MacOS/bin/emacsclient"
```
to `.zshrc` or `.bashrc`.

This setup significantly reduces the Emacs startup time while committing
changes.