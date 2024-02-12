''' This script reads an excel file and creates a degree time graph for the chosen activity 'Writing'. 
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
'''

### Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Joe's location
file_location = r'C:\Users\joeh2\OneDrive - University of Southampton\Documents\Southampton\GDP\General - Small Joint Implant Testing Rig\11 - Code\GDP_47\Flight_Mission_Cycle.xlsx'
### Henry's location
# file_location = r'D:\OneDrive - University of Southampton\Part 4\FEEG6013 - GDP\Electronics\GDP_47\GDP_47\Flight_Mission_Cycle.xlsx'

### Reading the Excel File
df_writing = pd.read_excel(file_location, sheet_name='Writing', header=None, index_col=0)
df_writing.insert(0, 'initial', [np.NaN, 0, 0, 0, 0, 0])
df_writing.loc['end_time'] = df_writing.loc['Duration'].cumsum()
df_writing = df_writing.transpose()

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
    print('Warning: Period does not divide total time.')

# Create points to plot
amplitude = [max_rom, min_rom] * n_saws
amplitude.insert(0, 0)

num_elements = len(amplitude)
time = list(np.linspace(period/4, total_time + period/4, num_elements-1))
time.insert(0, 0)

# Plot the graph
plt.plot(time, amplitude)
plt.title('Range of Motion - Angle vs Time')
plt.ylabel('Set Angle (Deg)')
plt.xlabel('Time (s)')
plt.show()