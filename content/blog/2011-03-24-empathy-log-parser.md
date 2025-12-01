---
title: "Empathy log parser"
slug: empathy-log-parser
date: 2011-03-24T15:40:00+0000
draft: false
---

I use [Empathy](http://live.gnome.org/Empathy) as my preferred IM application. Today, I wanted to have a look at an IM conversation I had with someone. I pulled out the Empathy log corresponding to that conversation, and boom - it is in XML.  
  
Just another excuse to write code. So I came up with the following. It was easy to write and it does not do much - It uses the [Hpricot gem](https://github.com/hpricot/hpricot) to parse the XML and prints the name of the people involved in the chat and their messages in a human readable form. What? You are one of those souls who actually enjoy reading XML? Well, I am not one of those.  
  
  
So here goes:  
  
  

#!/usr/bin/env ruby  
# empathy\_lp.rb  
# Usage - ./empathy\_lp.rb /tmp/20110323.log  
  
   
require 'rubygems'  
require 'hpricot'  
  
   
module EmpathyLP  
  class LogParser  
    def initialize file\_path  
      conversation\_xml = IO.readlines(file\_path).to\_s  
      @doc = Hpricot conversation\_xml  
    end  
  
   
    def messages  
      (@doc/"message").map do |m|  
        m.attributes['name'] + ": " + m.inner\_text  
      end  
    end  
  end  
end  
  
   
path = ARGV.first   
puts EmpathyLP::LogParser.new(path).messages

  
I will modify this slightly to show a timestamp for each message.