#!python
# draw line
#raster-01.py
from PIL import Image
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


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
    """
    dependent value change according to indepent value

    d: dependent value
    i: indepent value
    rtype : a list of dependent values change accoding to indepent value
    """
    if i0 == i1:
        return [d0]
    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0,i1):
        values.append(d)
        d = d + a
    return values

def drawLine(p0, p1, color):
    """
    draw line according to it is more vertical or more horizontal
    """
    dx = p1.x - p0.x
    dy = p1.y - p0.y

    if abs(dx) > abs(dy):
        if dx < 0:
            p0,p1 = p1,p0

        ys = interpolate(p0.x, p0.y, p1.x, p1.y)
        for x in range(p0.x,p1.x):
            putPixel(pixels, x, ys[(x - p0.x)], color)
    else:
        if dy < 0:
            p0,p1 = p1,p0

        xs = interpolate(p0.y, p0.x, p1.y, p1.x)
        for y in range(p0.y,p1.y):
            putPixel(pixels, xs[(y - p0.y)], y, color)

screen_width = 600
screen_height = 600
background_color = (255, 255, 255)

image = Image.new("RGB", (screen_width, screen_height), background_color)
pixels = image.load()

drawLine(Point(-200, -100), Point(240,120), (0,0,0))
drawLine(Point(-50, -200), Point(60, 240), (0,0,0))
image.save("raster01.png")
