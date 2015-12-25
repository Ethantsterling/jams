"""
Given a polygon with points on an integer lattice, determine:
	(1) The area,
	(2) The number of lattice points on the boundary,
	(3) The number of lattice points wholely inside the polygon.

We determine area as a sum of ordered areas of triangle slices.
Each triangle's area can be determined straightforwardly by determinant,
since its coordinates are known.

The number of points on a line segment with integer endpoints
is a straightforward consequence of gcd.

Given the area of a polygon with vertices on a 2D integer lattice,
plus the number of boundary points the polygon shares with that lattice,
we can use Pick's Theorem to derive the polygon's number of
internal lattice points.

Pick's Theorem: AREA = (#BOUNDARY) / 2 + #INSIDE + 1

So we write a function 'pick' which takes the vertices of a polygon and,
if those vertices lie on an integer lattice (and there are at least
three vertices), returns the area, the number of boundary lattice points,
and the number of fully internal points.

Note that order matters for the vertices, since a different ordering
of the same vertices could indicate a different polygon.
Also, although the polygon may be concave, it is assumed not to cross itself.

Performs v gcd operations on pairs of vertices, which should be the
limiting factor for speed.  GCD takes a linear number of % steps in the
length of its inputs, so (counting each vertex) we perform a number of 
% operations that is at most linear in the length of the input.

Inspired by a "count the number of lattice points inside" problem.
"""

def gcd(a,b):
    if a: return gcd(b%a, a)
    return b

def boundary(vertices):
    """Given integer coordinates, determines the total number of lattice points
    on the lines traversing the given vertices."""
    count = 0
    for i,v1 in enumerate(vertices):
        v2 = vertices[(i+1) % len(vertices)]
        count += gcd(abs(v2[0]-v1[0]), abs(v2[1] - v1[1]))
    return count

def triangleArea(v1, v2, v3):
    """Area using determinant method."""
    a = v2[0] - v1[0]
    b = v3[0] - v1[0]
    c = v2[1] - v1[1]
    d = v3[1] - v1[1]
    return abs(a*d - b*c) / 2.0

def polygonArea(vertices):
	"""Determines the area of given polygon by summing the ordered area
	of the triangular slices with one vertex serving as the root and
	each other adjacent pair filling out one triangle."""
	if len(vertices) <= 2: return 0
	v1 = vertices[0]
	area = 0
	for i in range(1, len(vertices) - 1):
		v2,v3 = vertices[i],vertices[i+1]
		area += triangleArea(v1,v2,v3)
	return abs(area)

def pick(vertices):
	area = polygonArea(vertices)
	num_boundary = boundary(vertices)
	num_inside = int(area - (num_boundary / 2.0) + 1)
	return (area, num_boundary, num_inside)

def numInside(vertices):
    area = polygonArea(vertices)
    num_boundary = boundary(vertices)
    return int(area - num_boundary / 2.0 + 1)

assert pick([(0,0),(0,1),(1,0)]) == (.5, 3, 0)
assert pick([(0,0),(4,0),(4,3),(0,3)]) == (12, 14, 6)

assert numInside([[2,3], [6,9], [10,160]]) == 289
assert numInside([[91207, 89566], [-88690, -83026], [67100, 47194]]) == 1730960165
