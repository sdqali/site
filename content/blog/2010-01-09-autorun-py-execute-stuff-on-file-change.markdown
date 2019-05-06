---
bbcommentid: 97
categories:
- code
- python
- development
comments: true
date: 2010-01-09
ghcommentid: 17
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- python
- development
title: Autorun.py - Execute stuff on file change
---

I really liked ZenTest's Autospec in action. Recently, when I was trying to write some Python stuff, I thought it would be nice if I would have a tool that would just run the unit tests, so that I don't have to switch between console windows. Better still, I could run it from inside my Emacs.

Clearly, monitoring files for changes, shouldn't be big deal. I decided to write the tool myself in Python. the prime intension was to help myself learn Python. Although that didn't quite workout, I managed to come up with a quick and dirty hack to do it. It uses `pyinotify`, which is a Python module for monitoring filesystem changes. Since `pyinotify` depends on the Linux kernel, this would work only on Linux boxes.

I named it `autorun.py`. If you want to run some task, depending on file changes in a directory, you navigate to that directory and start autorunner as:

`~/src/sdq/ocr$ ./autorun.py "python Test*.py"`

That would start `autorun.py` and every time I modify a file in the present directory the command  `python Test*.py` is executed. In my case, I am using the unittest framework that comes with Python. So everytime, a file is updates, it runs all my unit tests, as seen below:

```bash
sadiquea@sadiquea-laptop:~/src/sdq/ocr$ ./autorun.py "python Test*.py"
Autorunner in action
.............

----------------------------------------------------------------------

Ran 13 tests in 0.763s

OK
```

If I were working with Ruby and wanted to run all my unit tests when I modify the files, I could start the tool like this: `./autorun.py "rake spec"`

I would really like to add the ability to exclude some files/subdirectories from being watched for changes.

Here is the code snippet that does the trick:

```python
#!/usr/bin/env python

import sys
import os
import pyinotify

if len(sys.argv)==1:
    print "Please pass a command to excute as a parameter"
    print "For example autorun.py 'ruby foo.rb'"
    sys.exit()

commandToRun = sys.argv[1]

watchManager = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY

class ActionProcesser(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        print "Autorunner in action"
        os.system(commandToRun)

notifier = pyinotify.Notifier(watchManager, ActionProcesser())

wdd = watchManager.add_watch(os.getcwd(), mask, rec=True)

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break

```