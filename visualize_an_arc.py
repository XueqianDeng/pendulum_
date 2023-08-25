from psychopy import visual, core

# Define monitor specifications
monitor_width = 1920  # Width of the monitor screen in pixels
monitor_distance = 60  # Distance from the screen in centimeters

# Create a window
win = visual.Window(
    size=(800, 600),
    fullscr=False,
    allowGUI=False,
    monitor="testMonitor",  # Provide a name for the monitor
    units="deg",
    screen=0,  # The screen number to display the window on
    waitBlanking=True
)

# Create an arc stimulus
arc = visual.ShapeStim(
    win=win,
    units="deg",
    lineColor="white",
    lineWidth=5,
    fillColor=None,
    vertices=[[0, 0], [0, 10], [10, 10]],
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
