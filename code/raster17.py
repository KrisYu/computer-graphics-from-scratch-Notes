#!python
# texture
#raster-17.py
from PIL import Image, ImageDraw
from vector3 import Vector3
from collections import namedtuple
from matrix44 import Matrix44
from math import radians, sqrt, inf, cos, sin
from cmath import pi

Vector2 = namedtuple('Vector2', 'x y')
Triangle = namedtuple('Triangle', 'v0 v1 v2 color normal0 normal1 normal2 texture uv0 uv1 uv2')
Model = namedtuple('Model', 'vertexes triangles bounds_center bounds_radius')
Plane = namedtuple('Plane', 'normal distance')
Depth = namedtuple('Depth', 'x y buffer')
Light = namedtuple('Light', 'ltype intensity position')

class Instance:
    def __init__(self, model, position, orientation, scale):
        self.model = model
        self.position = position
        self.orientation = orientation
        self.scale = scale

        self.transform = Matrix44.translation(position.x, position.y, position.z) * Matrix44.scale(scale) * orientation
        self.bounds_radius = model.bounds_radius * scale # the bounds radius should also change
        self.bounds_center = self.transform.transform_vec3(model.bounds_center)

class Camera:
    def __init__(self, position, orientation, clipping_planes):
        self.position = position
        self.orientation = orientation
        self.clipping_planes = clipping_planes

        cameraTranlationMatrixInverse = Matrix44.translation_vec3(position).get_inverse_translation()
        cameraRotationInverse = orientation.get_inverse_rotation()
        self.matrix = cameraRotationInverse * cameraTranlationMatrixInverse

def putPixel(pixels, x, y, z, color):
    """
    The PutPixel() function.
    """
    # canvas coordinate to screen coordinate
    x = screen_width // 2 + x
    y = screen_height // 2  - y

    if x < 0 or x >= screen_height or y < 0 or y >= screen_height:
        return

    r, g, b = int(color.r), int(color.g), int(color.b)
    if z > depth_buffer[x][y]:
        pixels[x, y] = (r, g, b)
        depth_buffer[x][y] = z

def projectVertexToCanvas(v3):
    """
    v3: Vector3
    rtype: Vector2
    """
    return Vector2( int((v3.x * projection_plane_z * screen_width) / (v3.z * viewport_size)),
                  int((v3.y * projection_plane_z * screen_height) / (v3.z * viewport_size)) )

def canvasToViewPort(p2d):
    """
    p2d: Vector2
    rtype: Vector2
    """
    return Vector2(p2d.x * viewport_size / screen_width,
        p2d.y * viewport_size / screen_height)

def unprojectVertex(x, y, inv_z):
    """
    Unproject a point from canvas to 3d space
    """
    oz = 1 / inv_z
    ux = x * oz / projection_plane_z
    uy = y * oz / projection_plane_z
    p2d = canvasToViewPort(Vector2(ux, uy))
    return Vector3(p2d.x, p2d.y, oz)

