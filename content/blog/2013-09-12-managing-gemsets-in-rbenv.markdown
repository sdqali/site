---
bbissueid: 24
categories:
- code
- development
- ruby
- rbenv
- bundler
comments: true
date: 2013-09-12
ghissueid: 77
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- development
- code
- ruby
- rbenv
- bundler
title: Managing Gemsets in Rbenv
---

When I was setting up my new laptop today, I decided to use Rbenv [^1] to manage my Ruby versions. I have typically used RVM [^2] and had never used Rbenv. Rbenv is a Ruby version manager written by [Sam Stephenson](https://github.com/sstephenson/) and deliberately tries to do less and do it well. Instead of overriding Bash commands like RVM does, Rbenv chooses to use wrappers or **shims** around Ruby binaries to choose the Ruby executable to run.

This works well, until you have to manage Gemsets [^3]. Often, one is working on two projects that use the same version of Ruby, but has entirely different chain of dependency on Gems. RVM's gemsets work really well for this use case. I was looking around to see how one would manage gemsets with Rbenv. There are three ways to do it.

<!--more-->

## Use the `rbenv-gemset` plugin
[Jeffrey Lim](https://github.com/jf)'s `rbenv-gemset`[^4] plugin forces Rbenv to look in a specific path for gems. A typical workflow of using the plugin will be as follows.

* Specify the gemset by adding it's name to a `rbenv-gemsets` file in the root directory of the project.
```bash
cat rbenv-gemsets
$ .gems
```
* Install the gems, by using `gem install` or with bundler.
* The gems will be installed in `.gems` directory under the project root.
* Ruby will look for gems in the `.gems` directory.



## Use bundler to manage gemsets
In this approach, we will be using bundler's `--path` flag to install the gemset to a local directory and then wrap all calls with `bundle exec`. A typical workflow in this case will look like this.

* Install gems to a `.gems` directory using bundler
```bash
bundle install --path .gems
```
* Wrap calls with `bundle exec`
```bash
bundle exec rake --version
```

## Use a devenv file
This is a hacky way doing things and it was the first that came to my mind when I was looking at this problem. This approach involves adding a project specific `devenv` file that is sourced when one starts to work on that project. This file will set the `GEM_HOME` and `GEM_PATH` environment variables to the directory where the gemset is supposed to live as well as prepend the `gems/bin` directory of the gemset to `PATH`. An example `devenv` file will be as follows
```bash
export GEM_PATH=./.gems
export GEM_HOME=./.gems
export PATH=./.gems/bin:$PATH
```

In the end, I ended up choosing the `bundler` approach. I use bundler in most of my Ruby projects anyway. The downside to this is that every invocation will be spawning a `bundler` process, in addition to whatever we intend to do.

[^1]: Rbenv is used to pick a Ruby version for an application and guarantee that the development environment matches production. [Rbenv - Groom your app’s Ruby environment](https://github.com/sstephenson/rbenv).
[^2]: RVM is a command-line tool which allows you to easily install, manage, and work with multiple ruby environments from interpreters to sets of gems. [RVM - Cut Rubies with ease!](https://rvm.io/).
[^3]: Gemsets are collection of Ruby gems specific to a project. This [StackOverflow question](http://stackoverflow.com/questions/11086661/why-should-i-use-application-specific-rvm-gemsets-in-addition-to-bundler) answers why one should use gemsets.
[^4]: [`rbenv-gemsets` - Gem management for Rbenv](https://github.com/jf/rbenv-gemset).