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
df_writing.insert(0, 'initial', [np.NaN, 0, 0])
df_writing.loc['start_time'] = df_writing.loc['Duration'].cumsum()
df_writing = df_writing.transpose()
print(df_writing)

### Plotting the Force vs Time Graph
plt.plot(df_writing['start_time'], df_writing['Force_End'])
plt.xlabel('Time')
plt.ylabel('Force')
plt.title('Force vs Time')
plt.show()