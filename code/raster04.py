#-*- coding: utf-8 -*-
#!python

#raster-01.py
from PIL import Image, ImageDraw
import math


viewport_size = 1.0
projection_plane_z = 1.0


class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Vertex(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

		


def drawLine(p0, p1, color):
	print p0.x, p0.y, p1.x ,p1.y

	x0 = screen_width / 2 + p0.x 
	y0 = screen_height / 2 - p0.y

	x1 = screen_width / 2 + p1.x
	y1 = screen_height / 2 - p1.y

	draw = ImageDraw.Draw(image)
	draw.line((x0, y0, x1, y1), fill = color)

def viewportToCanvas(p2d):
	return Point(p2d.x * screen_width / viewport_size,
		p2d.y * screen_height / viewport_size)

def projectVertex(v):
	return viewportToCanvas(Point(v.x * projection_plane_z / v.z,
		v.y * projection_plane_z / v.z))


screen_width = 600
screen_height = 600


vA = Vertex(-2, -0.5, 5)
vB = Vertex(-2, 0.5, 5)
vC = Vertex(-1, 0.5, 5)
vD = Vertex(-1, -0.5, 5)

vAb = Vertex(-2, -0.5, 6)
vBb = Vertex(-2, 0.5, 6)
vCb = Vertex(-1, 0.5, 6)
vDb = Vertex(-1, -0.5, 6)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

background_color = (255, 255, 255, 255)


image = Image.new("RGBA", (screen_width, screen_height), background_color)

drawLine(projectVertex(vA),projectVertex(vB), BLUE)
drawLine(projectVertex(vB),projectVertex(vC), BLUE)
drawLine(projectVertex(vC),projectVertex(vD), BLUE)
drawLine(projectVertex(vD),projectVertex(vA), BLUE)

drawLine(projectVertex(vAb),projectVertex(vBb), RED)
drawLine(projectVertex(vBb),projectVertex(vCb), RED)
drawLine(projectVertex(vCb),projectVertex(vDb), RED)
drawLine(projectVertex(vDb),projectVertex(vAb), RED)

drawLine(projectVertex(vA),projectVertex(vAb), GREEN)
drawLine(projectVertex(vB),projectVertex(vBb), GREEN)
drawLine(projectVertex(vC),projectVertex(vCb), GREEN)
drawLine(projectVertex(vD),projectVertex(vDb), GREEN)

image.save("raster04.png")