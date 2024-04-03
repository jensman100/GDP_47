''' This script contains all functions from Mission_Cycle_Graphs.py
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
    '''

### Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def read_mission_cycle(file_location):
    ''' Reads a sheet named Flight Mission Cycle and returns a pandas dataframe with setting end times.
        '''
    df = pd.read_excel(file_location, sheet_name='Flight Mission Cycle', index_col=0)
    return df

def plot_timeline(df):
    ''' This function takes a dataframe and plots a timeline of the mission cycle.
        '''
    if len(df['Duration']) > 0:
        error = False
        plt.figure(figsize=(10, 3))
        plt.ylim([-0.5, 1])            # setting y limits
        plt.yticks([])                 # removing y ticks
        for spine in plt.gca().spines.values():  # Remove the box around the outside of the plot
            spine.set_visible(False)
        plt.xlim([-10, list(df['setting_end_time'])[-1] + 10]) # setting x limits
        plt.title('Timeline') # adding title
        plt.xlabel('Time (minutes)') # adding x label
        plt.subplots_adjust(top=0.6, bottom=0.3) # Adjusting the plot size

        # Plot each event as a colored section
        for index, event in df.iterrows():
            end_time = event['setting_end_time']
            duration = event['Duration']
            setting = event['Setting']
            center = end_time - duration/2
            plt.barh(y=0, height=1, width=duration, left=end_time-duration, edgecolor='black', label = setting)
            plt.text(center, 0, setting, ha='center', va='center', color='black')
    else:
        print('ERROR: No data in the mission cycle sheet. Please check the data.')
        error = True
    return error

def read_setting(file_location, sheet_name):
    ''' Reads in a specific sheet from an excel file and returns a pandas dataframe
        '''
    df = pd.read_excel(file_location, sheet_name=f'{sheet_name}', header=0, index_col=0)
    return df

def prepare_setting(df):
    ''' This function takes a dataframe, calculates the end time of forces and transposes the dataframe.
        Then checks for warnings.
        '''
    force_settings = ['set_points', 'angle_dependent']
    rom_settings = ['triangle', 'sinosoidal']

    # Checking for warnings
    error = False
    if df.loc['Force', 'Type'] not in force_settings:                                                # If force type is not set_points or angle_dependent
        print('ERROR: Force type is not correct. Please check the data.')
        error = True
    if df.loc['RoM', 'Type'] not in rom_settings:                                                    # If RoM type is not triangle or sinusoidal
        print('ERROR: RoM type is not correct. Please check the data.')
        error = True
    force_type = df.loc['Force', 'Type']
    if force_type == 'set_points':
        if list(df.loc['Force'])[1] > 0 or list(df.loc['Force'])[1] < 0:                                        # If force is not zero at the start
            print('Warning: Force is not zero at the start of the activity. Please check the data.')
        if list(df.loc['Force'])[-1] > 0 or list(df.loc['Force'])[-1] < 0:                                      # If force is not zero at the end
            print('Warning: Force is not zero at the end of the activity. Please check the data.')
        if list(df.loc['Duration'])[1] > 0 or list(df.loc['Duration'])[1] < 0:                                  # If duration is not zero at the start
            print('Warning: Duration is not zero at the start of the activity. Please check the data.')

        if len(list(df.loc['Force'])) < 2:                                                                  # If there are less than 2 data points
            print('ERROR: Less than 2 force data points. Please check the data.')
            error = True
        if df.loc['Force'].isna().sum() != df.loc['Duration'].isna().sum() -1:                                         # If force and duration are not the same length
            print('ERROR: Force and Duration are not the same length. Please check the data.')
            error = True
        if np.isnan(list(df.loc['Force'])[1]):                                                                  # If there is no data in the force column
            print('ERROR: No data in the force column. Please check the data.')
            error = True
        if np.isnan(list(df.loc['Duration'])[1]):                                                               # If there is no data in the duration column
            print('ERROR: No data in the duration column. Please check the data.')
            error = True
                                                          
    if np.isnan(list(df.loc['Max_RoM'])[1]):                                                               # If no Max_RoM value is entered
        print('ERROR: No Max_RoM entered. Please check the data.')
        error = True
    if np.isnan(list(df.loc['Min_RoM'])[1]):                                                               # If no Min_RoM value is entered
        print('ERROR: No Min_RoM entered. Please check the data.')
        error = True
        
    if np.isnan(list(df.loc['Period'])[1]):                                                             # If no Period value is entered
        print('ERROR: No Period entered. Please check the data.')
        error = True
    else:
        if list(df.loc['Period'])[0] <= 0:                                                                # If period is 0 or less
            print('ERROR: Period is 0 or less. Please check the data.')
            error = True
                                                              
    if not error:                                                                                      
        if list(df.loc['Max_RoM'])[1] < list(df.loc['Min_RoM'])[1] and df.loc['RoM', 'Type'] == 'triangle':                                         # If Max RoM is less than Min RoM
            wrong_max_rom = list(df.iloc['Max_RoM'])[1]
            df.loc[1, 'Max_RoM'] = list(df.loc['Min_RoM'])[1]
            df.loc[1, 'Min_RoM'] = wrong_max_rom
            print('Warning: Max RoM was less than Min RoM. Data has been changed.')
        
        # Calculating end time
        df.loc['end_time'] = df.loc['Duration'].cumsum()
    df= df.transpose()
    
    return df, error

