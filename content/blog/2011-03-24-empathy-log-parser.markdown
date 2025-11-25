---
bbissueid: 108
categories:
- code
- ruby
- development
comments: true
date: 2011-03-24
ghissueid: 23
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- ruby
- development
title: Empathy Log Parser
---

I use Empathy as my preferred IM application. Today, I wanted to have a look at an IM conversation I had with someone. I pulled out the Empathy log corresponding to that conversation, and boom - it is in XML.

Just another excuse to write code. So I came up with the following. It was easy to write and it does not do much - It uses the Hpricot gem to parse the XML and prints the name of the people involved in the chat and their messages in a human readable form. What? You are one of those souls who actually enjoy reading XML? Well, I am not one of those.

So here is the code:

```ruby
#!/usr/bin/env ruby
# empathy_lp.rb
# Usage - ./empathy_lp.rb /tmp/20110323.log

require 'rubygems'
require 'hpricot'

module EmpathyLP
  class LogParser
    def initialize file_path
      conversation_xml = IO.readlines(file_path).to_s
      @doc = Hpricot conversation_xml
    end

    def messages
      (@doc/"message").map do |m|
        m.attributes['name'] + ": " + m.inner_text
      end
    end
  end
end

path = ARGV.first
puts EmpathyLP::LogParser.new(path).messages
```

I will modify this slightly to show a timestamp for each message.