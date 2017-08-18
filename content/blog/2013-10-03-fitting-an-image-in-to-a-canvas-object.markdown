---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Fitting an Image in to a Canvas object"
date: 2013-10-03
comments: true
categories:
- javascript
- canvas
- code
tags:
- javascript
- canvas
- code
---
I have been playing around with Canvas objects and images for a side project I am doing. One of the first things I had to figure out for this project was how to fit an image of arbitrary height and width on to a Canvas object of arbitrary, but known dimensions while preserving the aspect ratios of the image. This blog post is an explanation of the solution I came up with for this.

### The problem
The application has a Canvas object on which it needs to draw arbitrary images. The Canvas's dimensions are set to **450px** by **300px**. The image that needs to be drawn will have unknown aspect ratio. The ideal case will be when the image's aspect ratio is **3:2**, just like the canvas. In this case, there is no need for any adjustments to be made and the image can be drawn like this:

```javascript
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var imageObj = new Image();
imageObj.onload = function() {
	context.drawImage(imageObj, 0, 0, canvas.width, canvas.height);
}
```
But fitting images with aspect ratios different from the Canvas can be a little tricky. The fundamental problem here is that when aspect ratio is different, there is only one pair of edges-either vertical or horizontal-that can be fitted on to the canvas. The image will have to be placed in the center along the other axis. The following diagram illustrates this.

![Canvas fitting](/images/canvas_fitting.png "Canvas fitting")

Since fitting depends on the aspect ratio, the code should take it into consideration. The following code compares the ratios and chooses to fit the image horizontally or vertically.
```javascript
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var imageObj = new Image();

var fitImageOn = function(canvas, imageObj) {
	var imageAspectRatio = imageObj.width / imageObj.height;
	var canvasAspectRatio = canvas.width / canvas.height;
	var renderableHeight, renderableWidth, xStart, yStart;

	// If image's aspect ratio is less than canvas's we fit on height
	// and place the image centrally along width
	if(imageAspectRatio < canvasAspectRatio) {
		renderableHeight = canvas.height;
		renderableWidth = imageObj.width * (renderableHeight / imageObj.height);
		xStart = (canvas.width - renderableWidth) / 2;
		yStart = 0;
	}

	// If image's aspect ratio is greater than canvas's we fit on width
	// and place the image centrally along height
	else if(imageAspectRatio > canvasAspectRatio) {
		renderableWidth = canvas.width
		renderableHeight = imageObj.height * (renderableWidth / imageObj.width);
		xStart = 0;
		yStart = (canvas.height - renderableHeight) / 2;
	}

	// Happy path - keep aspect ratio
	else {
		renderableHeight = canvas.height;
		renderableWidth = canvas.width;
		xStart = 0;
		yStart = 0;
	}
	context.drawImage(imageObj, xStart, yStart, renderableWidth, renderableHeight);
};

imageObj.onload = function() {
	fitImageOn(canvas, imageObj)
};

```

A demo of this code in action can be found [here](/demos/canvas_fitting.html).