def canvasToScreen(v2):
    """
    v2: Vector2
    rtype: Vector2 on screen
    """
    return Vector2(screen_width // 2 + int(v2.x), screen_height // 2 - int(v2.y))

def getTexturePixel(u, v):

    iu = (texture_width - 1) * u
    iv = (texture_height - 1) * v

    return texture_pixels[iu, iv]


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

def edgeInterpolate(y0, v0, y1, v1, y2, v2):
    v01 = interpolate(y0, v0, y1, v1)
    v12 = interpolate(y1, v1, y2, v2)
    v02 = interpolate(y0, v0, y2, v2)
    del v01[-1]
    v012 = v01 + v12
    return (v02, v012)

def computeIllumination(point, normal, camera, lights):
    """
    """
    illumination  = 0

    for light in lights:
        if light.ltype == 'AMBIENT':
            illumination += light.intensity
        else:
            vec_l = Vector3(0, 0, 0)
            if light.ltype == 'POINT':
                transformed_point_light = camera.matrix.transform_vec3(light.position)
                vec_l = transformed_point_light - point
            if light.ltype == 'DIRECTIONAL':
            # only direction will effect directional light
                transformed_directional_light = camera.matrix.transform_vec3(-light.position)
                vec_l = transformed_directional_light

            # diffuse
            # print(normal, vec_l)
            cos_alpha = vec_l.dot(normal) / (normal.length * vec_l.length)
            if cos_alpha > 0:
                illumination += cos_alpha * light.intensity

            # specular
            reflected = 2 * normal * normal.dot(vec_l) - vec_l
            view = -camera.position
            cos_beta = reflected.dot(view) / (reflected.length * view.length)
            if cos_beta > 0:
                specular = 500
                illumination += pow(cos_beta, specular) * light.intensity

    return illumination

def renderTriangleUsingPoints(v0, v1, v2, normal0 , normal1, normal2, color, transform, uv0, uv1, uv2):
    """
    """
    v01 = v1 - v0
    v02 = v2 - v0

    # we're using left-handed coordinate system.
    triangle_normal = v01.cross(v02)
    triangle_center = (v0 + v1 + v2) / 3

    # backface culling
    if triangle_center.dot(-triangle_normal) < 0:
        return

    p0, p1, p2 = projectVertexToCanvas(v0) ,projectVertexToCanvas(v1), projectVertexToCanvas(v2)


    if p1.y < p0.y:
        p0, p1 = p1, p0
        v0, v1 = v1, v0
        normal0, normal1 = normal1, normal0
        uv0, uv1 = uv1, uv0
    if p2.y < p0.y:
        p0, p2 = p2, p0
        v0, v2 = v2, v0
        normal0, normal2 = normal2, normal0
        uv0, uv2 = uv2, uv0
    if p2.y < p1.y:
        p1, p2 = p2, p1
        v1, v2 = v2, v1
        normal1, normal2 = normal2, normal1
        uv1, uv2 = uv2, uv1

    x0,y0,iz0 = p0.x,p0.y,1/v0.z
    x1,y1,iz1 = p1.x,p1.y,1/v1.z
    x2,y2,iz2 = p2.x,p2.y,1/v2.z

    x02, x012 = edgeInterpolate(y0, x0, y1, x1, y2, x2)
    iz02, iz012 = edgeInterpolate(y0, iz0, y1, iz1, y2, iz2)

    uz02, uz012 = edgeInterpolate(y0, uv0.x, y1, uv1.x, y2, uv2.x)
    vz02, vz012 = edgeInterpolate(y0, uv0.y, y1, uv1.y, y2, uv2.y)


    # normal also changed in the coordinate
    normal0 = transform.transform_vector(normal0)
    normal1 = transform.transform_vector(normal1)
    normal2 = transform.transform_vector(normal2)

    # Phong shading:interpolate normal vectors
    nx02, nx012 = edgeInterpolate(y0, normal0.x, y1, normal1.x, y2, normal2.x)
    ny02, ny012 = edgeInterpolate(y0, normal0.y, y1, normal1.y, y2, normal2.y)
    nz02, nz012 = edgeInterpolate(y0, normal0.z, y1, normal1.z, y2, normal2.z)

    m = len(x02) // 2
    if x02[m] < x012[m]:
        x_left, x_right = x02, x012
        iz_left, iz_right = iz02, iz012

        nx_left, nx_right = nx02, nx012
        ny_left, ny_right = ny02, ny012
        nz_left, nz_right = nz02, nz012

        uz_left, uz_right = uz02, uz012
        vz_left, vz_right = vz02, vz012
    else:
        x_left, x_right = x012, x02
        iz_left, iz_right = iz012, iz02

        nx_left, nx_right = nx012, nx02
        ny_left, ny_right = ny012, ny02
        nz_left, nz_right = nz012, nz02

        uz_left, uz_right = uz012, uz02
        vz_left, vz_right = vz012, vz02


    x_left = [int(x) for x in x_left]
    x_right = [int(x) for x in x_right]

    for y in range(y0, y2):
        xl, xr = x_left[y - y0], x_right[y - y0]

        zl, zr = iz_left[y - y0], iz_right[y - y0]
        zscan = interpolate(xl, zl, xr, zr)

        nxl, nxr = nx_left[y - y0], nx_right[y - y0]
        nyl, nyr = ny_left[y - y0], ny_right[y - y0]
        nzl, nzr = nz_left[y - y0], nz_right[y - y0]

        nxscan = interpolate(xl, nxl, xr, nxr)
        nyscan = interpolate(xl, nyl, xr, nyr)
        nzscan = interpolate(xl, nzl, xr, nzr)

        uzscan = interpolate(xl, uz_left[y-y0], xr, uz_right[y-y0])
        vzscan = interpolate(xl, vz_left[y-y0], xr, vz_right[y-y0])


        for x in range(xl, xr):
            inv_z = zscan[x - xl]
            vertex = unprojectVertex(x, y, inv_z)
            normal = Vector3(nxscan[x - xl], nyscan[x - xl], nzscan[x - xl])
            intensity = computeIllumination(vertex, normal, camera, lights)

            u = uzscan[x - xl]
            v = vzscan[x - xl]

            color = getTexturePixel(u, v)
            # print(color)
            putPixel(pixels, x, y, zscan[x - xl], Vector3(color) * intensity)

def clipTriangle(triangle, plane, vertexes, transform):
    """
    clip a triangle against a plane, draw the output triangle.
    """
    # get the projected vertex
    v0, v1, v2 = vertexes[triangle.v0], vertexes[triangle.v1], vertexes[triangle.v2]
    uv0, uv1, uv2 = triangle.uv0, triangle.uv1, triangle.uv2
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
        renderTriangleUsingPoints(v0, v1, v2, triangle.normal0, triangle.normal1, triangle.normal2,triangle.color, transform, uv0, uv1, uv2)
    elif len(vin) == 1:
        # the triangle has one vertex in, return one clipped triangle.
        pass
    elif len(vin) == 2:
        # the triangle has two vertex in, return two clipped triangle.
        pass

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
            clipTriangle(triangle, plane, transformed_vertexes, transform)

def renderScene(camera, instances):
    """
    """
    for instance in instances:
        transform = camera.matrix * instance.transform
        transformAndClip(camera.clipping_planes, instance, transform)

#------- scene setup

screen_width = 600
screen_height = 600

viewport_size = 1.0
projection_plane_z = 1.0

background_color = (255, 255, 255)
image = Image.new("RGB", (screen_width, screen_height), background_color)
pixels = image.load()

texture_image = Image.open('crate-texture.jpg')
texture_width, texture_height = texture_image.size
texture_pixels = texture_image.load()


#------- cube model
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

# for calculation
RED = Vector3(255, 0, 0)
GREEN = Vector3(0, 255, 0)
BLUE = Vector3(0, 0, 255)
YELLOW = Vector3(255, 255, 0)
PURPLE = Vector3(255, 0, 255)
CYAN = Vector3(0, 255, 255)

triangles = [
    Triangle(0, 1, 2, RED,    Vector3( 0,  0,  1), Vector3( 0,  0,  1), Vector3( 0,  0,  1), texture_image, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)),
    Triangle(0, 2, 3, RED,    Vector3( 0,  0,  1), Vector3( 0,  0,  1), Vector3( 0,  0,  1), texture_image, Vector2(0, 0), Vector2(1, 1), Vector2(0, 1)),
    Triangle(4, 0, 3, GREEN,  Vector3( 1,  0,  0), Vector3( 1,  0,  0), Vector3( 1,  0,  0), texture_image, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)),
    Triangle(4, 3, 7, GREEN,  Vector3( 1,  0,  0), Vector3( 1,  0,  0), Vector3( 1,  0,  0), texture_image, Vector2(0, 0), Vector2(1, 1), Vector2(0, 1)),
    Triangle(5, 4, 7, BLUE,   Vector3( 0,  0, -1), Vector3( 0,  0, -1), Vector3( 0,  0, -1), texture_image, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)),
    Triangle(5, 7, 6, BLUE,   Vector3( 0,  0, -1), Vector3( 0,  0, -1), Vector3( 0,  0, -1), texture_image, Vector2(0, 0), Vector2(1, 1), Vector2(0, 1)),
    Triangle(1, 5, 6, YELLOW, Vector3(-1,  0,  0), Vector3(-1,  0,  0), Vector3(-1,  0,  0), texture_image, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)),
    Triangle(1, 6, 2, YELLOW, Vector3(-1,  0,  0), Vector3(-1,  0,  0), Vector3(-1,  0,  0), texture_image, Vector2(0, 0), Vector2(1, 1), Vector2(0, 1)),
    Triangle(1, 0, 5, PURPLE, Vector3( 0,  1,  0), Vector3( 0,  1,  0), Vector3( 0,  1,  0), texture_image, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)),
    Triangle(5, 0, 4, PURPLE, Vector3( 0,  1,  0), Vector3( 0,  1,  0), Vector3( 0,  1,  0), texture_image, Vector2(0, 1), Vector2(1, 1), Vector2(0, 0)),
    Triangle(2, 6, 7, CYAN,   Vector3( 0, -1,  0), Vector3( 0, -1,  0), Vector3( 0, -1,  0), texture_image, Vector2(0, 0), Vector2(1, 0), Vector2(1, 1)),
    Triangle(2, 7, 3, CYAN,   Vector3( 0, -1,  0), Vector3( 0, -1,  0), Vector3( 0, -1,  0), texture_image, Vector2(0, 0), Vector2(1, 1), Vector2(0, 1))
]

