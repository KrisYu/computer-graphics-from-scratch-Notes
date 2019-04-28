#!python
# draw two cubes with transform
#raster-09.py 
from PIL import Image, ImageDraw
from vector3 import Vector3
from collections import namedtuple
from matrix44 import Matrix44
from math import radians

Vector2 = namedtuple('Vector2', 'x y')
Triangle = namedtuple('Triangle', 'v0 v1 v2 color')
Model = namedtuple('Model', 'vertexes triangles')
Camera = namedtuple('Camera', 'position orientation')

class Instance:
    def __init__(self, model, position, orientation, scale):
        self.model = model
        self.position = position
        self.orientation = orientation
        self.scale = scale      
        
        self.transform = Matrix44.translation_vec3(position) * Matrix44.scale(scale) * orientation
        
def renderTriangle(triangle, projected):
    p0, p1, p2, color = projected[triangle.v0], projected[triangle.v1], projected[triangle.v2], triangle.color
    p0, p1, p2 = canvasToScreen(p0), canvasToScreen(p1), canvasToScreen(p2)

    draw = ImageDraw.Draw(image)
    draw.polygon([p0, p1, p2],outline = color)


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
    return Vector2(screen_width / 2 + v2.x, screen_height / 2 - v2.y)


def renderModel(model, transform):
    projected = []

    for vertex in model.vertexes:
        vertexH = transform.transform_vec3(vertex)
        projected.append(projectVertexToCanvas(vertexH))

    for triangle in model.triangles:
        renderTriangle(triangle, projected)


def renderScene(camera, instances):
    """
    """
    cameraTranlationMatrixInverse = Matrix44.translation_vec3(camera.position).get_inverse_translation()
    cameraRotationInverse = camera.orientation.get_inverse_rotation()

    cameraMatrix = cameraRotationInverse * cameraTranlationMatrixInverse

    for instance in instances:
        transform = cameraMatrix * instance.transform
        renderModel(instance.model, transform)

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



background_color = (255, 255, 255)
image = Image.new("RGB", (screen_width, screen_height), background_color)

cube = Model(vertexes, triangles)

camera = Camera(Vector3(-3, 1, 2), Matrix44.y_rotation(radians(-30)))

instances = [Instance(cube, Vector3(-1.5, 0, 7), Matrix44(), 0.75),
            Instance(cube, Vector3(1.25, 2.5, 7.5), Matrix44.y_rotation(radians(195)), 1.0)]

renderScene(camera, instances)

image.save("raster09.png")


