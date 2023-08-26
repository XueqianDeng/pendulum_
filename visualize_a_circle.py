from psychopy import visual, event

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)

# Create a half circle stimulus
half_circle = visual.Circle(win, radius=100, fillColor='blue', start=0, end=180)

# Draw the half circle
half_circle.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()
