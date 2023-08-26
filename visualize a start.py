# Import necessary libraries
from psychopy import visual, event, core
import numpy as np

# Create a window
win = visual.Window(size=(800, 600), units='pix')

# Define colors
yellow = (1, 1, 0)  # Yellow in RGB

# Create a visually pleasing five-pointed star using ShapeStim with custom vertices
outer_radius = 100
inner_radius = 40
angle_offset = -np.pi / 2  # Offset angle to start drawing the star
angle_between_points = 2 * np.pi / 5  # Angle between each point

star_vertices = []
for i in range(5):
    angle = angle_offset + i * angle_between_points
    outer_x = outer_radius * np.cos(angle)
    outer_y = outer_radius * np.sin(angle)
    star_vertices.append((outer_x, outer_y))

    inner_angle = angle + angle_between_points / 2
    inner_x = inner_radius * np.cos(inner_angle)
    inner_y = inner_radius * np.sin(inner_angle)
    star_vertices.append((inner_x, inner_y))

# Create ShapeStim object for the star
star = visual.ShapeStim(win, vertices=star_vertices, fillColor=yellow, lineColor=None)

# Draw the star
star.draw()

# Update the window
win.flip()

# Wait for a response
event.waitKeys()

# Close the window
win.close()
