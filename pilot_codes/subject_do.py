import psychopy
from psychopy import visual, core, event, monitors
from psychopy.hardware import keyboard
from psychopy.visual import circle
import pandas as pd
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import WAIT_INFINITELY
import json
import websocket
import time
import asyncio
import random
import math
import pickle
import scipy as signal

# Global Variables
input_mapping = ['Dev2/ai0', 'Dev2/ai1']
nsamples = 10
samplerate = 1000

# Pendulum Parameters
conversion_unit_for_one_newton = 0.059  # Conversion 0.059 in forcekeyboard is 1 Newton
pendulum_length = 50  # in meters
pendulum_length_visual_coff = 4  # for visualization conversion, should be 200 in multiplication
pendulum_mass = 1  # 1 kilogram
pendulum_angle = np.pi / 4  # Initial angle (45 degrees)
pendulum_angular_velocity = 0.0
gravity = 9.8  # meter / second square
stiffness = 0.000001
inertia = pendulum_mass * pendulum_length * pendulum_length
drag_coefficient = 10  # Adjust the drag coefficient as needed
dt = 0.05  # in second
muscle_amplification = 100
muscle_left = 0
muscle_right = 0

def flow_maintainence(pend_angle):
    while pend_angle > 2 * np.pi:
        pend_angle = pend_angle - 2 * np.pi
    while pend_angle < 0:
        pend_angle = pend_angle + 2 * np.pi

    return pend_angle

def experiment_synchronize():
    global running, current_data, trials_run, trial_count, ofile, maintaining, already_in_range, init_time
    global pendulum_length, pendulum_mass, pendulum_angle, pendulum_angular_velocity, gravity, drag_coefficient
    global muscle_left, muscle_right
    last_time = time.time()
    while running:
        keys = event.getKeys(keyList=['escape'])
        if keys:
            window.close()
            core.quit()
        if np.sum(np.sum(current_data)) != 0:
            muscle_left = np.mean(current_data[:, 0])
            muscle_right = np.mean(current_data[:, -1])

        # Muscle Force Conversion

        print("Left,", muscle_left)
        print("Right", muscle_right)

        muscle_right = np.abs(muscle_right) / conversion_unit_for_one_newton * muscle_amplification
        muscle_left = - np.abs(muscle_left) / conversion_unit_for_one_newton * muscle_amplification

        print("Abs Left", muscle_left)
        print("Abs Right", muscle_right)

        # Time Elapsed
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time
        print("Time", elapsed_time)

        # Pendulum Physics
        pendulum_angular_acceleration = - pendulum_mass * gravity * pendulum_length * np.sin(pendulum_angle) \
                                        - drag_coefficient * pendulum_angular_velocity - stiffness * (pendulum_angle - np.pi) * \
                                        (np.abs(muscle_left) + np.abs(muscle_right)) + (muscle_left + muscle_right)
        pendulum_angular_acceleration = pendulum_angular_acceleration / inertia * dt
        pendulum_angular_velocity += pendulum_angular_acceleration
        pendulum_angle += pendulum_angular_velocity

        # Reset angle if greater overflow or underflow
        pendulum_angle = flow_maintainence(pendulum_angle)

        # Record Data
        with ni.Task() as read_task:
            for i in input_mapping:
                read_task.ai_channels.add_ai_voltage_chan(i)
            read_task.timing.cfg_samp_clk_timing(rate=samplerate, source='OnboardClock',
                                                 samps_per_chan=nsamples)
            indata = read_task.read(nsamples, timeout=WAIT_INFINITELY)
            current_data = np.asarray(indata).T
        record_data = np.append(np.mean(current_data, axis=0), current_time)
        ofile.write(str(record_data) + "\n")

        # Update Pendulum Visuals
        pendulum.start = (0, 0)
        pendulum.end = (pendulum_length * pendulum_length_visual_coff * np.sin(pendulum_angle), -pendulum_length * pendulum_length_visual_coff * np.cos(pendulum_angle))
        ball_pos = (pendulum_length * pendulum_length_visual_coff * np.sin(pendulum_angle), -pendulum_length * pendulum_length_visual_coff * np.cos(pendulum_angle))

        # Draw Pendulum and Ball
        pivot.draw()
        pendulum.draw()
        ball.pos = ball_pos
        ball.draw()
        window.flip()

        #  Maintaining Check Code
        if 150 < np.degrees(pendulum_angle) < 240 and not already_in_range:
            print("Here")
            already_in_range = True
            init_time = time.time()
        if not (150 < np.degrees(pendulum_angle) < 240) and already_in_range:
            already_in_range = False
            init_time = 0
        if 150 < np.degrees(pendulum_angle) < 240 and already_in_range:
            timer = time.time()
            if 100 > timer - init_time > 30:
                maintaining = True
        print('Status', already_in_range, maintaining)

        if maintaining:
            trial_count += 1
            ofile.close()
            ofile = open("data/" + subject_label + str(trial_count) + ".txt", "w")
            ofile.write(subject_label + "\n")
            ofile.write(" ".join(input_mapping) + "\n")
            # Create a text stimulus
            message = visual.TextStim(window, text="Wait for the next game", height=30, color='black')
            # Draw the text stimulus
            message.draw()
            window.flip()
            # Wait for 3 seconds
            core.wait(3)
            pendulum_angle = np.pi / 4  # Initial angle (45 degrees)
            maintaining = False

        if trial_count > trials_run:
            running = False

## Main Code


# Data Parameters
subject_label = "Test"
N_channels = 2 # recording channels
current_data = np.zeros([N_channels, nsamples])

# Window Parameters
window_size = [800, 600]
window = visual.Window(window_size, units='pix', fullscr=False)

# Pendulum Visuals
pivot = visual.Rect(window, width=10, height=10, fillColor='black')
pendulum = visual.Line(window, start=(0, 0), end=(pendulum_length * np.sin(pendulum_angle),
                                                   -pendulum_length * np.cos(pendulum_angle)),
                       lineColor='black', lineWidth=2)
ball_radius = 20
ball = visual.Circle(window, radius=ball_radius, fillColor='red', lineColor='black', lineWidth=2)

# Setting up
trials_run = 100
trial_count = 0
running = True
maintaining = False
already_in_range = False
ofile = open("data/" + subject_label + str(trial_count) + ".txt", "w")
ofile.write(subject_label + "\n")
ofile.write(" ".join(input_mapping) + "\n")

# asyncio.get_event_loop().run_until_complete(main())
init_time = time.time()
experiment_synchronize()

window.close()
core.quit()
