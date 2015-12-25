"""
Vertices on integer coordinates?  Count the number of lattice points inside?
Sounds like Pick's theorem.
We get area in terms of number of points on the boundary and number of points inside.
We find area via determinant.
We find number of points on the boundary by examining each segment.

NOTE: Pick's theorem and boundary-determination extend easily enough
to n-gons.  Area of an n-gon can be determine by apply the same
determinant method to a series of triangular cuts from the same root vertex.
So we do not actually the the plot of land to be triangular.
Any contiguous polygon should do.
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

def answer(vertices):
    area = polygonArea(vertices)
    num_boundary = boundary(vertices)
    num_inside = area - num_boundary / 2.0 + 1
    return int(num_inside)

assert pick([(0,0),(0,1),(1,0)]) == (.5, 3, 0)

assert answer([[2,3], [6,9], [10,160]]) == 289
assert answer([[91207, 89566], [-88690, -83026], [67100, 47194]]) == 1730960165
