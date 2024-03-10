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
# {key: [duration, start_time, cycles]}
force_history = [] # Create a list to store the force history
angle_history = [] # Create a list to store the angle history
time_history = [] # Create a list to store the force time history
start_time = 0
error = False

for setting in settings:
    if not error:
        print(f'Processing {setting} settings...')
        # If setting is a read setting, read the mission cycle stated and add
        if setting[:4] == 'Read':
            # Preparing to read new mission cycle, checking if read before
            fms_file_name, addon, settings_repeats, setting_counts = previous_mission_cycle_name(settings_repeats, setting_counts, setting)
            # Reading previous mission cycle
            force_angle_sheet, settings_sheet, error = read_previous_mission_cycle(fms_file_name)
            if not error:
                # Updating current mission cycle
                force_history, angle_history, time_history, start_time, timings = combining_mission_cyles(force_angle_sheet, start_time, settings_sheet, addon, timings, force_history, angle_history, time_history)
            else:
                print(f'ERROR: {setting} not processed due to error(s). See error message(s) above')

        elif setting in excel.sheet_names:
            # Reading setting sheet
            df = read_setting(file_location, setting)
            df, error = prepare_setting(df)

            if not error:
                cycles, setting, plot = test_in_settings(settings_repeats, setting, setting_counts, mission_cycle)
                # Test if plotting, if true create an set of axes
                axsb, axsa = test_if_plot(plot, setting, df)
                # Plotting degree time graph
                angle, time = plot_degree_vs_time(df, axsb, plot)

                # Plotting force time graph
                force = plot_force_vs_time(df, axsa, plot, angle, time)

                # Test which side of 0 the max and min RoM are
                max_rom_0, min_rom_0, total_time = test_roms(df)
                    
                # Updating mission cycle with next angle settings
                angle_history, time_history = update_mission_cycle_angles(time, angle, cycles, start_time, angle_history, time_history, total_time, max_rom_0, min_rom_0)

                # Updating mission cycle with next force settings
                force_history, duration_with_cycles = update_mission_cycle_forces(time, force, cycles, start_time, force_history, time_history, total_time, max_rom_0, min_rom_0)

                timings[setting] = [duration_with_cycles, start_time, cycles]
                start_time += duration_with_cycles
            else:
                print(f'ERROR: {setting} not processed due to error(s). See error message(s) above')
        else:
            print(f'Warning: {setting} sheet not found')


if not error:
### Plotting mission cycle timeline
    print('Processing Mission Cycle...')
    mission_cycle_graphs(timings, start_time, time_history, force_history, angle_history)

### Writing to Excel
    print('Writing to Excel...')
    writing_to_excel(time_history, force_history, angle_history, timings, 'output_1.xlsx')

### Complete
    print('Complete.')