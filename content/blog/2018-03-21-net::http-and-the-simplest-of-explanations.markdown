---
date: 2018-03-22 02:44:03
aliases:
- /blog/2018/03/21/nethttp-and-the-simplest-of-explanations/
ghcommentid: 133
tags:
- ruby
- docker
title: Net::HTTP and the simplest of explanations
---

_This blog post exists purely to remind myself that Ruby's `Net::HTTP` expects a `host` and a `port` as parameters when creating a new connection and not a `url` string._

This is a story about how many layers of abstractions and indirections one works through on a daily basis as a developer and the effort required to dive through these layers, all the while ignoring the simplest of explanations of why things may have gone wrong in the first place.

At work, we have a homegrown orchestration tool that brings up Docker containers and configures dependencies and network access between them - essentially an abstraction over `docker-compose`. In our continuous integration environment, this tool sets up all the different components of our system and then starts another container in which `RSpec` based integration tests that exercise various inetractions between the components of the system are run.

We added a new component and wanted a library used by the specs to use an API provided by this component. This essentially meant this for us:

1. Change our configurations so that the Docker container with the new component is started before the test container is started.
1. Ensure that the test container can talk to the new component container.
1. Tell the test container, through environment variables the `host` and the `port` of the new component.

So, off we went and configured everything:

```bash
env.NEWAPP_HOST=http://new-app.local
env.NEWAPP_PORT=1313
```

We ran the tests and boom:

```bash
SocketError (Failed to open TCP connection to http://new-app.local:1313 (getaddrinfo: nodename nor servname provided, or not known))
```

Well, that does not look right. We double check all the configurations and run the test again. Same result. May be we should be using a Ruby `Symbol` instead of a `String` in that particular config? May be. We try that, same result. 

At this point, we hop on to the test container and ping `new-app.local`. It can connect.
What if the app is not available? We should totally `telnet` it. Well, this container does not have `telnet`. We can totally install it, right? Right. What kind of distro is this running? Well `cat /etc/*release*`. Debian, huh? `apt-get install telnet`. Wooh. Back to `telnet` then. That looks good.

At this point, the attention turns to the RSpec tests. What if the tests have some environment variables? Let's debug it and look for things in Ruby's `ENV`. Hmmm, nothing interesting there. Can the Ruby process even connect to `new-app`? We have `Faraday`, let's try that:
```irb
> require 'faraday'
=> true
> resp = Faraday.get "http://google.com"
> resp.status
200
```

Okay, does the library we use for the test even use `Faraday`? Let's open the source code for that and poke around. Nah, it uses `Net::Http`. Let's try the example from [it's documentation](https://ruby-doc.org/stdlib-2.5.0/libdoc/net/http/rdoc/Net/HTTP.html):
```irb
> require 'net/http'
=> true
> Net::HTTP.get_response(URI("http://new-app.local:1313"))
=> #<Net::HTTPOK 200 OK readbody=true>
```
Looks good. Well, wait! Our library uses `Net::HTTP.new` to create a connection. Let's try that:
```irb
> conn = Net::HTTP.new("http://new-app.local", 1313)
=> #<Net::HTTP http://new-app.local:1313 open=false>
> conn.get("/")
Traceback (most recent call last):
.
.
.
SocketError (Failed to open TCP connection to http://new-app.local:1313 (getaddrinfo: nodename nor servname provided, or not known))
```
At this point, we are covered in a mix of disappointment and excitement. We are annoyed that things are not working. But, may be, may be we have uncovered some obscure bug somewhere in the toolset? We would learn later that this is the point where we should have known what's up? But we didn't and the story continues.

At this point, we ping the Slack channels of the teams involved in building the library we consume. They have not seen this before. Someone suggests that they have had issues with Ruby inside Docker containers. We finally find a GitHub issue for a different project where someone encountered their container setting the `HTTP_PROXY` env variable and that causing `Net::HTTP` to fail. We pore over everything to make sure that there is no proxy set. What now?

What if we attempt to connect to the new app from a Ruby process running on one of the other 10 containers we run?

```bash
> docker exec -it 51dbf9f75ca8 ruby -e 'require "net/http"; conn = Net::HTTP.new("http://new-app.local", 1313); conn.get("/")'
Traceback (most recent call last):
.
.
.
SocketError (Failed to open TCP connection to http://new-app.local:1313 (getaddrinfo: nodename nor servname provided, or not known))
```

That is interesting, isn't it? Is it happening to only our systems? What if we just tried to hit Google?

```bash
> docker exec -it 51dbf9f75ca8 ruby -e 'require "net/http"; conn = Net::HTTP.new("http://google.com", 80); conn.get("/")'
Traceback (most recent call last):
.
.
.
SocketError (Failed to open TCP connection to http://google.com:80 (getaddrinfo: nodename nor servname provided, or not known))
```

What if somehow our orchestration tool or containers created by us are causing it? Let's try a random container from DockerHub:

```bash
> docker run -it ruby:2.5-slim ruby -e 'require "net/http"; conn = Net::HTTP.new("http://google.com",80); conn.get("/")'
Traceback (most recent call last):
.
.
.
SocketError (Failed to open TCP connection to http://google.com:80 (getaddrinfo: nodename nor servname provided, or not known))
```

At this point, light bulbs are beginning to go off. Let's try this on our laptops? Same result. And then it struck us. It says it can't open a TCP connection to a URL with `http` in it.  Of course, it cant. It should be looking for `google.com`, should not it? Yes:

```irb
> docker run -it ruby:2.5-slim ruby -e 'require "net/http"; conn = Net::HTTP.new("google.com", 80); res = conn.get("/"); puts res.code'
301
```

And with a lot of excitement and some shame, we realize that the library really meant `host` when it asked for the `NEWAPP_HOST` environment variable.

I don't think there are any big lessons in this story other than that, sometimes the simplest explanation of a problems makes a lot more sense than you would think it does. Also, if you ever use `Net::HTTP.new`, remember that it expects you to provide a `host` as the first param, not a URL.
