''' This script reads an excel file and creates a degree time graph for the chosen activity 'Writing'. 
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
df_writing = pd.read_excel(file_location, sheet_name='Writing', header=None, index_col=0)
df_writing.loc['end_time'] = df_writing.loc['Duration'].cumsum()
df_writing = df_writing.transpose()

### Get the parameters for the triangle wave
max_rom = df_writing['Max_RoM'][1]
min_rom = df_writing['Min_RoM'][1]
period = df_writing['Period'][1]

# Calculate the total time
total_time = list(df_writing['end_time'])[-1]

# Number of saws
n_saws = int(total_time/period)
remainder = total_time % period
if remainder> 0:
    print('Warning: Period does not divide total time.')

### Initial Plotting
fig, axs = plt.subplots(1, 2)
fig.suptitle('Range of Motion summary')

### Plotting Angle vs Time
# Create points to plot
amplitude = [max_rom, min_rom] * n_saws
amplitude.insert(0, 0)

num_elements = len(amplitude)
time = list(np.linspace(period/4, total_time + period/4, num_elements-1))
time.insert(0, 0)

# Plot the graph
axs[0].plot(time, amplitude)
axs[0].set_title('Range of Motion - Angle vs Time')
axs[0].set_ylabel('Set Angle (Deg)')
axs[0].set_xlabel('Time (s)')

### Plotting Angle Visual
# Convert angles to radians
start_angle_rad = np.deg2rad(min_rom)
end_angle_rad = np.deg2rad(max_rom)

# Create the arc
arc_colour = 'blue'
arc = patches.Arc((0, 0), 2, 2, angle = 90, theta1=-max_rom, theta2=-min_rom, linewidth = 5, color = arc_colour)

start_coordx, start_coordy = np.sin(start_angle_rad), np.cos(start_angle_rad)
end_coordx, end_coordy = (np.sin(end_angle_rad), np.cos(end_angle_rad))

axs[1].add_patch(arc)
axs[1].set_ylim(-1.1, 1.1)
axs[1].set_xlim(-1.1, 1.1)

# Create the arrows
# Calculate the direction of the arrows
dx_start = -0.1 * np.cos(start_angle_rad)
dy_start = 0.1 * np.sin(start_angle_rad)
dx_end = 0.1 * np.cos(end_angle_rad)
dy_end = -0.1 * np.sin(end_angle_rad)

arrow_start = patches.FancyArrow(start_coordx, start_coordy, dx_start, dy_start, width=0.05, color = arc_colour)
arrow_end = patches.FancyArrow(end_coordx, end_coordy, dx_end, dy_end, width=0.05, color = arc_colour)
axs[1].add_patch(arrow_start)
axs[1].add_patch(arrow_end)

# Adding labels
axs[1].text(start_coordx - 0.5, start_coordy, f'{min_rom:.0f}°')
axs[1].text(end_coordx - 0.5, end_coordy, f'{max_rom:.0f}°')
# Final graph settings
axs[1].axis('off')
axs[1].set_aspect('equal')
axs[1].set_title('Range of Motion - Angle Visual')


### Showing plot
plt.show()