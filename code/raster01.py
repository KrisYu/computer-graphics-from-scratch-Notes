#-*- coding: utf-8 -*-
#!python

#raster-01.py
from PIL import Image
import math

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


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

def interpolate(i0, d0, i1, d1):
	if i0 == i1:
		return [d0]
	values = []
	a = (d1 - d0) * 1.0 / (i1 - i0)
	d = d0
	for i in xrange(i0,i1):
		values.append(d)
		d = d + a
	return values

def drawLine(p0, p1, color):
	dx = p1.x - p0.x
	dy = p1.y - p0.y

	if abs(dx) > abs(dy):
		if dx < 0:
			p0,p1 = p1,p0

		ys = interpolate(p0.x, p0.y, p1.x, p1.y)
		for x in xrange(p0.x,p1.x):
			putPixel(pixels, x, ys[(x - p0.x) | 0], color)
	else:
		if dy < 0:
			p0,p1 = p1,p0

		xs = interpolate(p0.y, p0.x, p1.y, p1.x)
		for y in xrange(p0.y,p1.y):
			putPixel(pixels, xs[(y - p0.y) | 0], y, color)

screen_width = 600
screen_height = 600
background_color = (255, 255, 255)

image = Image.new("RGBA", (screen_width, screen_height), background_color)
pixels = image.load()

drawLine(Point(-200, -100), Point(240,120), (0,0,0))
drawLine(Point(-50, -200), Point(60, 240), (0,0,0))
image.save("raster01.png")
