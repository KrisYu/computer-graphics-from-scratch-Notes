r = 1
n = 15

from cmath import pi
from math import sqrt, cos, sin
from vector3 import Vector3

vertexes= []

for d in range(n + 1):
    yb = 2 * r * d / n - r
    for i in range(n):
        alpha = 2 * pi * i / n
        rprime = sqrt(r * r - yb * yb)
        xb = rprime * cos(alpha)
        zb = rprime * sin(alpha)
        vertexes.append(Vector3(xb, yb, zb))
        print (xb,'\t',yb,'\t',zb)


for i in range(n):
    start = i * n
    for j in range(n - 1):
        a = start + j
        b = a + 1
        c = a + n  # this circle to next same index point in circle
        d = c + 1
        triangles.append([a, b, c])
        triangles.append([a, b, d])

