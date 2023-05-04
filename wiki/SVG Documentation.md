## What is SVG?

Scalable Vector Graphics (SVG) codes 2D images using Extensible Markup Language (XML).

## Why are we using SVG?

We want to use SVG because it enables us to code in scalable and resizable pictures (ie vector images).

### Basic shapes (elements) of SVG we are implementing 
We will list the elements below in the form

* basic shape: 
	* parameter1 (explanation1) 
	* parameter2 (explanation2)
	* etc
* text: 
	* x (x position measured pixels from left, positive x is directed right)
	* y (y position measured pixels from top, positive y is directed down)
	* fill (colour filling the object)
	* stroke (colour drawn around object)
	* stroke-linecap (how the ends of the lines end, eg: "butt", "round", "square")
	* stroke-width (thickness of line)
	* stroke-linejoin (how lines are joined, eg: mitre, bevel, round)


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

## Examples

SVG lines of code start with

The document starts with <svg ... here go the shapes and text (we call elements) until you reach the end-of-line character ">"
and then finally end with a closing </svg >

Examples of elements we're implementing

Examples we aren't implementing:

We aren't implementing images (element "img") because we haven't the capabilities or time in this project to convert the bytes in images and raster form to vector images.

We aren't implementing the attribute in-fill





