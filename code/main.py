import pyglet
import sys

import world
import graphics
import collision
import physics

# Update event loop
def update(dt):
    # Get the current world
    current_world = world.get_current_world()

    # Detect the collisions of each object
    collisions = collision.detect_collisions(current_world.objects)
    collided = collision.collided_objects(collisions)
    collisions = dict(collisions)
    
    # Move each object in the world
    for obj in current_world.objects:
        # Sum each of the object forces themselves
        net_force = obj.forces[0]
        for force in obj.forces:
            net_force += force

        # Now sum each world force
        for force in current_world.forces:
            net_force += (force * obj.mass)

        # Sum each colliding force
        if obj in collided:
            net_force += collisions[obj].exerted_force

        # Add the net force to the object's velocity
        obj.velocity += ((net_force / obj.mass) / 60)

        # Use the velocity to change X and Y
        obj.x += obj.velocity.direction[0]
        obj.y += obj.velocity.direction[1]

        # Change the object's exerted force
        obj.exerted_force = (obj.velocity * obj.mass) - obj.exerted_force

# Initialize the graphics
graphics.init_graphics()

# Load the correct world
if len(sys.argv) > 1:
    title = world.World("../worlds/%s.txt" % sys.argv[1])
else:
    title = world.World("../worlds/test.txt")

# Begin playing the title screen
title.play()

# Start the event loop
pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
