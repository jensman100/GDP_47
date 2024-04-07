'''  
This file contains the functions for the GUI programmes
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# functions which creates a sinosoidal waveform from max, min amplitudes and period
def create_waveform(min, max, duration, time = None):
    '''
    This function creates raw from min and max amplitudes and the period
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
    ''' This function creates a plot of the force and ROM waveforms for a given activity from raw time data
    
    '''
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

def read_activity(activity):
    ''' This function reads an activity stored in an excel file within the activity folder.
        The activity settings are stored in a sheet called 'settings' and the columns are:
        - Activity Name
        - Duration
        - Force Max
        - Force Min
        - ROM Max
        - ROM Min

        The raw data is stored in a sheet called 'waveforms' and the columns are:
        - Time
        - Angle
        - Force
'''
    # Read the settings
    code_path = os.getcwd()
    activity_folder_path = os.path.join(code_path, 'Activities')
    activity_file_name = os.path.join(activity_folder_path, activity + '.xlsx')
    try:
        settings = pd.read_excel(activity_file_name, sheet_name='settings')
        print('File read successfully.')
    except:
        print('Unable to read the file. Check the file name and whether the file is open.')
        return None, None, None, None, None, None, None, None, None
    
    activity_name = settings['Activity Name'][0]
    duration = settings['Duration'][0]
    force_max = settings['Force Max'][0]
    force_min = settings['Force Min'][0]
    rom_max = settings['ROM Max'][0]
    rom_min = settings['ROM Min'][0]

    # Read the waveforms
    waveforms = pd.read_excel(activity_file_name, sheet_name='waveforms')
    time = waveforms['Time']
    angle = waveforms['Angle']
    force = waveforms['Force']

    return activity_name, duration, force_max, force_min, rom_max, rom_min, time, angle, force