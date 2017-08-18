---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Know Your Tools - Don't Shoot Yourself in the Foot"
date: 2012-06-06
comments: true
categories:
- code
- development
- ruby
- rake
tags:
- code
- development
- ruby
- rake
---

Imagine this - Your build is taking forever. You put in a lot of effort and restructure it. Things improve a lot, but it is far from where you would like it to be. You try hard to identify things that could improve the build time, but fail. You blame the platforms you use, you blame Ruby and you even blame the relative position of the Moon to Venus. Slowly you learn to accept the slow build as a part of your life. Months later a new developer joins the team and proves that there is a bug in the build scripts that causes certain tasks to be run twice.

This happened to us recently, and the subsequent debugging/postmortem revealed that there were things about our tools that we simply did not know.

<!--more-->

## A bit of context

Ours is a Java code base, but we use Rake for our build scripts. We have been using Ruby 1.8.7 and Rake 0.8.7. We never got around to upgrading the Ruby versions due to a number of reasons including one of our gems breaking on 1.9.3 and more importantly our laziness. Well, laziness will cause you damage in the end and that is what happened to us.

## What is the issue ?
### "That step is not running multiple times, is it?"
While debugging our build, our new developer discovered that certain tasks that take up 10 minutes to complete were being executed twice. We soon started trying to figure out where in the chain of Rake task calls did we end up repeating a task. There were none. After some time, we would learn that we did not know enough about Rake and Ruby 1.8.7

### Rake's redefining behavior
Rake treats redefining a Task as akin to appending actions to the same Task. To see this in action, add the following to a Rakefile:
{% codeblock lang:ruby %}
task :foo do
  puts "foo " * 10
end

task :foo do
  puts "bar " * 10
end
{% endcodeblock %}

If you run the `foo` task, you would get:
{% codeblock lang:console %}
$rake foo
foo foo foo foo foo foo foo foo foo foo
bar bar bar bar bar bar bar bar bar bar
{% endcodeblock %}

This is far removed from behaviors of Ruby and [Make](http://www.gnu.org/software/make/ "Make"), the tools that inspired Rake. For clarity's sake, this is how Ruby treats redefinitions:
{% codeblock lang:ruby %}
#!/usr/bin/env ruby
#example.rb

def example
  puts "example " * 10
end

def example
  puts "foobar " * 10
end

example
{% endcodeblock %}

When run:
{% codeblock lang:console %}
$ruby example.rb
foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar
{% endcodeblock %}

Lets take a look at Make's behavior. This is how Make treats redefinitions:
{% codeblock lang:make %}
# Example Makefile

foo:
    @echo Foo target
foo:
    @echo Redefined foo target
{% endcodeblock %}

When run:
{% codeblock lang:console %}
$make foo
Makefile:6: warning: overriding commands for target `foo'
Makefile:4: warning: ignoring old commands for target `foo'
Redefined foo target
{% endcodeblock %}


While this behavior of Rake may seem weird, there are some advantages to it like the ability to add custom behavior to third party Rake tasks. I asked [Jim Weirich](https://twitter.com/#!/jimweirich), the creator of Rake and he was [of the opinion](http://www.quora.com/Ruby-programming-language/Why-did-Rake-choose-to-treat-a-re-definition-as-a-multiple-definition-instead-of-an-overwrite) that it was a useful choice. *We were <strong>not</strong> aware of this particular behavior of Rake.*

Under normal situations, this behavior should not cause us trouble, as it is unlikely that we would redefine our own Rake tasks. But this combined with the next issue led to some of our build tasks running twice.

### Ruby 1.8.7's multiple require issue
It turns out that in Ruby 1.8.7, whenever a file is `require`d multiple times, Ruby decides whether to reload it based on the path of the file provided. So if you have the same file being required twice, but using different paths, the file will be loaded twice. If there are Rake tasks defined in that file, the effect of actions in the Rake task will be multiplied.

Again, this can be best demonstrated with an example. Consider the following scenario. There is a paent directory with `Rakefile`, `zoo.rb` and a directory `subdir` with the file `bar.rb` inside it.

`zoo.rb` defines a Rake task `print_zoo`:
{% codeblock lang:ruby%}
# zoo.rb

desc "prints zoo"
task :print_zoo do
  puts "zoo " * 10
end
{% endcodeblock %}

`bar.rb` in the directory `subdir` does nothing but require `zoo` in the parent directory.
{% codeblock lang:ruby %}
#subdir/bar.rb

require File.dirname(__FILE__) + "/../zoo"
{% endcodeblock %}

The Rakefile requires both `zoo.rb` and `bar.rb` and defines a task to show the behavior.
{% codeblock lang:ruby%}
require File.dirname(__FILE__) + "/zoo"
require File.dirname(__FILE__) + "/subdir/bar"

desc "show weirdness"
task :test => :print_zoo
{% endcodeblock %}

Now if we run the `test` task:
{% codeblock lang:console %}
$rake test
zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo
zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo
{% endcodeblock %}

Lets take a step back and think about that. If we load Ruby files multiple times using `require` we can easily end up repeating a build step that would take 30 minutes to complete.

I must note that this issue does not happen on Ruby 1.9.3, where files are being loaded only once. All the code I showed here is available [here](https://github.com/sdqali/rake_sandbox), if you want to take a closer look.

## Learning
This is not meant to be a criticism of Rake or Ruby. Although Rake's behavior in this scenario looks weird, there are good reasons why Jim chose that behavior. And we should have moved to Ruby 1.9.3 anyway.  Certainly the learning is that we need to have a better understanding of the tools we use daily.
