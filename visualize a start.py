# Import necessary libraries
from psychopy import visual, event, core

# Create a window
win = visual.Window(size=(800, 600), units='pix')

# Define colors
yellow = (1, 1, 0)

# Create a star shape using Polygon
star_points = [
    (0, 100),    # Top point
    (21, 30),    # Top right point
    (100, 30),   # Right point
    (36, -12),   # Bottom right point
    (57, -90),   # Bottom point
    (0, -48),    # Bottom left point
    (-57, -90),  # Bottom left point
    (-36, -12),  # Bottom left point
    (-100, 30),  # Left point
    (-21, 30)    # Top left point
]
star = visual.Polygon(win, vertices=star_points, fillColor=yellow)

# Draw the star
star.draw()

# Update the window
win.flip()

# Wait for a response
event.waitKeys()

# Close the window
win.close()