def plot_force_vs_time(df, axs, plot, angle, time):
    ''' This function takes a dataframe and plots the force vs time on a given axis.
        '''
    force_setting = df.loc['Type', 'Force']
    # If force type is set_points
    if force_setting == 'set_points':
        force = list(df['Force'])[1:]
        end_time = list(df['end_time'])[1:]
        saved_end_time = []
        saved_force = []
        total_time = end_time[-1]-end_time[0]

        for i in range(len(end_time)-1):
            interval_time = end_time[i+1] - end_time[i]
            num_points = int(len(angle) * interval_time / total_time)
            current_end_time = np.linspace(end_time[i], end_time[i+1], num_points)
            current_force = np.linspace(force[i], force[i+1], num_points)
            saved_end_time.extend(current_end_time.tolist())
            saved_force.extend(current_force.tolist())

        # If there are any remaining points due to rounding, add them to the last interval
        remaining_points = len(angle) - len(saved_end_time)
        if remaining_points > 0:
            last_end_time = np.linspace(end_time[-1], end_time[-1], remaining_points)
            last_force = np.linspace(force[-1], force[-1], remaining_points)
            saved_end_time.extend(last_end_time.tolist())
            saved_force.extend(last_force.tolist())

        end_time = saved_end_time
        force = saved_force

    elif force_setting == 'angle_dependent':
        angle_instruction = list(df['Force'])[1]
        operator = angle_instruction[0]
        angle_causing_change = float(angle_instruction[1:])
        force = np.zeros(len(time))
        set_force = list(df['Force'])[2]
        if operator == '>':
            for i in range(len(time)):
                if angle[i] > angle_causing_change:
                    force[i] = set_force
        if operator == '<':
            for i in range(len(time)):
                if angle[i] < angle_causing_change:
                    force[i] = set_force
            
    if plot:
        axs.plot(time, force)
        axs.set_xlabel('Time')
        axs.set_ylabel('Force')
        axs.set_title('Force vs Time')

    return list(force)
    
def calcualte_roms_and_periods(df):
    ''' This function takes a dataframe and calculates the max and min RoM and the period of the activity.
        '''
    max_rom = df.loc['Unnamed: 2', 'Max_RoM']
    min_rom = df.loc['Unnamed: 2', 'Min_RoM']
    period = df.loc['Unnamed: 2', 'Period']
    if df.loc['Type', 'Force'] == 'set_points':
        total_time = list(df['end_time'])[-1]
    elif df.loc['Type', 'Force'] == 'angle_dependent':
        total_time = df.loc['Unnamed: 2', 'end_time']
    return max_rom, min_rom, period, total_time
    

def plot_degree_vs_time(df, axs, plot):
    ''' This function takes a dataframe and plots the degree vs time on a given axis.
        '''
    max_rom, min_rom, period, total_time = calcualte_roms_and_periods(df)

    if df.loc['Type', 'RoM'] == 'triangle':
        angle, time = triangle_angle(0, max_rom, min_rom, period, total_time)
    elif df.loc['Type', 'RoM'] == 'sinosoidal':
        angle, time = sinonisoidal_angle(0, max_rom, min_rom, period, total_time)
    else:
        print('ERROR: RoM type not recognised. Please check the data.')
        exit()

    if plot:
        # Plot the graph
        axs.plot(time, angle)
        axs.set_title('Angle vs Time')
        axs.set_ylabel('Set Angle (Deg)')
        axs.set_xlabel('Time (s)')
    return list(angle), list(time)

