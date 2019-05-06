---
bbcommentid: 42
categories:
- gis
- maps
- javascript
- geojson
- tools
comments: true
date: 2014-08-03
ghcommentid: 96
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- gis
- maps
- javascript
- geojson
- tools
title: A list of GIS tools
---

I have been playing around with maps a lot these days and have ended up using various tools in the process. This blog post is a way to make a note of these tools for later use.

# geojson.io
Mapbox's [geojson.io](http://geojson.io/) is a simple tool for creating, editing and sharing maps. It lets you import map data in various formats and has an editor to modify maps.

# GeoJSON-TopoJSON
[Jeff Paine](https://github.com/JeffPaine)'s [GeoJSON-TopoJSON](https://github.com/JeffPaine/geojson-topojson) is a simple tool to convert between the more common GeoJSON format and the TopoJSON format used by libraries like D3.js. It is a simple tool, but it does exactly what it says on the tin.

# The Distillery
The New York Times' [Shan Carter](http://shancarter.com/) built [The Distillery](http://shancarter.github.io/distillery/), a GUI around TopoJSON. Apart from converting GeoJSON to TopoJSON, it allows you to alter the map's projection.

# ogr2ogr
[ogr2ogr](http://www.gdal.org/ogr2ogr.html) is a command line utility to convert features data between different file formats.

# Ogre - ogr2ogr web client
[Ogre](http://ogre.adc4gis.com/) is a web UI around ogr2ogr. It lets you do transformations on your map files when you are lazy and don't want to use the command line to run ogr2ogr.

# merge-geojson-features
[merge-geojson-features](https://www.npmjs.org/package/) is a Node.js module to combine Features defined in different files in to a single FeatureCollection. I use it when I am not in the mood to alter GeoJSON objects from a JavaScript console by hand.