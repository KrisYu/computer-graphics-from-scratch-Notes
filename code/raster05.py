#-*- coding: utf-8 -*-
#!python

#raster-01.py
from PIL import Image, ImageDraw
import math

from gameobjects.vector3 import Vector3
from gameobjects.vector2 import Vector2

class Triangle(object):
	"""docstring for Triangle"""
	def __init__(self, v0, v1, v2, color):
		self.v0 = v0
		self.v1 = v1
		self.v2 = v2
		self.color = color


def renderTriangle(triangle, projected):
	p0, p1, p2, color = projected[triangle.v0], projected[triangle.v1], projected[triangle.v2], triangle.color
	p0, p1, p2 = canvasToScreen(p0), canvasToScreen(p1), canvasToScreen(p2)

	x0, y0 = p0.x, p0.y
	x1, y1 = p1.x, p1.y
	x2, y2 = p2.x, p2.y

	draw = ImageDraw.Draw(image)
	draw.line((x0, y0, x1, y1),fill = color)
	draw.line((x1, y1, x2, y2),fill = color)
	draw.line((x2, y2, x0, y0),fill = color)


def renderObject(vertexes, triangles):
	"""
	vertexes: vector3
	triangles: 
	"""
	projected = []
	for vertex in vertexes:
		projected.append(projectVertex(vertex))

	for triangle in triangles:
		renderTriangle(triangle, projected)

def viewportToCanvas(p2d):
	"""
	p2d: vector2
	rtype: vector2
	"""
	return Vector2(p2d.x * screen_width / viewport_size,
		p2d.y * screen_height / viewport_size)

def projectVertex(v3):
	"""
	v3: vector
	rtype: vector2
	"""
	return viewportToCanvas(Vector2(v3.x * projection_plane_z / v3.z,
		v3.y * projection_plane_z / v3.z))

def canvasToScreen(v2):
	"""
	v2: vector2
	rtype: vector2 on screen
	"""
	return Vector2(screen_width / 2 + v2.x, screen_height / 2 - v2.y)



screen_width = 600
screen_height = 600

viewport_size = 1.0
projection_plane_z = 1.0


vertexes = [
  Vector3(1, 1, 1),
  Vector3(-1, 1, 1),
  Vector3(-1, -1, 1),
  Vector3(1, -1, 1),
  Vector3(1, 1, -1),
  Vector3(-1, 1, -1),
  Vector3(-1, -1, -1),
  Vector3(1, -1, -1)
]


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

triangles = [
  Triangle(0, 1, 2, RED),
  Triangle(0, 2, 3, RED),
  Triangle(4, 0, 3, GREEN),
  Triangle(4, 3, 7, GREEN),
  Triangle(5, 4, 7, BLUE),
  Triangle(5, 7, 6, BLUE),
  Triangle(1, 5, 6, YELLOW),
  Triangle(1, 6, 2, YELLOW),
  Triangle(4, 5, 1, PURPLE),
  Triangle(4, 1, 0, PURPLE),
  Triangle(2, 6, 7, CYAN),
  Triangle(2, 7, 3, CYAN),
]



background_color = (255, 255, 255, 255)
image = Image.new("RGBA", (screen_width, screen_height), background_color)

for vertex in vertexes:
	vertex.x -= 1.5
	vertex.z += 7

renderObject(vertexes, triangles)

image.save("raster05.png")