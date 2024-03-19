import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV file and store it as a dataframe
df = pd.read_csv('cross_facing_green_down.csv')

# Remove the first row of the dataframe and store
calibration = df.loc[0, 'Weight (N)']
df = df.iloc[1:]

# Time is input in format 'YYYY-MM-DD HH:MM:SS', change this so the first time is 0 and the rest are in seconds and milliseconds
# The milliseconds are calculated if the time before has the same second so the next will be second + 0.5 seconds
# The time is stored in a new column called 'Time (s)'
df['Time (s)'] = float(0)
first_time_value = (df.loc[1, 'Time']).split(' ')[1]
first_time_split = first_time_value.split(':')
first_time_float = [float(i) for i in first_time_split]
first_time = first_time_float[0] * 3600 + first_time_float[1] * 60 + first_time_float[2]

previous_time = np.nan

for i in range(1, len(df)+1):
    time_value = (df.loc[i, 'Time']).split(' ')[1]
    time_split = time_value.split(':')
    time_split_float = [float(i) for i in time_split]
    time = time_split_float[0] * 3600 + time_split_float[1] * 60 + time_split_float[2]
    time = time - first_time
    if time == previous_time:
        time = time + 0.5
    df.loc[i, 'Time (s)'] = time
    previous_time = time

# Print the dataframe
plt.plot(df['Time (s)'], df['Weight (N)'])
plt.title('Weight vs Time', fontsize=16)
plt.xlabel('Time (s)', fontsize=14)
plt.ylabel('Weight (N)', fontsize=14)
plt.show()