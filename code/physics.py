import math
import pyglet

# 2D vector class
class Vector2D:
    def __init__(self, tail=(0,0), *args):
        # Set the starting coordinates of the vector
        self.tail = tail

        # Direction provided as a tuple
        if len(args) == 1:
            self.direction = args[0]
            self.angle = self.get_angle()
        # Direction provided as an angle
        elif len(args) == 2:
            # Get the magnitude and angle
            magnitude = args[0]
            self.angle = math.radians(args[1] + 90)

            # Calculate the direction from it
            self.direction = (magnitude * math.cos(self.angle), magnitude * math.sin(self.angle))
    def get_angle(self):
        x, y = self.direction
        if x == 0:
            return 0
        elif y == 0:
            return math.pi / 2
        else:
            return math.atan(x / y)
    def __add__(self, other):
        if not issubclass(type(other), Vector2D):
            raise Exception("Both operands of vector addition must be vectors")

        direction = (self.direction[0] + other.direction[0], self.direction[1] + other.direction[1])
        return Vector2D(self.tail, direction)
    def __radd__(self, other):
        return self + other
    def __sub__(self, other):
        if not issubclass(type(other), Vector2D):
            raise Exception("Both operands of vector subtraction must be vectors")

        direction = (self.direction[0] - other.direction[0], self.direction[1] - other.direction[1])
        return Vector2D(self.tail, direction)
    def __mul__(self, other):
        # Scalar multiplication
        if type(other) == float or type(other) == int:
            new = Vector2D(self.tail, (self.direction[0] * other, self.direction[1] * other))
            return new
    def __rmul__(self, other):
        return self * other
    def __truediv__(self, other):
        # Scalar division
        if type(other) == float or type(other) == int:
            new = Vector2D(self.tail, (self.direction[0] / other, self.direction[1] / other))
            return new
    def __neg__(self):
        return Vector2D(self.tail, -self.direction[0], -self.direction[1])
    def __str__(self):
        # Convert to string (for debugging)
        return "(%f.4, %f.4) at %d degrees" % (self.direction[0], self.direction[1], self.angle)
    def __hash__(self):
        # So this can be used as a dict key
        return id(self)
    def magnitude(self):
        return math.sqrt((self.direction[0] ** 2) + (self.direction[1] ** 2))

# Gravity acting on an object
class Gravity(Vector2D):
    def __init__(self, obj, acceleration=1, mass=1, angle=0):
        # Initialize the Vector2D class
        if obj:
            super().__init__((obj.x,obj.y), acceleration * mass, angle)
        else:
            super().__init__((0,0), acceleration * mass, angle)

        # Object
        self.obj = obj
    def on_load(self):
        pass

# Drag acting upon an object
class Drag(Vector2D):
    def __init__(self, obj, coefficent=.47):
        super().__init__((0, 0), 0, 0)

        self.obj = obj
        self.coefficent = coefficent
    def __add__(self, target):
        # We need to calculate the actual drag while adding
        dx = self.coefficent * (self.obj.density * self.obj.velocity.direction[0] ** 2) / 2 * self.obj.reference_area
        dy = self.coefficent * (self.obj.density * self.obj.velocity.direction[1] ** 2) / 2 * self.obj.reference_area
        return self._add(target) - Vector2D((0, 0), -dx, -dy)

    def __radd__(self, target):
        return self + target

    def _add(self, other):
        if not issubclass(type(other), Vector2D):
            raise Exception("Both operands of vector addition must be vectors")

        direction = (self.direction[0] + other.direction[0], self.direction[1] + other.direction[1])
        return Vector2D(self.tail, direction)


# Object
class Object(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, mass, surface_area, batch, group):
        # Initialize the Sprite class
        super().__init__(img=img, x=x, y=y, batch=batch, group=group)

        # Mass and surface area
        self.mass = mass
        self.surface_area = surface_area

        # Current velocity and force exerted
        self.velocity = Vector2D((x,y), 0, 0)
        self.exerted_force = Vector2D((0,0), 0, 0)

        # Force and subobject lists
        self.forces = []
        self.objects = []

        # Detect which objects it has collided with
        self.collided_objects = []
    def __hash__(self):
        return id(self)

# Check if floats are close enough to be considered equal
def almost_equal(a, b, dp=4):
    return round(a, dp) == round(b, dp)
