# Import necessary libraries
from psychopy import visual, event, core

# Create a window
win = visual.Window(size=(800, 600), units='pix')

# Define colors
yellow = (1, 1, 0)
black = (-1, -1, -1)

# Draw the lightbulb shape using drawing primitives
lightbulb = visual.Circle(win, radius=80, pos=(0, 0), fillColor=yellow, lineColor=black)
lamp = visual.Rect(win, width=40, height=100, pos=(0, -80), fillColor=black)

# Draw the lightbulb components
lightbulb.draw()
lamp.draw()

# Update the window
win.flip()

# Wait for a response
event.waitKeys()

# Close the window
win.close()
