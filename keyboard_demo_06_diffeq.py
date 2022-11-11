# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio
import struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk

BLOCKLEN = 64        # Number of frames per block
WIDTH = 2         # Bytes per sample
CHANNELS = 1         # Mono
RATE = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f1 = 400    # Frequency (Hz)

ORDER = 2   # filter order

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude

states = np.zeros(ORDER)
x = np.zeros(BLOCKLEN)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
    format=PA_FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=False,
    output=True,
    frames_per_buffer=128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS = False


def my_function(event):
    global CONTINUE
    global KEYPRESS
    global f1
    print('You pressed ' + event.char)
    if event.char == 'q':
        print('Good bye')
        CONTINUE = False
    if event.char == 'a':
        f1 = 50
    if event.char == 's':
        f1 = 100
    if event.char == 'd':
        f1 = 150
    if event.char == 'f':
        f1 = 200
    if event.char == 'g':
        f1 = 250
    if event.char == 'h':
        f1 = 300
    if event.char == 'j':
        f1 = 350
    if event.char == 'k':
        f1 = 400
    KEYPRESS = True


root = Tk.Tk()
root.bind("<Key>", my_function)

print('Press keys for sound.')
print('Press "q" to quit')

while CONTINUE:
    root.update()

    om1 = 2.0 * pi * float(f1)/RATE

    # Filter coefficients (second-order IIR)
    a = [1, -2*r*cos(om1), r**2]
    b = [r*sin(om1)]

    if KEYPRESS and CONTINUE:
        # Some key (not 'q') was pressed
        x[0] = 10000.0

    [y, states] = signal.lfilter(b, a, x, zi=states)

    x[0] = 0.0
    KEYPRESS = False

    y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)     # Clipping

    # Convert to binary binary data
    binary_data = struct.pack('h' * BLOCKLEN, *y)
    # Write binary binary data to audio output
    stream.write(binary_data, BLOCKLEN)

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
