#!python
# draw gradient triangle
#raster-03.py
from PIL import Image
from collections import namedtuple
from vector3 import Vector3

Point = namedtuple('Point', ['x', 'y', 'h'])

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
    for i in range(i0,i1+1):
        values.append(d)
        d = d + a
    return values


def drawShadedTriangle(p0, p1, p2, color):
    """
    draw shaded triangle using lerp
    """
    if p1.y < p0.y: p0, p1 = p1, p0
    if p2.y < p0.y: p0, p2 = p2, p0
    if p2.y < p1.y: p1, p2 = p2, p1

    x0,y0,h0 = p0.x,p0.y,p0.h
    x1,y1,h1 = p1.x,p1.y,p1.h
    x2,y2,h2 = p2.x,p2.y,p2.h

    x01 = interpolate(y0, x0, y1, x1)
    h01 = interpolate(y0, h0, y1, h1)

    x12 = interpolate(y1, x1, y2, x2)
    h12 = interpolate(y1, h1, y2, h2)

    x02 = interpolate(y0, x0, y2, x2)
    h02 = interpolate(y0, h0, y2, h2)

    del x01[-1]
    x012 = x01 + x12

    del h01[-1]
    h012 = h01 + h12

    m = len(x02) // 2
    if x02[m] < x012[m]:
        x_left = x02
        x_right = x012

        h_left = h02
        h_right = h012
    else:
        x_left = x012
        x_right = x02

        h_left = h012
        h_right = h02

    # int to use for in range
    x_left = [int(x) for x in x_left]
    x_right = [int(x) for x in x_right]

    #
    for y in range(y0, y2):
        x_l = x_left[y - y0]
        x_r = x_right[y - y0]

        h_segment = interpolate(x_l, h_left[y-y0], x_r, h_right[y-y0])
        for x in range(x_l, x_r):
            shaded_color = (h_segment[x - x_l] * color)
            (r, g, b) = (int(shaded_color.r), int(shaded_color.g), int(shaded_color.b))
            putPixel(pixels, x, y, (r, g, b))


screen_width = 600
screen_height = 600
background_color = (255, 255, 255)

p0 = Point(-200, -250, 0.3)
p1 = Point(200, 50, 0.1)
p2 = Point(20, 250, 1.0)

image = Image.new("RGB", (screen_width, screen_height), background_color)
pixels = image.load()

drawShadedTriangle(p0, p1, p2, Vector3(0,255,0))
image.save("raster03.png")
