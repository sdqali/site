---
bbcommentid: 23
categories:
- code
- bash
- tools
comments: true
date: 2013-09-15
ghcommentid: 78
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- bash
- tools
title: Shared history in Bash
---

One of the features that I miss most in Bash is the shared history between terminals that Zsh supports. I was hunting down a solution for this and came across this Stack Overflow answer [^1] by user *lesmana*. This code snippet does the trick:

```bash
HISTSIZE=9000
HISTFILESIZE=$HISTSIZE
HISTCONTROL=ignorespace:ignoredups

history() {
  _bash_history_sync
  builtin history "$@"
}

_bash_history_sync() {
  builtin history -a         #1
  HISTFILESIZE=$HISTSIZE     #2
  builtin history -c         #3
  builtin history -r         #4
}

PROMPT_COMMAND="_bash_history_sync;$PROMPT_COMMAND"
```
This is very hacky—This setting overrides the shell prompt to sync history every time the prompt is loaded. But like all great hacks, it works.

[^1]: [Preserve bash history in multiple terminal windows](http://stackoverflow.com/questions/103944/real-time-history-export-amongst-bash-terminal-windows/3055135#3055135)