from psychopy import visual, event

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)

# Define the vertices of a triangle
vertices = [(0, 0), (100, 200), (-100, 200)]  # Triangle vertices

# Create a polygon stimulus using the vertices
triangle = visual.Polygon(win, vertices=vertices, fillColor='green', lineColor=None)

# Draw the triangle
triangle.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()
