from math import sqrt

class Vector3:
    __slots__ = ('_v',)


    def __init__(self, *args):
        """Creates a Vector3 from 3 numeric values or a list-like object
        containing at least 3 values. No arguments result in a null vector.

        """
        if len(args) == 3:
            self._v = list(args[:3])
            return

        if not args:
            self._v = [0, 0, 0]
        elif len(args) == 1:
            self._v = list(args[0][:3])
        else:
            raise ValueError("Vector3.__init__ takes 0, 1 or 3 parameters")
    
    @classmethod
    def from_iter(cls, iterable):
        """Creates a Vector3 from an iterable containing at least 3 values."""
        next = iter(iterable).__next__()
        v = cls.__new__(cls, object)
        v._v = [ float(next()), float(next()), float(next()) ]
        return v

    @property
    def x(self):
        return self._v[0]

    @x.setter
    def x(self, value):
        self._v[0] = value

    @property
    def y(self):
        return self._v[1]
    @y.setter
    def y(self, value):
        self._v[1] = value
        
    @property
    def z(self):
        return self._v[2]

    @z.setter
    def z(self, value):
        self._v[2] = value
        
    @property
    def r(self):
        return self._v[0]

    @property
    def g(self):
        return self._v[1]

    @property
    def b(self):
        return self._v[2]

    @property
    def length(self):
        x,y,z = self._v
        return sqrt(x * x + y * y + z * z)
    
    def __repr__(self):
        x, y, z = self._v
        return "Vector3(%s, %s, %s)" % (x, y, z)


    def __getitem__(self, index):
        """Retrieves a component, given its index.

        index -- 0, 1 or 2 for x, y or z

        """
        return self._v[index]
    
    def __add__(self, rhs):
        """Returns the result of adding a vector (or collection of 3 numbers)
        from this vector.

        rhs -- Vector or sequence of 3 values

        """
        x, y, z = self._v
        ox, oy, oz = rhs
        return Vector3(x+ox, y+oy, z+oz)

    def __iadd__(self, rhs):
        """Adds another vector (or a collection of 3 numbers) to this vector.

        rhs -- Vector or sequence of 2 values

        """
        ox, oy, oz = rhs
        v = self._v
        v[0] += ox
        v[1] += oy
        v[2] += oz
        return self

    def __neg__(self):
        """
        invert 
        """
        x, y, z = self._v
        return Vector3(-x, -y, -z)

    def __sub__(self, rhs):
        """Returns the result of subtracting a vector (or collection of
        3 numbers) from this vector.

        rhs -- 3 values

        """

        x, y, z = self._v
        ox, oy, oz = rhs
        return Vector3(x-ox, y-oy, z-oz)


    def __isub__(self, rhs):
        """Subtracts another vector (or a collection of 3 numbers) from this
        vector.

        rhs -- Vector or sequence of 3 values

        """
        ox, oy, oz = rhs
        v = self._v
        v[0] -= ox
        v[1] -= oy
        v[2] -= oz
        return self

    def __mul__(self, rhs):
        """Return the result of multiplying this vector by another vector, or
        a scalar (single number).


        rhs -- Vector, sequence or single value.

        """
        x, y, z = self._v
        if hasattr(rhs, "__getitem__"):
            ox, oy, oz = rhs
            return Vector3(x*ox, y*oy, z*oz)
        else:
            return Vector3(x*rhs, y*rhs, z*rhs)

    def __rmul__(self, lhs):

        x, y, z = self._v
        if hasattr(lhs, "__getitem__"):
            ox, oy, oz = lhs
            return Vector3(x*ox, y*oy, z*oz)
        else:
            return Vector3(x*lhs, y*lhs, z*lhs)
        
    def __imul__(self, rhs):
        """Multiply this vector by another vector, or a scalar
        (single number).

        rhs -- Vector, sequence or single value.

        """

        v = self._v
        if hasattr(rhs, "__getitem__"):
            ox, oy, oz = rhs
            v[0] *= ox
            v[1] *= oy
            v[2] *= oz
        else:
            v[0] *= rhs
            v[1] *= rhs
            v[2] *= rhs

        return self

        
    def __truediv__(self, rhs):
        """Return the result of dividing this vector by another vector, or a scalar (single number)."""
        x, y, z = self._v
        if hasattr(rhs, "__getitem__"):
            ox, oy, oz = rhs
            return Vector3(x/ox, y/oy, z/oz)
        else:
            return Vector3(x/rhs, y/rhs, z/rhs)

    def __itruediv__(self, rhs):
        """Divide this vector by another vector, or a scalar (single number)."""

        v = self._v
        if hasattr(rhs, "__getitem__"):
            ox, oy, oz = rhs
            v[0] /= ox
            v[1] /= oy
            v[2] /= oz
        else:
            v[0] /= rhs
            v[1] /= rhs
            v[2] /= rhs
        return self

    def dot(self, other):

        """Returns the dot product of this vector with another.

        other -- A vector or tuple

        """
        x, y, z = self._v
        ox, oy, oz = other
        return x*ox + y*oy + z*oz
    
    def cross(self, other):

        """Returns the cross product of this vector with another.

        other -- A vector or tuple

        """

        x, y, z = self._v
        bx, by, bz = other
        return Vector3( y*bz - by*z,
                        z*bx - bz*x,
                        x*by - bx*y )

    def normalize(self):
        """Scales the vector to be length 1."""
        v = self._v
        x, y, z = v
        l = sqrt(x*x + y*y + z*z)
        try:
            v[0] /= l
            v[1] /= l
            v[2] /= l
        except ZeroDivisionError:
            v[0] = 0.0
            v[1] = 0.0
            v[2] = 0.0
        return self

    def as_tuple(self):
        """Returns a tuple of the x, y, z components. A little quicker than
        tuple(vector)."""
        return tuple(self._v)