cube = Model(vertexes, triangles, Vector3(0, 0, 0), sqrt(3))

#----- Light
lights = [
    Light('AMBIENT', 0.2, None),
    Light('POINT', 0.6, Vector3(-3, 2, -10)),
    Light('DIRECTIONAL', 0.2, Vector3(-1, 0, 1))
]

#----- Camera
sqrt_2 = sqrt(2)
clipping_planes = [
    Plane(Vector3(0, 0, 1), -1), # Near
    Plane(Vector3(sqrt_2, 0, sqrt_2), 0), # Left
    Plane(Vector3(-sqrt_2, 0, sqrt_2), 0), # Right
    Plane(Vector3(0, -sqrt_2, sqrt_2), 0), # Top
    Plane(Vector3(0, sqrt_2, sqrt_2), 0) # Bottom
]

camera = Camera(Vector3(-3, 1, 2), Matrix44().y_rotation(radians(-30)), clipping_planes)


depth_buffer = [[0 for _ in range(screen_height)] for _ in range(screen_width)]

instances = [Instance(cube, Vector3(-1.5, 0, 7), Matrix44(), 0.75),
             Instance(cube, Vector3(1.25, 2.5, 7.5), Matrix44.y_rotation(radians(195)), 1.0),
             Instance(cube, Vector3(1.75, 0, 5), Matrix44.y_rotation(radians(-30)), 1.0)]

renderScene(camera, instances)
image.save("raster17.png")
