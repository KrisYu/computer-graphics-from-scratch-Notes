#!python
# draw cube 
#raster-04.py 
from PIL import Image, ImageDraw
from vector3 import Vector3
from collections import namedtuple

Vector2 = namedtuple('Vector2', ['x', 'y'])

def drawLine(p0, p1, color):
    """
    draw line using PIL library
    """
    p0 = canvasToScreen(p0)
    p1 = canvasToScreen(p1)

    draw = ImageDraw.Draw(image)
    draw.line((p0, p1), fill = color)


def viewportToCanvas(p2d):
    """
    p2d: Vector2
    rtype: Vector2
    """
    return Vector2(p2d.x * screen_width / viewport_size,
        p2d.y * screen_height / viewport_size)


def projectVertex(v3):
    """
    v3: Vector3
    rtype: Vector2
    """
    return viewportToCanvas(Vector2(v3.x * projection_plane_z / v3.z,
        v3.y * projection_plane_z / v3.z))

def canvasToScreen(v2):
    """
    v2: Vector2
    rtype: Vector2 on screen
    """
    return Vector2(screen_width / 2 + v2.x, screen_height / 2 - v2.y)


screen_width = 600
screen_height = 600


viewport_size = 1.0
projection_plane_z = 1.0

vA = Vector3(-2, -0.5, 5)
vB = Vector3(-2, 0.5, 5)
vC = Vector3(-1, 0.5, 5)
vD = Vector3(-1, -0.5, 5)

vAb = Vector3(-2, -0.5, 6)
vBb = Vector3(-2, 0.5, 6)
vCb = Vector3(-1, 0.5, 6)
vDb = Vector3(-1, -0.5, 6)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

background_color = (255, 255, 255)


image = Image.new("RGB", (screen_width, screen_height), background_color)

drawLine(projectVertex(vA),projectVertex(vB), BLUE);
drawLine(projectVertex(vB),projectVertex(vC), BLUE);
drawLine(projectVertex(vC),projectVertex(vD), BLUE);
drawLine(projectVertex(vD),projectVertex(vA), BLUE);

drawLine(projectVertex(vAb),projectVertex(vBb), RED);
drawLine(projectVertex(vBb),projectVertex(vCb), RED);
drawLine(projectVertex(vCb),projectVertex(vDb), RED);
drawLine(projectVertex(vDb),projectVertex(vAb), RED);

drawLine(projectVertex(vA),projectVertex(vAb), GREEN);
drawLine(projectVertex(vB),projectVertex(vBb), GREEN);
drawLine(projectVertex(vC),projectVertex(vCb), GREEN);
drawLine(projectVertex(vD),projectVertex(vDb), GREEN);

image.save("raster04.png")
