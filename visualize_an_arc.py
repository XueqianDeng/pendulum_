from psychopy import visual, core

# Create a window
win = visual.Window(size=(800, 600), fullscr=False, allowGUI=False)

# Create an arc stimulus
arc = visual.ShapeStim(
    win=win,
    units="deg",
    lineColor="white",
    lineWidth=5,
    fillColor=None,
    vertices=[[0, 0], [0, 100], [100, 100]],
    closeShape=False
)

# Draw the arc
arc.draw()

# Update the window
win.flip()

# Wait for a key press or a certain duration
core.wait(2)

# Close the window
win.close()
