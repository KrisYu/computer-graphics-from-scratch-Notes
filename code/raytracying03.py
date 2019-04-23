#!python
# Ray Tracying with diffuse and specular
from PIL import Image
from math import sqrt, inf
from vector3 import Vector3
from collections import namedtuple

def putPixel(pixels, x, y, color):
	"""
	The PutPixel() function.
	"""
	# canvas coordinate to screen coordinate
	x = screen_width // 2 + x
	y = screen_height // 2  - y 

	if x < 0 or x >= screen_height or y < 0 or y >= screen_height:
		return

	pixels[x, y] = color


# ======================================================================
#  A very basic raytracer.
# ======================================================================

Sphere = namedtuple('Sphere', ['center', 'radius', 'color', 'specular'])

class Light(object):
	"""
	Light class
	:type ltype: string
	:type intensity: float
	:type position: vector
	"""
	def __init__(self, ltype, intensity, position = None):
		self.ltype = ltype
		self.intensity = intensity
		self.position = position

def canvasToViewPort(p2d):
	"""
	Converts 2D canvas coordinates to 3D viewport coordinates.
	:type p2d: tuple
    :rtype: Vector3
	"""

	return Vector3(p2d[0] * viewport_size / screen_width,
		p2d[1] * viewport_size / screen_height,
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
	oc = origin - sphere.center
	k1 = direction.dot(direction)
	k2 = 2 * oc.dot(direction)
	k3 = oc.dot(oc) - sphere.radius * sphere.radius

	discriminant = k2 * k2 - 4 * k1 * k3
	if discriminant < 0:
		return [inf, inf]

	t1 = (-k2 + sqrt(discriminant)) / (2*k1)
	t2 = (-k2 - sqrt(discriminant)) / (2*k1)
	return [t1, t2]

def ComputeLighting(point, normal, view, specular):
	"""
	:type point: Vector3, location
	:type normal: Vector3, vector
	"""
	intensity = 0

	for light in lights:
		if light.ltype == 'AMBIENT':
			intensity += light.intensity
		else:
			vec_l = Vector3(0 , 0, 0)
			if light.ltype == 'POINT':
				vec_l = light.position - point 
			else:
				vec_l = -light.position # direction

			n_dot_l = normal.dot(vec_l)
			if n_dot_l > 0:
				intensity += light.intensity * n_dot_l / (normal.length * vec_l.length)

			if specular != -1:
				vec_r = 2 * normal * normal.dot(vec_l)
				r_dot_v = view.dot(vec_r)
				if r_dot_v > 0:
					intensity += light.intensity * pow((r_dot_v / (view.length * vec_r.length)), specular)

	return intensity

def traceRay(origin, direction, min_t, max_t):
	"""
	Traces a ray against the set of spheres in the scene.
	:type origin: Vector3
	:type direction: Vector3
	:type min_t: float
	:type max_t: float
	:rtype: color
	"""
	closest_t = inf
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

	point = origin + closest_t * direction
	normal = (point - closest_sphere.center).normalize()

	color = closest_sphere.color * ComputeLighting(point, normal, -direction, sphere.specular)
	return (int(color.r), int(color.g), int(color.b))

viewport_size = 1
projection_plane_z = 1
camera_position = Vector3(0, 0, 0)
background_color = (255, 255, 255)
spheres = [Sphere(Vector3(0.0, -1.0, 3.0), 1.0, Vector3(255, 0, 0), 500),
           Sphere(Vector3(2.0, 0.0, 4.0), 1.0, Vector3(0, 0, 255), 500),
           Sphere(Vector3(-2.0, 0.0, 4.0), 1.0, Vector3(0, 255, 0), 10),
           Sphere(Vector3(0.0, -5001.0, 0.0), 5000.0, Vector3(255, 255, 0), 1000)]

screen_width = 600
screen_height = 600


lights = [
  Light('AMBIENT', 0.2),
  Light('POINT', 0.6, Vector3(2, 1, 0)),
  Light('DIRECTIONAL', 0.2, Vector3(1, 4, 4))
]


def run():
	image = Image.new("RGB", (screen_width, screen_height), background_color)
	pixels = image.load()

	for x in range(-screen_width//2, screen_width//2):
		for y in range(-screen_height//2,screen_height//2):
			direction = canvasToViewPort((x, y))
			color = traceRay(camera_position, direction, 1, inf)
			putPixel(pixels, x, y ,color)

	image.save("raytracying03.png")

#
# Main loop.
#
if __name__ == '__main__':
	run()
