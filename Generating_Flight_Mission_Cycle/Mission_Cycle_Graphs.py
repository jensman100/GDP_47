''' This script reads an excel file and creates a timeline, a force time graph and a degree time graph. 
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
'''
### Importing functions
from Functions_for_Mission_Cycle_Graphs import *

### Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt


### Reading the flight mission cycle sheet
print('Reading Excel File...')
file_location = 'Flight_Mission_Cycle.xlsx'

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
# count the repetitions of each setting
settings_repeats = mission_cycle.index.value_counts().to_dict()
setting_counts = dict.fromkeys(mission_cycle.index, 0)
        
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
            if settings_repeats[setting] > 1 and setting_counts[setting] != 0:
                setting_repeat_no = setting_counts[setting]
                cycles = list(mission_cycle.loc[setting, 'No. of cycles'])[setting_repeat_no]
                setting_counts[setting] += 1
                setting = f'{setting} (Repeat{setting_repeat_no})'
                plot = False
            elif settings_repeats[setting] > 1:
                cycles = list(mission_cycle.loc[setting, 'No. of cycles'])[0]
                setting_counts[setting] += 1
                plot = True
            else:
                cycles = mission_cycle.loc[setting, 'No. of cycles']
                setting_counts[setting] += 1
                plot = True

            # Creating figure plot with mosaic
            if plot:
                fig, axs = plt.subplot_mosaic('''   aaa
                                                    bbc''', figsize=(10, 8))
                # a for force time graph, b for degree time graph, c for angle visual

                fig.suptitle(f'{setting} settings', fontsize = 20) # adding title
                # Plotting angle visual
                plot_angle_visual(df, axs['c'])

            # Plotting degree time graph
            angle, atime = plot_degree_vs_time(df, axs['b'], plot)

            # Plotting force time graph
            force, ftime = plot_force_vs_time(df, axs['a'], plot, angle, atime)

            max_rom, min_rom, period, total_time = calcualte_roms_and_periods(df)
            max_rom_0 = False
            min_rom_0 = False
            if max_rom < 0:
                max_rom_0 = True
            if min_rom > 0:
                min_rom_0 = True

            # Updating mission cycle with next angle settings
            angle_history, atime_history = update_mission_cycle_angles(atime, angle, cycles, start_time, angle_history, atime_history, total_time, max_rom_0, min_rom_0)

            # Updating mission cycle with next force settings
            force_history, ftime_history, duration_with_cycles = update_mission_cycle_forces(ftime, force, cycles, start_time, force_history, ftime_history, total_time, max_rom_0, min_rom_0)

            # Updating timings dictionary
            timings[setting] = [duration_with_cycles, start_time, cycles]
            start_time += duration_with_cycles

        else:
            print(f'ERROR: {setting} not processed due to error(s). See error message(s) above')
    else:
        print(f'Warning: {setting} sheet not found')

### Plotting mission cycle timeline
if not error:
    print('Processing Mission Cycle...')
    fig, axs = plt.subplot_mosaic('''a
                                b
                                c''', figsize=(10, 8))
    fig.suptitle('Flight Mission Cycle', fontsize = 20)
    plot_timeline_dict(timings, start_time, axs['a']) # Inputs are dictionary and final start and duration times
    plot_mission_force(ftime_history, force_history, axs['b'])
    plot_mission_angle(atime_history, angle_history, axs['c'])
    fig.tight_layout()
    print('Displaying Graphs...')
    # plt.show()

### Writing to Excel
    print('Writing to Excel...')
    writing_to_excel(ftime_history, force_history, angle_history, timings, 'output.xlsx')
    print('Complete.')