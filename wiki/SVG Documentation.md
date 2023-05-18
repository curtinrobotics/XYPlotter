## What is SVG?

Scalable Vector Graphics (SVG) codes 2D images using Extensible Markup Language (XML). Most information retrieved from: (_SVG Tutorial - SVG_, 2023)

Please note all x & y positions are measured from the top left corners and positive values represent a translation right and down respectively: 
 - x position measured pixels from left, positive x is directed right; and 
 - y position measured pixels from top, positive y is directed down

## Why are we using SVG?

We want to use SVG because it enables us to code in scalable and resizable pictures (ie vector images).

### Basic shapes (elements) of SVG we are implementing 
We will list the elements below with their elements. Note all transformations (eg: fill, stroke-width, stroke) will be discussed in the following heading under the <\g> element.

* circle
	* cx = x-coordinate
	* cy = y-coordinate
	* r = radius
	* Eg: `<circle cx=40 cy=50 r=10/>` 
* rect
	* x = x-coordinate
	* y = y-coordinate
	* width 
	* height 
	* rx = x-radius of corners of rectangle
	* ry = y-radius of corners of rectangle
	* Eg: `<rect x="10" y="10" width="30" height="30"/>`
* text: 
	* x 
	* y 
* circle 
* ellipse 
* line 
* polyline 
* polygon 
 

* path:  ``` <path> ```
	* d (defines a path to be drawn. contains list of commands and parameters used by the commands) string of series commands to be drawn[^1] 
		* MoveTo (M,m) [^2] 
			* M (parameters: x, y)
				* Moves current point to this absolute coordinate.
			*  m (parameters: *dx*, *dy*)
				* moves current point *dx* right and *dy* down from last known position
		[^2]: Always possible to give negative values 
			negative angles become anticlockwise
			absolute negative x and y values are negative coordinates
			realtive negative x and y values move left and up respectively
		
		* LineTo (L, l, H, h, V, v)
		| Command | Parameters | Description |
		| --- | --- | --- |
		| L | (x, y)+ | draws a line from current position to absolute point (x, y) |
		| l | (```dx```, ```dy```)+ | draws a line from current position to a point shifted ```dx``` right and ```dy``` down |
		
		* Cubic Bézier Curve (C, c, S, s)
		* Quadratic Bézier Curve (Q, q, T, t)
		* Elliptical Bézier Curve (A, a)
		* ClosePath (Z, z)
		[^1]: Note all commands are case-sensitive
		
	* creates lines, curves, arcs 
	* ```<polyline>``` is an inferior version and doesn't scale up well (uses lots of small lines)
	* 


### The <\g> ELement
Essentially this is a container which contains other SVG elements and groups them together. 
Transformations applied to the <\g> element are inherited by all the elements it contains ie:
``` 
<svg width ="30", height = "10">
  <g fill="white" stroke="green" stroke-width="5">
    <shape parameter = "number"/>
  </g>
</svg>
``` 

## Examples

SVG lines of code start with

The document starts with <svg ... here go the shapes and text (we call elements) until you reach the end-of-line character ">"
and then finally end with a closing </svg >

Examples of elements we're implementing

Examples we aren't implementing:

We aren't implementing images (element "img") because we haven't the capabilities or time in this project to convert the bytes in images and raster form to vector images.

We aren't implementing the attribute in-fill


Further Reading & Bibliography:

_SVG Tutorial - SVG: Scalable Vector Graphics | MDN_. (2023, March 6). [https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial)



