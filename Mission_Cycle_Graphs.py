''' This script reads an excel file and creates a timeline, a force time graph and a degree time graph. 
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
'''
### Importing functions
from Functions_for_Mission_Cycle_Graphs import *

### Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

### Reading the flight mission cycle sheet
print('Reading excel file...')
file_location = r'C:\Users\joeh2\OneDrive - University of Southampton\Documents\Southampton\GDP\General - Small Joint Implant Testing Rig\11 - Code\GDP_47\Flight_Mission_Cycle.xlsx'
try:
    excel = pd.ExcelFile(file_location)
except:
    print('ERROR: File cannot be opened. Please check the file location and whether it is open and try again.')
    exit()

try:
    mission_cycle = read_mission_cycle(file_location)
except:
    print("ERROR: Mission cycle cannot be read. Please check the sheet names are formatted correctly and try again")
    exit()

settings = list(mission_cycle.index) # Gathering setting names
if len(settings) < 1:
    print('ERROR: No settings entered. Please enter a mission cycle and try again')
    exit()

### Plotting setting graphs
timings = {} # Create a dictionary to store the start_time, duration of each setting 
# {key: [start_time, duration]}
force_history = [] # Create a list to store the force history
angle_history = [] # Create a list to store the angle history
ftime_history = [] # Create a list to store the force time history
atime_history = [] # Create a list to store the angle time history
start_time = 0

for setting in settings:
    print(f'Processing {setting} settings...')
    if setting in excel.sheet_names:
        # Reading setting sheet
        df = read_setting(file_location, setting)
        df, error = prepare_setting(df)

        if not error:
            # Data for timeline
            cycles = mission_cycle.loc[setting, 'No. of cycles']
            if setting not in timings:

                # Creating figure plot with mosaic
                fig, axs = plt.subplot_mosaic('''   aaa
                                                    bbc''', figsize=(10, 8))
                # a for force time graph, b for degree time graph, c for angle visual

                fig.suptitle(f'{setting} settings', fontsize = 20) # adding title

                plot_angle_visual(df, axs['c'])
                # Add in setting to apply force when angle is above a certain value
                force, ftime = plot_force_vs_time(df, axs['a'])                
                fduration = max(ftime)

                force = force * cycles
                updated_ftime = [x + start_time for x in ftime]

                number_of_changes = len(ftime)
                count = 1
                final_fvalue = updated_ftime[-1]
                while count < cycles:
                    updated_ftime += [x  + final_fvalue + (count-1) * fduration for x in ftime[-number_of_changes:]]
                    count += 1
                
                force_history += force 
                ftime_history += updated_ftime
                # Add in setting for sinonodal angle
                angle, atime = plot_degree_vs_time(df, axs['b'])

                aduration = max(atime)
                angle = angle * cycles

                updated_atime = [x + start_time for x in atime]

                number_of_changes= len(atime)
                count = 1
                final_avalue = updated_atime[-1]
                while count < cycles:
                    updated_atime += [x + final_avalue + (count-1)* aduration for x in atime[-number_of_changes:]]
                    count += 1
                
                angle_history += angle
                atime_history += updated_atime
                
                duration_with_cycles = fduration * cycles
                timings[setting] = [duration_with_cycles, start_time]
                start_time += duration_with_cycles

            else:
                print(f'ERROR: {setting} entered more than once. Please check the mission cycle and try again.')
                exit()
        else:
            print(f'ERROR: {setting} not processed due to error(s). See error message(s) above')
    else:
        print(f'Warning: {setting} sheet not found')

### Plotting mission cycle timeline
print('Processing Mission Cycle...')
fig, axs = plt.subplot_mosaic('''a
                            b
                            c''', figsize=(10, 8))
fig.suptitle('Flight Mission Cycle', fontsize = 20)
plot_timeline_dict(timings, start_time, axs['a']) # Inputs are dictionary and final start and duration times
plot_mission_force(ftime_history, force_history, axs['b'])
plot_mission_angle(atime_history, angle_history, axs['c'])
fig.tight_layout()
print('Displaying graphs...')
plt.show()
print('Complete.')