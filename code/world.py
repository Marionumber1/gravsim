import math

import pyglet

import physics
import objects
import graphics
import music

# Current world
current_world = None

class Background(pyglet.sprite.Sprite):
    def __init__(self, img, x, y, batch, group):
        # Initialize the Sprite class
        super().__init__(img=img, x=x, y=y, batch=batch, group=group)
    def on_load(self):
        pass
    def on_unload(self):
        pass

class World:
    def __init__(self, filename):
        # Create an object list, force list, media list, and graphics batch for the word
        self.objects = []
        self.forces = []
        self.media = []
        self.batch = pyglet.graphics.Batch()

        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

        self.drag_enabled = None

        self.read(filename)
    def read(self, filename):
        # Open the world file
        fin = open(filename, 'r')

        # Current object being parsed
        obj = None

        # Read each object from the file
        for line in fin.readlines():
            line = line.replace('\n','')
            line = line.replace('\r','')
            line = line.split(' ')

            # Parsing existing object
            if line[0] == '':
                # Get the name of the sub-object
                name = line[4]

                # Object force
                if name == "Gravity":
                    # Get the force acceleration and angle
                    acceleration = float(line[5])
                    angle = int(line[6])

                    # Create force for the object and add it
                    subobj = physics.Gravity(obj=obj, acceleration=acceleration, mass=obj.mass, angle=angle)
                    obj.forces.append(subobj)
                # Initial velocity (like being thrown)
                elif name == "InitialVelocity":
                    # Get the magnitude and angle
                    magnitude = float(line[5])
                    angle = int(line[6])

                    # Set the velocity and exerted force
                    obj.velocity = physics.Vector2D((obj.x, obj.y), magnitude, angle)
                    obj.exerted_force = obj.velocity * obj.mass
            # New object
            else:
                # Get the name of the object
                name = line[0]

                # Audio/visual stuff
                if name == "Background":
                    obj = Background(img=pyglet.image.load("../sprites/" + line[1]), x=0, y=0, batch=self.batch, group=self.background)
                    self.media.append(obj)
                elif name == "MusicPlayer":
                    obj = music.MusicPlayer(name=line[1])
                    self.media.append(obj)

                # Various objects
                if name == "Sphere":
                    # Get the coordinates and properties of the sphere
                    x = float(line[1])
                    y = float(line[2])
                    radius = float(line[4])
                    mass = float(line[5])

                    # Create a sphere object
                    obj = objects.Sphere(img=pyglet.image.load("../sprites/" + line[3]), x=x, y=y, radius=radius, mass=mass, batch=self.batch, group=self.foreground)
                    self.objects.append(obj)

                # Forces
                if name == "Gravity":
                    # Get the force acceleration and angle
                    acceleration = float(line[1])
                    angle = int(line[2])

                    # Create force for the object and add it
                    obj = physics.Gravity(obj=None, acceleration=acceleration, mass=1, angle=angle)
                    self.forces.append(obj)
                if name == "Drag":
                    self.drag_enabled = float(line[1])
    def play(self):
        global current_world

        # Check for Drag and enable
        if self.drag_enabled:
            for obj in self.objects:
                obj.forces.append(physics.Drag(obj, self.drag_enabled))

        old_world = current_world
        current_world = self

        window = graphics.get_current_window()

        # Pop all the old handlers
        if old_world:
            for obj in old_world.objects:
                obj.on_unload()
                window.remove_handlers(obj)

        # Push all the new handlers
        for obj in self.objects:
            obj.on_load()
            window.push_handlers(obj)

        # Switch to the new graphics
        graphics.set_current_batch(self.batch)
    def end(self):
        window = graphics.get_current_window()

        for obj in self.objects:
            obj.on_unload()
            window.remove_handlers(obj)

# Get the current world
def get_current_world():
    return current_world
