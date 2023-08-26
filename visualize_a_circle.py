from psychopy import visual, event

# Create a window
win = visual.Window(size=(800, 600), units='pix', fullscr=False)

# Create a circle stimulus
circle = visual.Circle(win, radius=100, fillColor='red')

# Draw the circle
circle.draw()
win.flip()

# Wait for a key press to close the window
event.waitKeys()

# Close the window
win.close()

core.quit()