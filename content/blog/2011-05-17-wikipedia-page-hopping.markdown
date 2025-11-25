---
bbissueid: 111
categories:
- code
- development
- ruby
- wikipedia
comments: true
date: 2011-05-17
ghissueid: 26
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- code
- development
- ruby
- wikipedia
title: Wikipedia Page Hopping
---

I have realized that like most users of Wikipedia, I do a lot of Wikipedia page-hopping [1]. Wikipedia is sort of addictive that way. You start reading about a piece of Flamenco music and after twenty minutes find yourself staring at the page about [ETA](http://en.wikipedia.org/wiki/ETA), a Basque nationalist organization. So I decided to figure out how I exactly do I get lost in the huge list of interconnected articles. I use Chromium, and it stores its history in a SQLite3 database file. I wrote a small Ruby script that parses the history, splits them to chunks of articles accessed per day, and filter only Wikipedia links from this.

This is basically what I had to do:

* Query the db for the last visit time and URLs.

* Chromium (and Google Chrome) stores timestamps of page visits in a not so obvious format. They basically store time stamps as the [number of micro seconds expired since Jan 01, 1601](http://www.mail-archive.com/chromium-discuss@googlegroups.com/msg03891.html)

* Splitting the URLs into chunks accessed per day involved calculating the number of micro-seconds in a day and splitting the URLs based on this. Ruby's Array#group_by is really handy here.

* Analysis of the URLs involves filtering only the URLs that contain "wikipedia"

* There is a caveat here, as redirects to Wikipedia from both Google and Facebook contain the string "wikipedia" in their URLs. These need to be filtered out.

The analysis of my Wikipedia history showed me some interesting things. For example, when I was reading [Michael J. Arlen's](http://en.wikipedia.org/wiki/Michael_J._Arlen) Passage to Ararat, I spent a lot of time on Wikipedia, hopping between pages about Armenian history and culture. This is what the list of Wikipedia pages on that day look like:

    http://en.wikipedia.org/wiki/TRS-80
    http://en.wikipedia.org/wiki/Aunt_Sally
    http://en.wikipedia.org/wiki/Pai
    http://en.wikipedia.org/wiki/Pai_(surname)
    http://en.wikipedia.org/wiki/Gowd_Saraswat_Brahmins
    http://en.wikipedia.org/wiki/Girish_Karnad
    http://en.wikipedia.org/wiki/Konkani_people
    http://en.wikipedia.org/wiki/Roots_(book)
    http://en.wikipedia.org/wiki/Mountains_of_Ararat
    http://en.wikipedia.org/wiki/Armenian_Highland
    http://en.wikipedia.org/wiki/Searches_for_Noah%27s_Ark
    http://en.wikipedia.org/wiki/Tiberian_Hebrew
    http://en.wikipedia.org/wiki/Mount_Judi
    http://en.wikipedia.org/wiki/Islamic_view_of_Noah
    http://en.wikipedia.org/wiki/Greater_Armenia_(political_concept)
    http://en.wikipedia.org/wiki/Coat_of_Arms_of_Armenia
    http://en.wikipedia.org/wiki/Turkish_War_of_Independence
    http://en.wikipedia.org/wiki/Kuva-yi_Milliye
    http://en.wikipedia.org/wiki/Turkish-Armenian_War
    http://en.wikipedia.org/wiki/Anatolia
    http://en.wikipedia.org/wiki/Bursa
    http://en.wikipedia.org/wiki/Armenia
    http://en.wikipedia.org/wiki/Hayk
    http://en.wikipedia.org/wiki/Ecbatana
    http://en.wikipedia.org/wiki/Goat_meat
    http://en.wikipedia.org/wiki/Kid
    http://en.wikipedia.org/w/index.php?title=Special%3ASearch&amp;search=xenophon
    http://en.wikipedia.org/wiki/Xenophon
    http://en.wikipedia.org/wiki/International_Mother_Language_Day
    http://en.wikipedia.org/wiki/Debian
    http://en.wikipedia.org/wiki/Language_Movement_Day

When I was reading about Data warehousing, this is how the hopping happened:

    http://en.wikipedia.org/wiki/ROLAP
    http://en.wikipedia.org/wiki/Dimension_(data_warehouse)
    http://en.wikipedia.org/wiki/Extract,_transform,_load
    http://en.wikipedia.org/wiki/Mondrian_OLAP_server
    http://en.wikipedia.org/wiki/OLAP
    http://en.wikipedia.org/wiki/Comparison_of_OLAP_Servers
    http://en.wikipedia.org/wiki/Pentaho
    http://en.wikipedia.org/wiki/Multidimensional_Expressions
    http://en.wikipedia.org/wiki/Decision_science
    http://en.wikipedia.org/wiki/Star_schema
    http://en.wikipedia.org/wiki/Snowflake_schema
    http://en.wikipedia.org/wiki/Sarkar
    http://en.wikipedia.org/wiki/Fact_table
    http://en.wikipedia.org/wiki/OLTP
    http://en.wikipedia.org/wiki/Ralph_Kimball
    http://en.wikipedia.org/wiki/Bill_Inmon
    http://en.wikipedia.org/wiki/Decision_support
    http://en.wikipedia.org/wiki/Heart_of_Midlothian_F.C.
    http://en.wikipedia.org/wiki/The_Heart_of_Midlothian

I am still trying to make more sense of the links that I clicked away and the articles I read when I was page hopping.

The Ruby script that parses Chromium history and figures out the Wikipedia links is below:

```ruby
#!/usr/bin/env ruby
# Ruby script to parse Chromium (or Google Chrome) history to identify Wikipedia pages read per day.
# usage: ./wikipedia_history.rb <location of Chromium history db>
# The Chromium history db can be usually found under ~/.config/chromium/Default

require 'rubygems'
require 'sqlite3'

US_IN_A_DAY = 24 * 60 * 60 * 1000000
SITE = "wikipedia"

module ChromiumHP
  class DbConnection
    def initialize db_name
      @db_name = db_name
    end

    def urls_history
      db = SQLite3::Database.new @db_name
      urls = db.execute("SELECT last_visit_time, url from urls ORDER BY last_visit_time;").map do |t, u|
        {:last_visit_time => t, :url => u}
      end
      db.close
      urls
    end
  end

  class Parser
    def initialize db_name
      @db_name = db_name
    end

    def chunks days
      @history ||= get_history
      parts = @history.group_by do |h|
         h[:last_visit_time] / (days * US_IN_A_DAY)
      end
      parts.map { |k, group| group }
    end

    private
    def get_history
      DbConnection.new(@db_name).urls_history
    end
  end

  class Analyzer
    def self.graph chunks
      chunks.map do |c|
        c.find_all do |entry|
          url = entry[:url]
          url.include?(SITE) &&
            !url.include?("facebook") &&
            !url.include?("google")
        end
      end.find_all do |c|
        !c.empty?
      end.sort_by do |c|
        c.length
      end.map do |c|
        c.map do |entry|
          entry[:url]
        end
      end
    end
  end
end


history_loc = ARGV.first
abort "Error: Pass the chromium history location as parameter" if history_loc.nil?

daily_chunks = ChromiumHP::Parser.new(history_loc + "/History").chunks(1)
ChromiumHP::Analyzer.graph(daily_chunks).each do |entries|
  puts entries
  puts ""
end
```