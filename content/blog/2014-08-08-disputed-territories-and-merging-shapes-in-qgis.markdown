---
bbissueid: 44
categories:
- gis
- maps
- javascript
- geojson
- tools
comments: true
date: 2014-08-08
ghissueid: 97
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- gis
- maps
- javascript
- geojson
- tools
title: Disputed territories and merging shapes and features
---

Making a map that shows a disputed territory can be a tricky business. Nation states vigorously contest maps that appear to portray a boundary that challenges what a border looks like. From the Falkland Islands to Kuril Islands; from Western Sahara to Arunachal Pradesh, disputed territories result in omissions, additions and inaccuracies in maps.

I grew up looking at maps in books printed by the Oxford Press, that came with a disclaimer in blue rubber stamped across them that stated how the map was wrong. This was due to the fact that the maps showed only the parts of Kashmir being administered by India, thereby omitting areas under Chinese and Pakistani control. The Criminal Law Amendment Act, 1961 in India makes it punishable with imprisonment up to 6 months to publish a map that excludes all or parts of Kashmir[^1].

This creates a lot of trouble for people who make maps for fun or to visualize data. Survey of India does not make it easy to get hold of shape files that represent India's boundaries, and all the shape files that are available from international sources exclude parts of Kashmir. So, how do we solve this problem?

The North American Cartographic Information Society's Natural Earth [^2] maps has all the disputed territories available for download as shape files. One way to solve the issue on our hands will be to take the shapes relevant to Kashmir from this file and merge it with the rest of India.

We will explore how to perform and an operation like this through QGIS [^3].

1. Open the disputed areas shape file in QGIS.
1. Select all the regions in Kashmir that are seen by India as it's territories.
1. In order to make merging these shapes easier, we will introduce a new attribute on them. Go to `Layer → Open Attribute Table`.
1. Switch to editing mode in the Attribute Table by clicking the `Toggle editing mode` button.
1. Click `New column`.
1. Choose a name for the column. In this example we are using `target`. Select `Text (string)` as the Type and choose a number like `10` for width.
1. For all the selected shapes, set the value of `target` to Kashmir.
1. Use the `Dissolve` tool, found at `Vector → Geoprocessing tools → Dissolve` to dissolve the shapes in to a single shape file. Choose `target` as the value for `dissolve` field. Save the output to a new shape file.
1. Install the QGIS plugin `MergeShapes`. Plugins can be installed from `Plugins → Manage and Install Plugins`.
1. Copy the [India shape file](http://biogeo.ucdavis.edu/data/diva/adm/IND_adm.zip) from DIVA-GIS and the newly generated Kashmir shape file to a directory.
1. Merge these into a single shape using `Vector → MergeShapes → MergeShapes`.

With that we have a shape File for India that closely resembles India's official version.

Once we have the shape File for Kashmir from step `8`, we could do the merging by converting both shape Files to their corresponding GeoJSON formats and doing simple JavaScript operations on the objects.

1. Start by converting both shape Files to their GeoJSON representation.
```bash
> ogr2ogr -f GeoJSON india.geo.json india.shp
> ogr2ogr -f GeoJSON kashmir.geo.json kashmir.shp
```
1. Load the two feature collections in to a JavaScript console. I tend to use Chromium's Developer Tools, but in this example I am using  Node.js' REPL.
```javascript
kashmir = JSON.parse(fs.readFileSync("./kashmir.geo.json").toString());
india = JSON.parse(fs.readFileSync("./india.geo.json").toString());
```
1. Identify the Kashmir feature in the India feature collection.
```javascript
kin = india.features.filter(function(f) {return f.properties.NAME_1.match("Kashmir");})[0];
```
1. Replace it's coordinates with the unified Kashmir we generated.
```javascript
kin.geometry.coordinates = kashmir.features[0].geometry.coordinates;
```
1. Save it back to a GeoJSON file.
```javascript
fs.writeFileSync("full_india.geo.json", JSON.stringify(india));
```

Now the GeoJSON file can be transformed back in to a shape file.
```bash
ogr2ogr -f 'ESRI Shapefile' full_india.shp full_india.geo.json
```

Back to Kashmir and laws. Will this map save one from trouble? I am not sure, but this is an improvement on the omission of territories.

[^1]: The Criminal Law Amendment Act, 1961 - [Questioning the territorial integrity or frontiers of India in a manner prejudicial to the interests of safety and security of India.](http://www.vakilno1.com/bareacts/laws/the-criminal-law-amendment-act-1961.html#2_Questioning_the_territorial_integrity_or_frontiers_of_India_in_a_manner_prejudicial_to_the_interests_of_safety_and_security_of_India)
[^2]: Natural Earth is a public domain map dataset available at 1:10m, 1:50m, and 1:110 million scales. The data set is available for download [here](http://www.naturalearthdata.com/downloads/).
[^3]: [QGIS](http://qgis.org/en/site/) is a cross-platform free and open source desktop geographic information systems application that provides data viewing, editing, and analysis capabilities.