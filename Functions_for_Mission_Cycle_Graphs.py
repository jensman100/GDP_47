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
    df = pd.read_excel(file_location, sheet_name=f'{sheet_name}', header=None, index_col=0)
    return df

def prepare_setting(df):
    ''' This function takes a dataframe, calculates the end time of forces and transposes the dataframe.
        Then checks for warnings.
        '''
    # Calculating end tim
    df.loc['end_time'] = df.loc['Duration'].cumsum()
    df= df.transpose()

    # Checking for warnings
    error = False
    if list(df['Force'])[0] > 0 or list(df['Force'])[0] < 0:                                        # If force is not zero at the start
        print('Warning: Force is not zero at the start of the activity. Please check the data.')
    if list(df['Force'])[-1] > 0 or list(df['Force'])[-1] < 0:                                      # If force is not zero at the end
        print('Warning: Force is not zero at the end of the activity. Please check the data.')
    if list(df['Duration'])[0] > 0 or list(df['Duration'])[0] < 0:                                  # If duration is not zero at the start
        print('Warning: Duration is not zero at the start of the activity. Please check the data.')
    
    if len(list(df['Force'])) < 2:                                                                  # If there are less than 2 data points
        print('ERROR: Less than 2 force data points. Please check the data.')
        error = True
    if df['Force'].isna().sum() != df['Duration'].isna().sum():                                         # If force and duration are not the same length
        print('ERROR: Force and Duration are not the same length. Please check the data.')
        error = True
    if np.isnan(list(df['Force'])[0]):                                                                  # If there is no data in the force column
        print('ERROR: No data in the force column. Please check the data.')
        error = True
    if np.isnan(list(df['Duration'])[0]):                                                               # If there is no data in the duration column
        print('ERROR: No data in the duration column. Please check the data.')
        error = True
    if np.isnan(list(df['Max_RoM'])[0]):                                                               # If no Max_RoM value is entered
        print('ERROR: No Max_RoM entered. Please check the data.')
        error = True
    if np.isnan(list(df['Min_RoM'])[0]):                                                               # If no Min_RoM value is entered
        print('ERROR: No Min_RoM entered. Please check the data.')
        error = True
    if np.isnan(list(df['Period'])[0]):                                                             # If no Period value is entered
        print('ERROR: No Period entered. Please check the data.')
        error = True
    else:
        if list(df['Period'])[0] <= 0:                                                                # If period is 0 or less
            print('ERROR: Period is 0 or less. Please check the data.')
            error = True
                                                              
    
    if not error:                                      
        if list(df['Max_RoM'])[0] < list(df['Min_RoM'])[0]:                                         # If Max RoM is less than Min RoM
            wrong_max_rom = list(df['Max_RoM'])[0]
            df.loc[1, 'Max_RoM'] = list(df['Min_RoM'])[0]
            df.loc[1, 'Min_RoM'] = wrong_max_rom
            print('Warning: Max RoM was less than Min RoM. Data has been changed.')
    
    return df, error

def plot_force_vs_time(df, axs):
    ''' This function takes a dataframe and plots the force vs time on a given axis.
        '''
    end_time = list(df['end_time'])
    force= list(df['Force'])
    axs.plot(end_time, force)
    axs.set_xlabel('Time')
    axs.set_ylabel('Force')
    axs.set_title('Force vs Time')
    return force, end_time
    
def calcualte_roms_and_periods(df):
    ''' This function takes a dataframe and calculates the max and min RoM and the period of the activity.
        '''
    max_rom = df['Max_RoM'][1]
    min_rom = df['Min_RoM'][1]
    period = df['Period'][1]
    return max_rom, min_rom, period
    

def plot_degree_vs_time(df, axs):
    ''' This function takes a dataframe and plots the degree vs time on a given axis.
        '''

    max_rom, min_rom, period = calcualte_roms_and_periods(df)

    # Calculate the total time
    total_time = list(df['end_time'])[-1]

    # Number of saws
    n_saws = int(total_time/period)
    remainder = total_time % period
    if remainder> 0:
        print('ERROR: Period does not divide total time. Please check the data.')

    # Plotting Angle vs Time
    amplitude = [max_rom, min_rom] * n_saws # Create points to plot
    amplitude.append(0) # Add the final point
    amplitude.insert(0, 0) # Add the first point

    if max_rom == min_rom:
        max_fraction_through = 0.5
    else:
        max_fraction_through = abs(max_rom/(max_rom - min_rom))

    time = [0, max_fraction_through * period/2, max_fraction_through * period/2 + period/2] # Create time points
    count = 1
    while count < n_saws:
        time += [x + period for x in time[-2:]]
        count += 1
    time.append(total_time)

    # Plot the graph
    axs.plot(time, amplitude)
    axs.set_title('Angle vs Time')
    axs.set_ylabel('Set Angle (Deg)')
    axs.set_xlabel('Time (s)')

    return amplitude, time

def plot_angle_visual(df, axs):
    ''' This function takes a dataframe and plots the angle vs time on a given axis.
        '''
    
    max_rom, min_rom, period = calcualte_roms_and_periods(df)
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

    # Final graph settings
    axs.axis('off')
    axs.set_aspect('equal')
    axs.set_title('Angle Visual')

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
        axs.text(center, 0, f'{key}', ha='center', va='center', color='black', fontsize = 20)

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