#!python
# draw two cubes with transform and clip
#raster-08.py
from PIL import Image, ImageDraw
from vector3 import Vector3
from collections import namedtuple
from matrix44 import Matrix44
from math import radians, sqrt

Vector2 = namedtuple('Vector2', 'x y')
Triangle = namedtuple('Triangle', 'v0 v1 v2 color')
Model = namedtuple('Model', 'vertexes triangles bounds_center bounds_radius')
Plane = namedtuple('Plane', 'normal distance')
Camera = namedtuple('Camera', 'position orientation clipping_planes')


class Instance:
    def __init__(self, model, position, orientation, scale):
        self.model = model
        self.position = position
        self.orientation = orientation
        self.scale = scale

        self.transform = Matrix44.translation(position.x, position.y, position.z) * Matrix44.scale(scale) * orientation
        self.bounds_radius = model.bounds_radius * scale # the bounds radius should also change
        self.bounds_center = self.transform.transform_vec3(model.bounds_center)

def renderTriangleUsingPoints(p0, p1, p2, color):
    """
    render triangle with three Vector3 point and color.
    p0, p1, p2: Vector3
    color: tuple
    render the triangle accordingly.
    """
    p0, p1, p2 = projectVertexToCanvas(p0),projectVertexToCanvas(p1),projectVertexToCanvas(p2)
    p0, p1, p2 = canvasToScreen(p0), canvasToScreen(p1), canvasToScreen(p2)

    draw = ImageDraw.Draw(image)
    draw.polygon([p0, p1, p2],outline = color)

def clipTriangle(triangle, plane, vertexes):
    """
    clip a triangle against a plane, draw the output triangle.
    """
    # get the projected vertex
    v0, v1, v2 = vertexes[triangle.v0], vertexes[triangle.v1], vertexes[triangle.v2]
    vin, vout = [], []

    if plane.normal.dot(v0) + plane.distance > 0:
        vin.append(v0)
    else:
        vout.append(v0)

    if plane.normal.dot(v1) + plane.distance > 0:
        vin.append(v1)
    else:
        vout.append(v1)

    if plane.normal.dot(v2) + plane.distance > 0:
        vin.append(v2)
    else:
        vout.append(v2)

    if len(vin) == 0:
        # Nothing to do - the triangle is fully clipped out.
        return []
    elif len(vin) == 3:
        # the triangle is fully in front of the plane.
        renderTriangleUsingPoints(v0, v1, v2, triangle.color)
    elif len(vin) == 1:
        # the triangle has one vertex in, return one clipped triangle.
        A = vin[0]
        intersection_point = []
        for v in vout:
            t = ( -plane.distance - plane.normal.dot(A) ) \
                   / ( plane.normal.dot(v - A) )
            intersection_point.append(A + t * (v - A))

        Bprime, Cprime = intersection_point
        renderTriangleUsingPoints(A, Bprime, Cprime, triangle.color)

    elif len(vin) == 2:
        # the triangle has two vertex in, return two clipped triangle.
        A, B = vin
        C = vout[0]
        intersection_point = []
        for v in vin:
            t = ( -plane.distance - plane.normal.dot(v) ) \
                / ( plane.normal.dot(C - v) )
            print(t)
            intersection_point.append(v + t * (C - v))

        Aprime, Bprime = intersection_point
        renderTriangleUsingPoints(A, Aprime, B, triangle.color)
        renderTriangleUsingPoints(Aprime, Bprime, B, triangle.color)



def transformAndClip(clipping_planes, instance, transform):
    """
    Transform the bounding sphere, and attemp early discard.

    clipping_planes: Plane
    instance: Instance
    transform: Matrix44
    """
    center = instance.bounds_center
    radius = instance.bounds_radius
    model = instance.model

    for plane in clipping_planes:
        distance_to_plane = plane.normal.dot(center) + plane.distance
        if distance_to_plane < -model.bounds_radius:
            return

    transformed_vertexes = []
    for vertex in model.vertexes:
        vertexH = transform.transform_vec3(vertex)
        transformed_vertexes.append(vertexH)

    for triangle in model.triangles:
        for plane in clipping_planes:
            clipTriangle(triangle, plane, transformed_vertexes)



def projectVertexToCanvas(v3):
    """
    v3: Vector3
    rtype: Vector2
    """
    return Vector2( (v3.x * projection_plane_z * screen_width) / (v3.z * viewport_size),
             (v3.y * projection_plane_z * screen_height) / (v3.z * viewport_size) )

def canvasToScreen(v2):
    """
    v2: Vector2
    rtype: Vector2 on screen
    """
    return Vector2(screen_width / 2 + int(v2.x), screen_height / 2 - int(v2.y))


def renderScene(camera, instances):
    """
    """
    cameraTranlationMatrixInverse = Matrix44.translation_vec3(camera.position).get_inverse_translation()
    cameraRotationInverse = camera.orientation.get_inverse_rotation()

    cameraMatrix = cameraRotationInverse * cameraTranlationMatrixInverse

    for instance in instances:
        transform = cameraMatrix * instance.transform
        transformAndClip(camera.clipping_planes, instance, transform)

screen_width = 400
screen_height = 400

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



background_color = (255, 255, 255)
image = Image.new("RGB", (screen_width, screen_height), background_color)

cube = Model(vertexes, triangles, Vector3(0, 0, 0), sqrt(3))

sqrt_2 = sqrt(2)
clipping_planes = [
    Plane(Vector3(0, 0, 1), -1), # Near
    Plane(Vector3(sqrt_2, 0, sqrt_2), 0), # Left
    Plane(Vector3(-sqrt_2, 0, sqrt_2), 0), # Right
    Plane(Vector3(0, -sqrt_2, sqrt_2), 0), # Top
    Plane(Vector3(0, sqrt_2, sqrt_2), 0) # Bottom
]


camera = Camera(Vector3(-3, 1, 2), Matrix44().y_rotation(radians(-30)), clipping_planes)


instances = [Instance(cube, Vector3(-1.5, -1, 7), Matrix44(), 0.75),
             Instance(cube, Vector3(1.25, 2.5, 7.5), Matrix44.y_rotation(radians(195)), 1.0)]

renderScene(camera, instances)

image.save("raster08.png")
