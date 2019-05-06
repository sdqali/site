---
aliases:
- /2012/02/bullet-proof-jenkins-setup.html
bbcommentid: 61
categories:
- jenkins
- ci
- continuous-delivery
- best-practices
- learn
- code
- development
comments: true
date: 2012-02-03
ghcommentid: 30
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- jenkins
- ci
- continuous-delivery
- best-practices
- learn
- code
- development
title: Bullet proof Jenkins setup
---

In this post, I will describe how a neat setup and some discipline will ensure a Jenkins that can be rolled back and recreated very easily - a bullet proof Jenkins setup.  I have been working on configuring our Jenkins instance. This was the first time I had played around with Jenkins. I am fairly comfortable with <a href="http://www.thoughtworks-studios.com/go-agile-release-management" target="_blank">Go</a> from ThoughtWorks Studios. All of my past teams used Go as their tool for continuous delivery.

One of the things I found very different from Go in Jenkins is the absence of the notion of a Pipeline as the basic entity of build, as proposed in <a href="http://continuousdelivery.com/" target="_blank">Continuous Delivery</a>. Although there are plugins to make this available in Jenkins, we decided to go with Jenkins' model of Jobs.

<!--more-->

Another difference I spotted is that when a custom task is defined as part of a Job, Jenkins creates a shell script with all the steps while executing the Job. In Go, each of the steps will have to be defined as a custom command.

We wanted to ensure that our Jenkins configuration is version controlled. While this is a huge win, one of the ways this situation deteriorates is when a large number of changes are made to the configuration over a period of time and these is not checked in. So we decided to take this one step further and ensure that these changes are automatically checked in. There are instructions on how to do this, but we had to do some tweaking to get this working for us.

These are the steps to setup a bullet proof Jenkins setup. This assumes that Jenkins is running on a Linux box.

1. Create a Git repository in Jenkins' base directory - This is generally `/var/lib/jenkins`

2.Create a `.gitignore` file to exclude Jenkins workspaces. The Jenkins base directory is the home directory for the Jenkins user created to run Jenkins. This means that there will be a number ofLinux user specific files like `.ssh/` , `.gem` etc. These files need to be specified in the `.gitignore` file. A sample `.gitignore` file is listed below.

```
# The following ignores...
# Miscellaneous Hudson litter
*.log
*.tmp
*.old
*.bak
*.jar
*.json

# Linux user files
.Xauthority
.bash_history
.bash_profile
.fontconfig
.gitconfig
.gem
.lesshst
.mysql_history
.owner
.ri
.rvm
.ssh
.viminfo
.vnc
bin/

# Generated Hudson state
/.owner
/secret.key
/queue.xml
/fingerprints/
/shelvedProjects/
/updates/
jobs/*/workspace/
plugins/*.bak
updates/default.json
war/
*.bak

# Tools that Hudson manages
/tools/

# Extracted plugins
/plugins/*/

# Job state
builds/
workspace/
lastStable
lastSuccessful
nextBuildNumber
modules/

# Project specific stuff
custom_deps/
slave/workspace/
slave-slave.log.*
```

3. Setup a Jenkins job to check in the changed configuration files every day at midnight. (Or whatever time interval you choose). Add a custom task with the following steps:

```bash
#/usr/bin/env bash
JENKINS_HOME=/var/lib/jenkins
cd $JENKINS_HOME

git add *.xml jobs/*/config.xml users/*/config.xml userContent/*

CHANGES_TO_BE_COMMITTED=$(git status | grep "^# Changes to be committed:" | wc -l)

if [ $CHANGES_TO_BE_COMMITTED -eq 0 ]; then
  echo "Nothing to commit"
else
  git commit -m "Automated commit of Jenkins configuration at $(date)"
  git push origin master
fi
```

While this ensures that the configuration is more or less tracked well, there are times when somebody makes a massive change in the configuration. This is where the most important piece of the bullet proof configuration comes in - team discipline. The team should ensure that big changes are checked in as soon add possible. This can be easily done by triggering the Jenkins job manually, without having to ssh in to the Jenkins box.

### Credits:

1.  The Jenkins community documentation provided a nice <a href="http://jenkins-ci.org/content/keeping-your-configuration-and-data-subversion" target="_blank">starting point</a> for this.
2.  The `.gitignore` file was forked from <a href="https://gist.github.com/780105" target="_blank">this gist</a> by <a href="https://github.com/sit" target="_blank"><span id="goog_1138400375"></span>sit</a>. I have added some project specific stuff to it.