def triangle_angle(time, max_rom, min_rom, period, total_time):
            # Number of saws
        n_saws = int(total_time/period)
        remainder = total_time % period
        if remainder> 0:
            print('ERROR: Period does not divide total time. Please check the data.')

        # Plotting Angle vs Time
        if min_rom > 0:
            intial_angle = [min_rom, max_rom, min_rom]
            additional_angle = [max_rom, min_rom] * (n_saws -1)
            angle = intial_angle + additional_angle
        elif max_rom < 0:
            intial_angle = [max_rom, min_rom, max_rom]
            additional_angle = [min_rom, max_rom] * (n_saws -1)
            angle = intial_angle + additional_angle
        else:
            angle = [max_rom, min_rom] * n_saws # Create points to plot
            angle.append(0) # Add the final point
            angle.insert(0, 0) # Add the first point

        if max_rom == min_rom:
            max_fraction_through = 0.5
        else:
            max_fraction_through = abs(max_rom/(max_rom - min_rom))
        
        if min_rom > 0 or max_rom < 0:
            time = [0, period/2] # Create time points
        else:
            time = [0, max_fraction_through * period/2, max_fraction_through * period/2 + period/2] # Create time points
        
        count = 1
        while count < n_saws:
            time += [x + period for x in time[-2:]]
            count += 1
        time.append(total_time)

        saved_time = []
        saved_angle = []

        for i in range(len(time)-1):
            saved_time.extend(np.linspace(time[i], time[i+1], num=20))
            saved_angle.extend(np.linspace(angle[i], angle[i+1], num=20))

        return saved_angle, saved_time

def sinonisoidal_angle(time, max_rom, min_rom, period, total_time):
        time = np.linspace(0, total_time, 50)
        amplitude = (max_rom - min_rom)/2
        y_offset = (max_rom + min_rom)/2
        if max_rom < 0 or min_rom > 0 or amplitude == 0:
            x_offset = 0
        else:
            x_offset =np.arcsin(-y_offset/amplitude)
        angle = amplitude * np.sin(2 * np.pi * time/period + x_offset) + y_offset
        return angle, time

def plot_angle_visual(df, axs):
    ''' This function takes a dataframe and plots the angle vs time on a given axis.
        '''
    
    max_rom, min_rom, period, total_time = calcualte_roms_and_periods(df)
    start_angle_rad = np.deg2rad(min_rom) # Convert angles to radians
    end_angle_rad = np.deg2rad(max_rom)

    arc_colour = 'blue'
    arc = patches.Arc((0, 0), 2, 2, angle = 90, theta1=-max_rom, theta2=-min_rom, linewidth = 5, color = arc_colour)

    start_coordx, start_coordy = np.sin(start_angle_rad), np.cos(start_angle_rad)
    end_coordx, end_coordy = (np.sin(end_angle_rad), np.cos(end_angle_rad))

    axs.add_patch(arc)
    axs.set_ylim(-1.1, 1.1)
    axs.set_xlim(-1.1, 1.1)

    # Create the arrows
    dx_start = -0.1 * np.cos(start_angle_rad) # Setting the direction of the arrows
    dy_start = 0.1 * np.sin(start_angle_rad)
    dx_end = 0.1 * np.cos(end_angle_rad)
    dy_end = -0.1 * np.sin(end_angle_rad)

    arrow_start = patches.FancyArrow(start_coordx, start_coordy, dx_start, dy_start, width=0.06, color = arc_colour)
    arrow_end = patches.FancyArrow(end_coordx, end_coordy, dx_end, dy_end, width=0.06, color = arc_colour)
    axs.add_patch(arrow_start) # Plotting arrows
    axs.add_patch(arrow_end)

    # Adding labels
    axs.text(start_coordx - 0.5, start_coordy, f'{min_rom:.0f}°')
    axs.text(end_coordx - 0.4, end_coordy - 0.2, f'{max_rom:.0f}°')
    axs.text(0, 0.2, f'Period = {period:.0f}s', ha = 'center', va = 'center')
    axs.text(0, 0.1, f'Duration = {total_time:.0f}s', ha = 'center', va = 'center')

    # Final graph settings
    axs.axis('off')
    axs.set_aspect('equal')
    axs.set_title('Angle Visual')

