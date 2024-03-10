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

for setting in settings:
    print(f'Processing {setting} settings...')
    if setting[:4] == 'Read':
        if settings_repeats[setting] == 1:
            settings_repeats.pop(setting)
            setting_counts.pop(setting)
            addon = '_0'
        else:
            addon = f'_{settings_repeats[setting]}'
            settings_repeats[setting] -= 1

        fms_name = f'{setting[5:]}'
        fms_file_name = fms_name + '.xlsx'
        try:
            force_angle_sheet = pd.read_excel(fms_file_name, sheet_name='Values', index_col=None, header=0)
            settings_sheet = pd.read_excel(fms_file_name, sheet_name='Settings', index_col=0, header=0)
        except:
            print('ERROR: File cannot be opened. Please check the file location and whether it is open and try again.')
            error = True
            exit()
        fms_times = list(force_angle_sheet['Time'] + start_time)
        force_history += list(force_angle_sheet['Force'])
        angle_history += list(force_angle_sheet['Angle'])
        time_history += fms_times

        # Update timings dictionary
        settings_sheet.loc['Start Time', :] += start_time
        fms_settings = list(settings_sheet.columns)
        for fms_setting in fms_settings:
            new_fms_setting = fms_setting + addon
            timings[new_fms_setting] = [settings_sheet.loc[ 'Duration', fms_setting], settings_sheet.loc['Start Time', fms_setting], settings_sheet.loc['No. of cycles', fms_setting]]

        start_time = fms_times[-1]
        error = False

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
    writing_to_excel(time_history, force_history, angle_history, timings, 'output.xlsx')

### Complete
    print('Complete.')