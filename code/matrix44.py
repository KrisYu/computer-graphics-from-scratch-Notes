from math import sin,cos
from vector3 import Vector3

class Matrix44Error(Exception):
    """Matrix44 Exception class"""
    def __init__(self, description):
        Exception.__init__(self)
        self.description = description

    def __str__(self):
        return self.description

class Matrix44:

    _identity = ( (1.0 ,0.0 ,0.0 ,0.0),
                  (0.0 ,1.0 ,0.0 ,0.0),
                  (0.0 ,0.0 ,1.0 ,0.0),
                  (0.0 ,0.0 ,0.0 ,1.0) )

    __slots__ = ('_m',)

    def __init__(self, *args):

        """If no parameteres are given, the Matrix44 is initialised to the identity Matrix44.
        If 1 parameter is given it should be an iterable with the 16 values of the Matrix44.
        If 4 parameters are given they should be 4 sequences of up to 4 values.
        Missing values in each row are padded out with values from the identity matix
        (so you can use Vector3's or tuples of 3 values).

        """


        if not args:
            self._m = [1.,0.,0.,0., 0.,1.,0.,0., 0.,0.,1.,0., 0.,0.,0.,1.]
            return


        elif len(args) == 4:
            self._m = [1.,0.,0.,0., 0.,1.,0.,0., 0.,0.,1.,0., 0.,0.,0.,1.]

            row_0, row_1, row_2, row_3 = self._setters
            r1, r2, r3, r4 = args

            row_0(r1)
            row_1(r2)
            row_2(r3)
            row_3(r4)

        else:
            raise TypeError("Matrix44.__init__() takes 0, or 4 arguments (%i given)"%len(args))

    @property
    def row0(self):
        return tuple(self._m[0:4])
    @row0.setter
    def row0(self, values):
        values = tuple(values)[:4]
        self._m[0:len(values)] = values

    @property
    def row1(self):
        return tuple(self._m[4:8])
    @row1.setter
    def row1(self, values):
        values = tuple(values)[:4]
        self._m[4:4+len(values)] = values

    @property
    def row2(self):
        return tuple(self._m[8:12])
    @row2.setter
    def row2(self, values):
        values = tuple(values)[:4]
        self._m[8:8+len(values)] = values

    @property
    def row3(self):
        return tuple(self._m[12:16])
    @row3.setter
    def row3(self, values):
        values = tuple(values)[:4]
        self._m[12:12+len(values)] = values

    def rows(self):
        """Returns an iterator for the rows in the Matrix44 (yields 4 tuples
        of 4 values)."""

        m = self._m
        return iter(( tuple(m[0:4]),
                      tuple(m[4:8]),
                      tuple(m[8:12]),
                      tuple(m[12:16]) ))

    def __repr__(self):

        def format_row(row):
            return "(%s)" % ", ".join(str(value) for value in row )

        return "Matrix44(%s)" % \
            ",".join(format_row(row) for row in self.rows())


    def __mul__(self, rhs):
        """Returns the result of multiplying this Matrix44 by another, called
        by the * (multiply) operator."""

        m1_0,  m1_1,  m1_2,  m1_3, \
        m1_4,  m1_5,  m1_6,  m1_7, \
        m1_8,  m1_9,  m1_10, m1_11, \
        m1_12, m1_13, m1_14, m1_15 = self._m

        m2_0,  m2_1,  m2_2,  m2_3, \
        m2_4,  m2_5,  m2_6,  m2_7, \
        m2_8,  m2_9,  m2_10, m2_11, \
        m2_12, m2_13, m2_14, m2_15 = rhs._m

        retm =  [ m1_0 * m2_0 + m1_1 * m2_4 + m1_2 * m2_8 + m1_3 * m2_12,
                  m1_0 * m2_1 + m1_1 * m2_5 + m1_2 * m2_9 + m1_3 * m2_13,
                  m1_0 * m2_2 + m1_1 * m2_6 + m1_2 * m2_10 + m1_3 * m2_14,
                  m1_0 * m2_3 + m1_1 * m2_7 + m1_2 * m2_11 + m1_3 * m2_15,

                  m1_4 * m2_0 + m1_5 * m2_4 + m1_6 * m2_8 + m1_7 * m2_12,
                  m1_4 * m2_1 + m1_5 * m2_5 + m1_6 * m2_9 + m1_7 * m2_13,
                  m1_4 * m2_2 + m1_5 * m2_6 + m1_6 * m2_10 + m1_7 * m2_14,
                  m1_4 * m2_3 + m1_5 * m2_7 + m1_6 * m2_11 + m1_7 * m2_15,

                  m1_8 * m2_0 + m1_9 * m2_4 + m1_10 * m2_8 + m1_11 * m2_12,
                  m1_8 * m2_1 + m1_9 * m2_5 + m1_10 * m2_9 + m1_11 * m2_13,
                  m1_8 * m2_2 + m1_9 * m2_6 + m1_10 * m2_10 + m1_11 * m2_14,
                  m1_8 * m2_3 + m1_9 * m2_7 + m1_10 * m2_11 + m1_11 * m2_15,

                  m1_12 * m2_0 + m1_13 * m2_4 + m1_14 * m2_8 + m1_15 * m2_12,
                  m1_12 * m2_1 + m1_13 * m2_5 + m1_14 * m2_9 + m1_15 * m2_13,
                  m1_12 * m2_2 + m1_13 * m2_6 + m1_14 * m2_10 + m1_15 * m2_14,
                  m1_12 * m2_3 + m1_13 * m2_7 + m1_14 * m2_11 + m1_15 * m2_15 ]

        ret = self.__new__(self.__class__, object)
        ret._m = retm

        return ret


    @classmethod
    def scale(cls, scale_x, scale_y= None, scale_z= None):
        """Creates a scale Matrix44.
        If one parameter is given the scale is uniform,
        if three parameters are give the scale is different (potentialy) on each x axis.

        """

        m = cls.__new__(cls, object)
        return m.make_scale(scale_x, scale_y, scale_z)

    @classmethod
    def translation(cls, x, y, z):
        """Creates a translation Matrix44 to (x, y, z).

        x -- X Coordinate
        y -- Y Coordinate
        z -- Z Coordinate

        """

        m = cls.__new__(cls, object)
        return m.make_translation(x, y, z)

    @classmethod
    def translation_vec3(cls, v):
        """Creates a translation Matrix44 from Vector3. ).
        """
        x, y, z = v
        m = cls.__new__(cls, object)
        return m.make_translation(x, y, z)

    @classmethod
    def xyz_rotation(cls, angle_x, angle_y, angle_z):
        """Creates a Matrix44 that does a rotation about each axis.

        angle_x -- Angle of rotation, about x
        angle_y -- Angle of rotation, about y
        angle_z -- Angle of rotation, about z

        """

        m = cls.__new__(cls, object)
        return m.make_xyz_rotation(angle_x, angle_y, angle_z)

    @classmethod
    def x_rotation(cls, angle):
        """Creates a Matrix44 that does a rotation about the x axis.

        angle -- Angle of rotation (in radians)

        """

        m = cls.__new__(cls, object)
        return m.make_x_rotation(angle)


    @classmethod
    def y_rotation(cls, angle):
        """Creates a Matrix44 that does a rotation about the y axis.

        angle -- Angle of rotation (in radians)

        """

        m = cls.__new__(cls, object)
        return m.make_y_rotation(angle)


    @classmethod
    def z_rotation(cls, angle):
        """Creates a Matrix44 that does a rotation about the z axis.

        angle -- Angle of rotation (in radians)

        """

        m = cls.__new__(cls, object)
        return m.make_z_rotation(angle)

    def make_scale(self, scale_x, scale_y= None, scale_z= None):
        """Makes a scale Matrix44.

        If the scale_y and scale_z parameters are not given they default to the same as scale_x.

        """
        scale_y = scale_x if not scale_y else scale_y
        scale_z = scale_x if not scale_z else scale_z

        self._m =   [scale_x,  0,        0,       0,
                     0,        scale_y,  0,       0,
                     0,        0,        scale_z, 0,
                     0,        0,        0,       1]
        return self

    def make_translation(self, x, y, z):
       """Makes a translation Matrix44."""

       self._m =   [1,  0,  0,  x,
                    0,  1,  0,  y,
                    0,  0,  1,  z,
                    0,  0,  0,  1]
       return self

    def make_x_rotation(self, angle):
        """Makes a rotation Matrix44 around the x axis."""

        cos_a = cos(angle)
        sin_a = sin(angle)

        self._m =  [1,  0,        0,      0,
                    0,  cos_a,    sin_a,  0,
                    0,  -sin_a,   cos_a,  0,
                    0,  0,        0,      1]
        return self

    def make_y_rotation(self, angle):
        """Makes a rotation Matrix44 around the y axis."""

        cos_a = cos(angle)
        sin_a = sin(angle)

        self._m =  [ cos_a,  0,  -sin_a,  0,
                     0,      1,  0,       0,
                     sin_a,  0,  cos_a,   0,
                     0,      0,  0,       1]
        return self

    def make_z_rotation(self, angle):
        """Makes a rotation Matrix44 around the z axis."""

        cos_a = cos(angle)
        sin_a = sin(angle)

        self._m =  [  cos_a,   sin_a,  0,  0,
                     -sin_a,   cos_a,  0,  0,
                      0,       0,      1,  0,
                      0,       0,      0,  1]
        return self

    def make_xyz_rotation(self, angle_x, angle_y, angle_z):
        """Makes a rotation Matrix44 about 3 axis."""

        cx = cos(angle_x)
        sx = sin(angle_x)
        cy = cos(angle_y)
        sy = sin(angle_y)
        cz = cos(angle_z)
        sz = sin(angle_z)

        sxsy = sx*sy
        cxsy = cx*sy

        # http://web.archive.org/web/20041029003853/http:/www.j3d.org/matrix_faq/matrfaq_latest.html#Q35
        #A = cos(angle_x)
        #B = sin(angle_x)
        #C = cos(angle_y)
        #D = sin(angle_y)
        #E = cos(angle_z)
        #F = sin(angle_z)

    #     |  CE      -CF       D   0 |
    #M  = |  BDE+AF  -BDF+AE  -BC  0 |
    #     | -ADE+BF   ADF+BE   AC  0 |
    #     |  0        0        0   1 |

        self._m = [ cy*cz,  sxsy*cz+cx*sz,  -cxsy*cz+sx*sz, 0,
                    -cy*sz, -sxsy*sz+cx*cz, cxsy*sz+sx*cz,  0,
                    sy,     -sx*cy,         cx*cy,          0,
                    0,      0,               0,             1]

        return self

    def transform_vec4(self, v):
        """Transforms a vector4 and returns the result as a 4 element tuple.

        v -- Vector to transform

        """

        m = self._m
        x, y, z, w = v
        return ( m[0] * x + m[1] * y + m[2] * z  + m[3] * w,
                 m[4] * x + m[5] * y + m[6] * z  + m[7] * w,
                 m[8] * x + m[9] * y + m[10] * z + m[11] * w,
                 m[12] *x + m[13] * y + m[14] * z + m[15] *w)

    def transform_point(self, v):
        """
        Transform a point and return the result as Vector3.
        """
        m = self._m
        x, y, z = v
        w = 1

        result_w = m[12] * x + m[13] * y + m[14] * z + m[15] * w

        if (result_w == 0) or (abs(result_w) < 0.00000000000000001):
            raise Matrix44Error("Something wrong with the transform poit, w = 0 after translation")

        result_x =  (m[0] * x + m[1] * y + m[2] * z  + m[3] * w) / result_w
        result_y =  (m[4] * x + m[5] * y + m[6] * z  + m[7] * w) / result_w
        result_z =  (m[8] * x + m[9] * y + m[10] * z + m[11] * w) / result_w
        return Vector3(result_x, result_y, result_z)


    def transform_vector(self, v):
        """
        Transform a vector and return the result as Vector3.
        """
        m = self._m
        x, y, z = v
        w = 0

        result_w = m[12] * x + m[13] * y + m[14] * z + m[15] * w

        if (result_w != 0) or (abs(result_w) > 0.00000000000000001):
            raise Matrix44Error("Something wrong with the transform vector, w != 0 after translation")

        return Vector3( m[0] * x + m[1] * y + m[2] * z,
                        m[4] * x + m[5] * y + m[6] * z,
                        m[8] * x + m[9] * y + m[10] * z)


    def transform_vec3(self, v):
        """Transforms a Vector3 and returns the result as a Vector3.

        v -- Vector to transform

        """

        m = self._m
        x, y, z = v
        return Vector3( m[0] * x + m[1] * y + m[2] * z  + m[3],
                        m[4] * x + m[5] * y + m[6] * z  + m[7],
                        m[8] * x + m[9] * y + m[10] * z + m[11])

    def get_inverse_rotation(self):
        """Returns the inverse of a Matrix44 with only rotation.

        rotation matrix looks like:
        (( A B C 0 )
         ( D E F 0 )
         ( G H I 0 )
         ( 0 0 0 1 ))
        """

        ret = self.__new__(self.__class__, object)
        i = self._m

        i0,  i1,  i2,  i3, \
        i4,  i5,  i6,  i7, \
        i8,  i9,  i10, i11, \
        i12, i13, i14, i15 = i

        det = i0 * i5 * i10 + i1 * i6 * i8 + i2 * i4 * i9 \
               -i2 * i5 * i8  - i1 * i4 * i10 - i0 * i6 * i9


        if (det == 0) or (abs(det) < 0.00000000000000001):
            raise Matrix44Error("This Matrix44 can not be inverted")


        ret._m = [ i0, i4, i8, i12,
                   i1, i5, i9, i13,
                   i2, i6, i10, i14,
                   i3, i7, i11, i15 ]

        return ret

    def get_inverse_translation(self):
        """Returns the inverse of a Matrix44 with only translation.

        rotation matrix looks like:
        (( 1 0 0 x )
         ( 0 1 0 y )
         ( 0 0 1 z )
         ( 0 0 0 1 ))
        """

        ret = self.__new__(self.__class__, object)
        i = self._m

        i0,  i1,  i2,  i3, \
        i4,  i5,  i6,  i7, \
        i8,  i9,  i10, i11, \
        i12, i13, i14, i15 = i

        ret._m = [ 1, 0, 0, -i3,
                   0, 1, 0, -i7,
                   0, 0, 1, -i11,
                   0, 0, 0, 1 ]
        return ret