def update_mission_cycle_angles(atime, angle, cycles, start_time, angle_history, atime_history, total_time, max_rom_0, min_rom_0):
    length = len(atime) * cycles
    aduration = max(atime)
    updated_atime = [x + start_time for x in atime]

    number_of_changes = len(atime)
    count = 1
    final_avalue = updated_atime[-1]
    while count < cycles:
        updated_atime += [x + final_avalue + (count-1) * aduration for x in atime[-number_of_changes:]]
        count += 1

    updated_angle = angle * cycles
    angle_history += updated_angle
    atime_history += updated_atime

    if max_rom_0:
        atime_history[-length:] = [time + 3 for time in atime_history[-length:]]
        angle_history.insert(-length, 0)
        angle_history.append(0)
        atime_history.insert(-length, start_time)
        atime_history.append(start_time + total_time * cycles + 6)
    
    elif min_rom_0:
        atime_history[-length:] = [time + 3 for time in atime_history[-length:]]
        angle_history.insert(-length, 0)
        angle_history.append(0)
        atime_history.insert(-length, start_time)
        atime_history.append(start_time + total_time * cycles + 6)
    
    return(angle_history, atime_history)

def update_mission_cycle_forces(ftime, force, cycles, start_time, force_history, ftime_history, total_time, max_rom_0, min_rom_0):
    length = len(ftime) * cycles
    fduration = max(ftime)
    duration_with_cycles = fduration * cycles

    force = force * cycles
    
    force_history += force 
    # ftime_history += updated_ftime

    if max_rom_0:
        ftime_history[-length:] = [time + 3 for time in ftime_history[-length:]]
        force_history.insert(-length, 0)
        force_history.append(0)

        duration_with_cycles += 6

    elif min_rom_0:
        ftime_history[-length:] = [time + 3 for time in ftime_history[-length:]]
        force_history.insert(-length, 0)
        force_history.append(0)

        duration_with_cycles += 6
    
    return(force_history, int(duration_with_cycles))

def plot_timeline_dict(timing_dict,  end_time, axs):
    ''' This function takes a dictionary and plots a timeline of the mission cycle.
    {key: [start_time, duration]}
        '''
    axs.set_ylim([-0.5, 1])            # setting y limits
    axs.set_yticks([])                 # removing y ticks
    for spine in axs.spines.values():  # Remove the box around the outside of the plot
        spine.set_visible(False)
    axs.set_xlim([-10, end_time + 10])  # setting x limits
    # axs.set_title('Timeline')  # adding title
    axs.set_xlabel('Time (minutes)', fontsize = 15) # adding x label
    axs.tick_params(axis='x', labelsize=15)

    # Plot each event as a colored section
    for key in timing_dict.keys():
        start_time = timing_dict[key][1]
        duration = timing_dict[key][0]
        center = start_time + duration/2
        axs.barh(y=0, height=1, width=duration, left=start_time, edgecolor='black', label = f'{key}')
        axs.text(center, 0, f'{key}', ha='center', va='center', color='black', fontsize = 15)

def plot_mission_force(time, force, axs):
    axs.plot(time, force, label = 'Force')
    axs.set_title('Force Cycle')
    axs.set_xlabel('Time')
    axs.set_ylabel('Force')
    axs.set_xlim(0)

def plot_mission_angle(time, angle, axs):
    axs.plot(time, angle, label = 'Force')
    axs.set_title('RoM Cycle')
    axs.set_xlabel('Time')
    axs.set_ylabel('Angle (deg)')
    axs.set_xlim(0)

def writing_to_excel(time, force_history, angle_history, timings, excel_file_name):
    # Create new data frame
    values_dict = {'Time': time, 'Force': force_history, 'Angle': angle_history}
    values_df = pd.DataFrame(values_dict)
    values_df = values_df.set_index('Time')

    settings_df = pd.DataFrame(timings)
    settings_df.index = ['Duration', 'Start Time', 'No. of cycles']  # Set header names

    with pd.ExcelWriter(excel_file_name) as excel_writer:
        values_df.to_excel(excel_writer, sheet_name='Values')
        settings_df.to_excel(excel_writer, sheet_name='Settings')

