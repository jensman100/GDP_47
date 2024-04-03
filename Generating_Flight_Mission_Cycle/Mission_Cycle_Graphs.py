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
arduino_settings = {}
# {key: [list_of_timings, list_of_forces, list_of_angles]}
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
                if setting not in arduino_settings:
                    arduino_settings[setting] = [time, force, angle]
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

### Writing to c++ file
    print('Writing to C++...')

    # Reading the template text file
    file_name = 'Arduino template.txt'
    with open(file_name, 'r') as file:
        file_content = file.readlines()
    
    # Updating the first lane to state that the file has been modified
    file_content[1] = 'This file has been modified\n'

    # Inserting main script
    # Finding where the mission cycle starts
    mission_cycle_start = file_content.index('// Add mission cycle here\n')
    activity_start = mission_cycle_start + 1
    for activity in timings.keys():
        activity_string = activity.split('_')[0]
        # Writing function in format:
        # function_name(no. of cycles))
        file_content.insert(activity_start, f'{activity_string}({timings[activity][2]});\n')

    # Inserting fuctions
    # Finding where the functions start
    function_list_start = file_content.index('// Add functions here\n')
    function_start = function_list_start + 1

    for function in arduino_settings.keys():
        delay = (arduino_settings[function][0][1] - arduino_settings[function][0][0]) * 1000
        stored_delay = delay
        file_content.insert(function_start, f'void {function}(int cycles){{\n')
        function_start += 1
        file_content.insert(function_start, f'  for(int i = 0; i < cycles; i++){{\n')
        function_start += 1

        final_delay = False
        old_angle = np.nan
        old_force = np.nan

        for count in range(len(arduino_settings[function][0])):

            new_angle = int(arduino_settings[function][1][count]) 
            new_force = int(arduino_settings[function][2][count])

            if old_angle == new_angle and old_force == new_force:
                delay += (arduino_settings[function][0][count] - arduino_settings[function][0][count - 1]) * 1000
                final_delay = True

            else:
                final_delay = False
                if old_angle != new_angle:
                    file_content.insert(function_start, f'      analogWrite(11, {int(arduino_settings[function][1][count])});\n')
                    function_start += 1
                if old_force != new_force:
                    file_content.insert(function_start, f'      analogWrite(12, {int(arduino_settings[function][2][count])});\n')
                    function_start += 1

                file_content.insert(function_start, f'      delay({int(delay)});\n')
                function_start += 1
                delay = stored_delay

                old_angle = new_angle
                old_force = new_force
        
        if final_delay:
            file_content.insert(function_start, f'      delay({int(delay)});\n')
            function_start += 1

        file_content.insert(function_start, f'  }}\n')
        function_start += 1
        file_content.insert(function_start, f'}}\n')
        function_start += 1

    ### Saving the modified text file
    new_file_name = 'Arduino template modified.txt'
    with open(new_file_name, 'w') as new_file:
        new_file.writelines(file_content)

### Complete
    print('Complete.')