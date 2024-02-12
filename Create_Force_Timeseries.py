''' This script reads an excel file and creates a force time graph for the chosen activity 'Writing'. 
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
df_writing.loc['start_time'] = df_writing.loc['Duration'].cumsum()
df_writing = df_writing.transpose()

### Checking data
if list(df_writing['Force'])[0] > 0 or list(df_writing['Force'])[0] < 0:
    print('Warning: Force is not zero at the start of the activity. Please check the data.')
if list(df_writing['Force'])[-1] > 0 or list(df_writing['Force'])[-1] < 0:
    print('Warning: Force is not zero at the end of the activity. Please check the data.')

### Plotting the Force vs Time Graph
plt.plot(df_writing['start_time'], df_writing['Force'])
plt.xlabel('Time')
plt.ylabel('Force')
plt.title('Force vs Time')
plt.show()