def process_setting(timings, setting, settings_repeats, setting_counts, mission_cycle, df, start_time, force_history, angle_history, ftime_history, atime_history):
    cycles, setting, plot = test_in_settings(settings_repeats, setting, setting_counts, mission_cycle)
    # Test if plotting, if true create an set of axes
    axsb, axsa = test_if_plot(plot, setting, df)
    # Plotting degree time graph
    angle, atime = plot_degree_vs_time(df, axsb, plot)

    # Plotting force time graph
    force, ftime = plot_force_vs_time(df, axsa, plot, angle, atime)

    # Test which side of 0 the max and min RoM are
    max_rom_0, min_rom_0, total_time = test_roms(df)

    # Updating mission cycle with next angle settings
    angle_history, atime_history = update_mission_cycle_angles(atime, angle, cycles, start_time, angle_history, atime_history, total_time, max_rom_0, min_rom_0)

    # Updating mission cycle with next force settings
    force_history, ftime_history, duration_with_cycles = update_mission_cycle_forces(ftime, force, cycles, start_time, force_history, ftime_history, total_time, max_rom_0, min_rom_0)

    timings[setting] = [duration_with_cycles, start_time, cycles]
    start_time += duration_with_cycles
    return angle_history, atime_history, force_history, ftime_history, duration_with_cycles, cycles, timings, start_time

def test_in_settings(settings_repeats, setting, setting_counts, mission_cycle):
    if settings_repeats[setting] > 1 and setting_counts[setting] != 0:
        setting_repeat_no = setting_counts[setting]
        cycles = list(mission_cycle.loc[setting, 'No. of cycles'])[setting_repeat_no]
        setting_counts[setting] += 1
        setting = f'{setting} \n (Repeat{setting_repeat_no})'
        plot = False
    elif settings_repeats[setting] > 1:
        cycles = list(mission_cycle.loc[setting, 'No. of cycles'])[0]
        setting_counts[setting] += 1
        plot = True
    else:
        cycles = mission_cycle.loc[setting, 'No. of cycles']
        setting_counts[setting] += 1
        plot = True
    
    return int(cycles), setting, plot

def test_if_plot(plot, setting, df):
        # Creating figure plot with mosaic
    if plot:
        fig, axs = plt.subplot_mosaic('''   aaa
                                            bbc''', figsize=(10, 8))
        # a for force time graph, b for degree time graph, c for angle visual

        fig.suptitle(f'{setting} settings', fontsize = 20) # adding title
        # Plotting angle visual
        plot_angle_visual(df, axs['c'])
        axsb = axs['b']
        axsa = axs['a']

    else :
        axsb = None
        axsa = None
    return axsb, axsa

def test_roms(df):
    max_rom, min_rom, period, total_time = calcualte_roms_and_periods(df)
    max_rom_0 = False
    min_rom_0 = False
    if max_rom < 0:
        max_rom_0 = True
    if min_rom > 0:
        min_rom_0 = True
    return max_rom_0, min_rom_0, total_time

def mission_cycle_graphs(timings, start_time, time_history, force_history, angle_history):
    ''' This function takes an excel file and processes the mission cycle sheets.
        '''
    fig, axs = plt.subplot_mosaic('''a
                                b
                                c''', figsize=(10, 8))
    fig.suptitle('Flight Mission Cycle', fontsize = 20)
    plot_timeline_dict(timings, start_time, axs['a']) # Inputs are dictionary and final start and duration times
    plot_mission_force(time_history, force_history, axs['b'])
    plot_mission_angle(time_history, angle_history, axs['c'])
    fig.tight_layout()
    print('Displaying Graphs...')
    plt.show()

def previous_mission_cycle_name(settings_repeats, setting_counts, setting):
    if settings_repeats[setting] == 1:
        settings_repeats.pop(setting)
        setting_counts.pop(setting)
        addon = '_0'
    else:
        addon = f'_{settings_repeats[setting]}'
        settings_repeats[setting] -= 1

    fms_name = f'{setting[5:]}'
    fms_file_name = fms_name + '.xlsx'
    return fms_file_name, addon, settings_repeats, setting_counts

def read_previous_mission_cycle(file_name):
    try:
        force_angle_sheet = pd.read_excel(file_name, sheet_name='Values', index_col=None, header=0)
        settings_sheet = pd.read_excel(file_name, sheet_name='Settings', index_col=0, header=0)
        error = False
    except:
        print('ERROR: File cannot be opened. Please check the file location and whether it is open and try again.')
        error = True
        force_angle_sheet = None
        settings_sheet = None

    return force_angle_sheet, settings_sheet, error

def combining_mission_cyles(force_angle_sheet, start_time, settings_sheet, addon, timings, force_history, angle_history, time_history):
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
    return force_history, angle_history, time_history, start_time, timings


def write_to_c(arduino_file_name, timings, arduino_settings):
        # Reading the template text file
    with open(arduino_file_name, 'r') as file:
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