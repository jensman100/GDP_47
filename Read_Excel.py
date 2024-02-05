''' The is used to create a script to control the implant testing rig
    1. First it reads an excel file containing steps for a 'mission flight cycle'.
    2. Next excel data is converted to force and rotation values.
    3. Finally a templatecode is converted run the flight mission cycle for an arduino.
'''

### Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Reading Excel File
file_location = r'C:\Users\joeh2\OneDrive - University of Southampton\Documents\Southampton\GDP\General - Small Joint Implant Testing Rig\11 - Code\GDP_47\Flight_Mission_Cycle.xlsx'
df_fms = pd.read_excel(file_location, sheet_name='Flight Mission Cycle')
df_settings = pd.read_excel(file_location, sheet_name='Settings')

### Plotting Timeline
# Calculating Start Times
df_fms['start_time'] = 0
for i in range(1, len(df_fms)):
    df_fms['start_time'][i] = df_fms['start_time'][i-1] + df_fms['Duration'][i-1]

# Create a figure and axis
fig, ax = plt.subplots()

ax.set_ylim([-2, 2])
ax.set_yticks([])

ax.set_xlim([-10, df_fms['start_time'].iloc[-1] + df_fms['Duration'].iloc[-1]+10])

ax.set_title('Timeline of Flight Mission Cycle')
ax.set_xlabel('Time (minutes)')

# Plot each event as a colored section
for index, event in df_fms.iterrows():
    start_time = event['start_time']
    duration = event['Duration']
    setting = event['Setting']
    center = start_time + duration/2
    ax.barh(y=0, height=1, width=duration, left=start_time, edgecolor='black', label = setting)
    ax.text(center, 0, setting, ha='center', va='center', color='black')

plt.show()