''' This script reads an excel file and creates a timeline, a force time graph and a degree time graph for the chosen activity 'Writing'. 
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
'''

### Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

### Joe's location
file_location = r'C:\Users\joeh2\OneDrive - University of Southampton\Documents\Southampton\GDP\General - Small Joint Implant Testing Rig\11 - Code\GDP_47\Flight_Mission_Cycle.xlsx'
### Henry's location
# file_location = r'D:\OneDrive - University of Southampton\Part 4\FEEG6013 - GDP\Electronics\GDP_47\GDP_47\Flight_Mission_Cycle.xlsx'

### Reading the Excel File
# Settings sheet
df_settings = pd.read_excel(file_location, sheet_name='Flight Mission Cycle')
df_settings['end_time'] = df_settings['Duration'].cumsum()

# Writing sheet
df_writing = pd.read_excel(file_location, sheet_name='Writing', header=None, index_col=0)
df_writing.loc['end_time'] = df_writing.loc['Duration'].cumsum()
df_writing = df_writing.transpose()

### Checking data
if list(df_writing['Force'])[0] > 0 or list(df_writing['Force'])[0] < 0:
    print('Warning: Force is not zero at the start of the activity. Please check the data.')
if list(df_writing['Force'])[-1] > 0 or list(df_writing['Force'])[-1] < 0:
    print('Warning: Force is not zero at the end of the activity. Please check the data.')
if list(df_writing['Duration'])[0] > 0 or list(df_writing['Duration'])[0] < 0:
    print('Warning: Duration is not zero at the start of the activity. Please check the data.')

### Creating figure plot with mosaic
fig, axs = plt.subplot_mosaic('''   aaa
                                    bbb
                                    ccd''', figsize=(10, 8))

# a for timeline, b for force time graph, c for degree time graph, d for angle representation

fig.suptitle('Flight Mission Cycle', fontsize = 20) # adding title

### Plotting Timeline
axs['a'].set_ylim([-0.5, 2])            # setting y limits

axs['a'].set_yticks([])                 # removing y ticks
for spine in axs['a'].spines.values():  # Remove the box around the outside of the plot
    spine.set_visible(False)
axs['a'].set_xlim([-10, list(df_settings['end_time'])[-1] + 10]) # setting x limits
axs['a'].set_title('Timeline') # adding title
axs['a'].set_xlabel('Time (minutes)') # adding x label

# Changing the size of the subplot
pos = axs['a'].get_position()           # Get the current position of the subplot
new_height = pos.height / 2             # Change this value to adjust the height
axs['a'].set_position([pos.x0, pos.y0 + new_height, pos.width, new_height]) # Set the new position of the subplot

# Plot each event as a colored section
for index, event in df_settings.iterrows():
    end_time = event['end_time']
    duration = event['Duration']
    setting = event['Setting']
    center = end_time - duration/2
    axs['a'].barh(y=0, height=1, width=duration, left=end_time-duration, edgecolor='black', label = setting)
    axs['a'].text(center, 0, setting, ha='center', va='center', color='black')

### Plotting the Force vs Time Graph
axs['b'].plot(df_writing['end_time'], df_writing['Force'])
axs['b'].set_xlabel('Time')
axs['b'].set_ylabel('Force')
axs['b'].set_title('Force vs Time')

# Changing the size of the subplot
pos = axs['b'].get_position()           # Get the current position of the subplot
axs['b'].set_position([pos.x0, pos.y0 + new_height/2, pos.width, pos.height]) # Set the new position of the subplot

### Plotting the Degree vs Time Graph
# Get the parameters for the triangle wave
max_rom = df_writing['Max_RoM'][1]
min_rom = df_writing['Min_RoM'][1]
period = df_writing['Period'][1]

# Calculate the total time
total_time = list(df_writing['end_time'])[-1]

# Number of saws
n_saws = int(total_time/period)
remainder = total_time % period
if remainder> 0:
    print('Warning: Period does not divide total time. Please check the data.')

# Plotting Angle vs Time
amplitude = [max_rom, min_rom] * n_saws # Create points to plot
amplitude.insert(0, 0)

num_elements = len(amplitude)
time = list(np.linspace(period/4, total_time + period/4, num_elements-1))
time.insert(0, 0)

# Making sure the angle ends at 0
if time[-1] > 0 or time[-1] < 0:
    time.pop()              # Remove the last element from time
    amplitude.pop()
    time.append(total_time)
    amplitude.append(0)

# Plot the graph
axs['c'].plot(time, amplitude)
axs['c'].set_title('Angle vs Time')
axs['c'].set_ylabel('Set Angle (Deg)')
axs['c'].set_xlabel('Time (s)')

### Plotting Angle Visual
# Create the arc
start_angle_rad = np.deg2rad(min_rom) # Convert angles to radians
end_angle_rad = np.deg2rad(max_rom)

arc_colour = 'blue'
arc = patches.Arc((0, 0), 2, 2, angle = 90, theta1=-max_rom, theta2=-min_rom, linewidth = 5, color = arc_colour)

start_coordx, start_coordy = np.sin(start_angle_rad), np.cos(start_angle_rad)
end_coordx, end_coordy = (np.sin(end_angle_rad), np.cos(end_angle_rad))

axs['d'].add_patch(arc)
axs['d'].set_ylim(-1.1, 1.1)
axs['d'].set_xlim(-1.1, 1.1)

# Create the arrows
dx_start = -0.1 * np.cos(start_angle_rad) # Setting the direction of the arrows
dy_start = 0.1 * np.sin(start_angle_rad)
dx_end = 0.1 * np.cos(end_angle_rad)
dy_end = -0.1 * np.sin(end_angle_rad)

arrow_start = patches.FancyArrow(start_coordx, start_coordy, dx_start, dy_start, width=0.06, color = arc_colour)
arrow_end = patches.FancyArrow(end_coordx, end_coordy, dx_end, dy_end, width=0.06, color = arc_colour)
axs['d'].add_patch(arrow_start) # Plotting arrows
axs['d'].add_patch(arrow_end)

# Adding labels
axs['d'].text(start_coordx - 0.5, start_coordy, f'{min_rom:.0f}°')
axs['d'].text(end_coordx - 0.4, end_coordy - 0.2, f'{max_rom:.0f}°')

# Final graph settings
axs['d'].axis('off')
axs['d'].set_aspect('equal')
axs['d'].set_title('Angle Visual')

### Show the plot
plt.show()
