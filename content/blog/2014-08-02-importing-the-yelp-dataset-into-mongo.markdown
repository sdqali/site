---
aliases:
- /blog/2014/08/02/importing-the-yelp-dataset-into-mongo/index.html
categories:
- mongo
- code
- ruby
- yelp
- data
comments: true
date: 2014-08-02
ghcommentid: 95
image:
  feature: /images/threaded-blue-on-black-cropped.jpg
tags:
- mongo
- code
- ruby
- yelp
- data
title: Importing the Yelp dataset into MongoDB
---

Today Yelp announced their dataset challenge [^1]. The dataset they released includes data from 5 cities (Phoenix, Las Vegas, Madison, Waterloo and Edinburgh) and consists of

* 42,153 businesses
* 320,002 business attributes
* 31,617 check-in sets
* 252,898 users
* 955,999 edge social graph
* 403,210 tips
* 1,125,458 reviews

The data is available for public consumption, although Yelp owns any derivative dataset you create from the original [^2].

The data is available as files with each line representing a JSON object. Since I am using MongoDB these days to analyze geospatial data, I wanted to convert this into an easy format that I could import into Mongo. Mongo puts a strict constraint on how a location needs to be specified - It expects a location field in a document to be an array in the format `[longitude, latitude]`.

With this in mind, the first step is to convert and transform the objects into objects that Mongo can make sense of. The following Ruby script does the job:

```ruby
#!/usr/bin/env ruby

require "json"

businesses = IO.readlines("yelp.business.json").map do |line|
  b = JSON.parse(line)
  b["location"] = {
    "type" => "Point",
    "coordinates" => [b["longitude"], b["latitude"]]
  }
  b
end
IO.write "businesses.mongo.json", businesses.to_json
```

The next step is to import this data into Mongo using the `mongoimport` tool.

```bash
mongoimport --collection businesses --file businesses.mongo.json --jsonArray
```
We need the `--jsonArray` parameter because our data is an array.

Since there are 42153 businesses, it will take some time. On my Macbook Pro, it took around 2 minutes, 10 seconds. Once the import is done, make sure that we have a Geospatial index on the `location` field.

```javascript
db.businesses.ensureIndex({location: "2dsphere"})
```

Once the indexing is done, we can use Mongo's Geospatial queries to find interesting things. As an example, here we look up all the restaurants within 1 kilometer distance from downtown Phoenix.

```javascript
db.businesses.find({
  location: {
    $near: {
      $geometry: {
	type: "Point",
	coordinates: [-112.0667, 33.4500]
      },
      $maxDistance: 1000
    }
  }
})
```

Happy hacking.


[^1]: [Yelp Dataset Challenge, 2014](http://www.yelp.com/dataset_challenge).
[^2]: DATASET CHALLENGE ACADEMIC DATASET TERMS OF USE [Section 5, Ownership](https://www.yelp.com/html/pdf/Dataset_Challenge_Academic_Dataset_Agreement.pdf).