# Import necessary libraries
from psychopy import visual, event, core

# Create a window
win = visual.Window(size=(800, 600), units='pix')

# Define colors
yellow = (1, 1, 0)
black = (-1, -1, -1)

# Create a lightbulb shape using Bézier curve control points
curve_points = [
    (-50, 0),
    (-100, 100),
    (100, 100),
    (50, 0)
]

# Draw the lightbulb shape using Bézier curve
lightbulb_curve = visual.ElementArrayStim(win, nElements=1, xys=curve_points, colors=yellow, elementTex=None, elementMask=None)

# Draw the lightbulb curve
lightbulb_curve.draw()

# Update the window
win.flip()

# Wait for a response
event.waitKeys()

# Close the window
win.close()
