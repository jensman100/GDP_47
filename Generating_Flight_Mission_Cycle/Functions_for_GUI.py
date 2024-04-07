'''  
This file contains the functions for the GUI programmes
'''
import numpy as np
import matplotlib.pyplot as plt

# functions which creates a sinosoidal waveform from max, min amplitudes and period
def create_waveform(min, max, duration, time = None):
    '''
    This function creates a sinosoidal waveform from the min and max amplitudes and the period
    '''
    if time is None:
        time = np.linspace(0, duration, 50)

    amplitude = (max - min)/2
    y_offset = (max + min)/2
    if max < 0 or min > 0 or amplitude == 0:
        x_offset = 0
    else:
        x_offset =np.arcsin(-y_offset/amplitude)
    wave = amplitude * np.sin(2 * np.pi * time/duration + x_offset) + y_offset
    return time, wave

def create_force_rom_plot(activity_name, time, force, angle):
    # Create plot
    plt.figure()  # Create a new figure
    # Set suptitle
    plt.suptitle(activity_name)

    # Plot Force
    plt.subplot(2, 1, 1)
    plt.plot(time, force)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Force')
    plt.tight_layout()  # Add this line to adjust the spacing between subplots

    # Plot ROM
    plt.subplot(2, 1, 2)
    plt.plot(time, angle)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (degrees)')
    plt.title('ROM')
    plt.tight_layout()  # Add this line to adjust the spacing between subplots

    # Show plot
    plt.show()