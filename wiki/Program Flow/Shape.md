Shape is a classes file holding most of the types of elements in an [[SVG File]].
Each shape has three main functions:
- Add
- Check Shape
- Get Points
For a list of shapes, see this [[SVG Documentation#Basic shapes (elements) of SVG we are implementing|shape list we are implementing]].

# Add
Adds an attribute to the shape objects
Returns status on successfulness of adding an attribute:
- Success: attribute added successfully
- Warning: attribute added but not implemented
- Not Found: attribute not found
- Error: attribute is invalid (e.g., is not a integer when supposed to be)

# Check Shape
Check that a shape has all necessary points to be plotted
Returns True if shape has valid attributes

# Get Points
Gets a list of points bassed on attributes