#-*- coding: utf-8 -*-
#!python
# Ray Tracying without lighting
from PIL import Image
import math
from gameobjects.vector3 import Vector3
from gameobjects.vector2 import Vector2

def putPixel(pixels, x, y, color):
	"""
	The PutPixel() function.
	"""
	# canvas coordinate to screen coordinate
	x = screen_width / 2 + x
	y = screen_height / 2  - y 

	if x < 0 or x >= screen_height or y < 0 or y >= screen_height:
		return

	pixels[x, y] = color


# ======================================================================
#  A very basic raytracer.
# ======================================================================

class Sphere(object):
	"""
	Sphere class
	:type center: Vector3
	:type radius: float
	:type color: typle as color
	"""
	def __init__(self, center, radius, color):
		self.center = center
		self.radius = radius
		self.color = color

def canvasToViewPort(p2d):
	"""
	Converts 2D canvas coordinates to 3D viewport coordinates.
	:type p2d: Vector2
    :rtype: Vector3
	"""

	return Vector3(p2d.x * viewport_size / screen_width,
		p2d.y * viewport_size / screen_height,
		projection_plane_z)


def intersectRaySphere(origin, direction, sphere):
	"""
	Computes the intersection of a ray and a sphere. Returns the values
	of t for the intersections.
	:type origin: Vector3
	:type direction: Vector3
	:type sphere: Sphere
	:rtype: [List[int]]
	"""
	oc = sphere.center - origin
	k1 = direction.dot(direction)
	k2 = - 2 * oc.dot(direction)
	k3 = oc.dot(oc) - sphere.radius * sphere.radius

	discriminant = k2 * k2 - 4 * k1 * k3
	if discriminant < 0:
		return [float('inf'), float('inf')]

	t1 = (-k2 + math.sqrt(discriminant)) / (2*k1)
	t2 = (-k2 - math.sqrt(discriminant)) / (2*k1)
	return [t1, t2]


def traceRay(origin, direction, min_t, max_t):
	"""
	Traces a ray against the set of spheres in the scene.
	:type origin: Vector3
	:type direction: Vector3
	:type min_t: float
	:type max_t: float
	:rtype: color
	"""
	closest_t = float('inf')
	closest_sphere = None

	for sphere in spheres:
		t1, t2 = intersectRaySphere(origin, direction, sphere)
		if t1 < closest_t and min_t < t1 and t1 < max_t:
			closest_t = t1
			closest_sphere = sphere
		if t2 < closest_t and min_t < t2 and t2 < max_t:
			closest_t = t2
			closest_sphere = sphere

	if closest_sphere == None:
		return background_color

	return closest_sphere.color


viewport_size = 1
projection_plane_z = 1
camera_position = Vector3(0, 0, 0)
background_color = (255, 255, 255)
spheres = [Sphere(Vector3(0.0, -1.0, 3.0), 1.0, (255, 0, 0)),
           Sphere(Vector3(2.0, 0.0, 4.0), 1.0, (0, 0, 255)),
           Sphere(Vector3(-2.0, 0.0, 4.0), 1.0, (0, 255, 0))]


screen_width = 600
screen_height = 600




def run():
	image = Image.new("RGBA", (screen_width, screen_height), background_color)
	pixels = image.load()

	for x in xrange(-screen_width/2, screen_width/2):
		for y in xrange(-screen_height/2,screen_height/2):
			direction = canvasToViewPort(Vector2(x, y))
			color = traceRay(camera_position, direction, 1, float('inf'))
			putPixel(pixels , x, y ,color)

	image.save("raytracying01.png")

#
# Main loop.
#
if __name__ == '__main__':
	run()
