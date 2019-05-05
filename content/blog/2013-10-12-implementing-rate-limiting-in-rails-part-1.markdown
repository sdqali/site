---
categories:
- rails
- ruby
- development
- code
- rate-limiting
- redis
comments: true
date: 2013-10-12
ghcommentid: 87
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- rails
- ruby
- development
- code
- rate-limiting
- redis
title: Implementing Rate Limiting in Rails - Part 1
---

*The second part of this series can be found [here](/blog/2013/10/13/implementing-rate-limiting-in-rails-part-2/).*

Rate limiting or throttling is the practice of limiting how frequently legitimate users of a web service can access the service. Rate limiting is often put in place to prevent the hogging of resources by a sub set of the users of the system. Rate limiting works by responding with error messages when a client exceeds their allocated share of requests within a predefined time window. In addition to the error message, the response should also include information as to when rate limit will be reset so that the client can continue accessing the system after the reset.

What we need is a way to record the number of requests each client is making and reset this number to zero after a predefined time period and decide for each request whether the client making the request has exceeded the limits.

### The test application
We will create a simple Rails application with a single API endpoint at `foo.json`. The code needed for this is as follows:

Routes:
```ruby
# config/routes.rb

RailsThrottle::Application.routes.draw do
  get 'foo.json' => 'foo#index'
end
```

The controller:
```ruby
# app/controllers/foo_controller.rb

class FooController < ApplicationController
  def index
    render json: {foo: :bar}
  end
end
```

### Storing the rate data

We need a place to store each client's IP address and the number of requests it made. We need to increment this count for each request and reset the count to zero after a time period. Considering these needs, [Redis](http://redis.io/) is a great fit for this data store. Redis stores key value pairs and allows expiry time to be specified for each entry. Redis also comes with an `INCR` [^1] command that ensures that increment operations are atomic. This will be useful to us if we were to run multiple instances of our app behind a load balancer.

To setup the application to use Redis, we will need to install the `redis` [^2] gem. Once we have the gem, we will add a new `initializer` named `throttle.rb` which configures our Redis client.

```ruby
# config/initializers/throttle.rb

require "redis"

redis_conf  = YAML.load(File.join(Rails.root, "config", "redis.yml"))
REDIS = Redis.new(:host => redis_conf["host"], :port => redis_conf["port"])
```

This will load the Redis server's host and port from the configuration file located at `config/redis.yml`. This file will look like this:

```
# config/redis.yml

host: localhost
port: 6379
```


### Using a `before_filter` for rate limiting.

The first step is to log the number of requests each client is making. This can easily be achieved with a `before_filter` [^3]. Let's add the filter into the `ApplicationController`.

```ruby
# app/controllers/application_controller.rb

class ApplicationController < ActionController::Base
  ...

  before_filter :throttle

  def throttle
    client_ip = request.env["REMOTE_ADDR"]
    key = "count:#{client_ip}"
    count = REDIS.get(key)

    unless count
      REDIS.set(key, 0)
    end
    REDIS.incr(key)
    true
  end

  ...
end
```

Since this `before_filter` belongs to the `ApplicationController`, it will be applied to all requests, unless a specific controller chooses to skip it. So before every request is processed, the filter grabs the client's IP and checks whether there is a count in Redis for this IP. If there is no count key, it creates one. Finally it increments the count.

At this point, the filter just records the requests made, but does not limit requests. Let's go ahead and implement limiting. We need to specify the time window for rate limiting and how many requests should be allowed in that time window. We will allow a client a maximum of `60` requests in `15` minutes. The following constants need to be defined in `throttle.rb`.

```
THROTTLE_TIME_WINDOW = 15 * 60
THROTTLE_MAX_REQUESTS = 60
```

The filter needs to be changed to respond with error messages when the rate limit is exceeded.

```ruby
# app/controllers/application_controller.rb

class ApplicationController < ActionController::Base
  ...

  before_filter :throttle

  def throttle
    client_ip = request.env["REMOTE_ADDR"]
    key = "count:#{client_ip}"
    count = REDIS.get(key)

    unless count
      REDIS.set(key, 0)
      REDIS.expire(key, THROTTLE_TIME_WINDOW)
      return true
    end

    if count.to_i >= THROTTLE_MAX_REQUESTS
      render :status => 429, :json => {:message => "You have fired too many requests. Please wait for some time."}
      return
    end
    REDIS.incr(key)
    true
  end

  ...
end
```

When the limit is reached, subsequent requests will be responded with an error message and the HTTP status code `429`. The 429 [^4] status code indicates that the user has sent too many requests in a given amount of time.

Let's go ahead and test this.

```bash
bash$ for i in {1..100}
do
curl -i http://localhost:3000/foo.json >> /dev/null
done

bash$ less log/development.log | grep "200 OK" | wc -l
      60

bash$ less log/development.log | grep "429 Too Many Requests" | wc -l
      40

```
As you can see after `60` requests, all requests get the `429` response.


### Improvements

While what we have implemented limits the requests, it does not give the client enough information as to how long it has to wait before making requests again. It would also be helpful if the server tells the client on each request how many total requests it is allowed to make in a window and how many more requests it can perform before limiting kicks in. We will look at this in the next blog post.

A sample application with this rate limiting in place is on [GitHub](https://github.com/sdqali/rails_throttle/tree/filter).

[^1]: [Redis documentation](http://redis.io/commands/incr) for INCR command.
[^2]: [redis](https://rubygems.org/gems/redis) - A Ruby client that tries to match Redis' API one-to-one, while still providing an idiomatic interface. It features thread-safety, client-side sharding, pipelining, and an obsession for performance.
[^3]: Rails' [before filter](http://apidock.com/rails/AbstractController/Callbacks/ClassMethods/before_filter).
[^4]: IETF: Additional HTTP Status Codes - [429 Too Many Requests](https://tools.ietf.org/html/rfc6585#section-4).