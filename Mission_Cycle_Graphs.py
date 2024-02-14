''' This script reads an excel file and creates a timeline, a force time graph and a degree time graph. 
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
'''
### Importing functions
from Functions_for_Mission_Cycle_Graphs import *

### Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

### Reading the flight mission cycle sheet
print('Reading excel file...')
file_location = r'C:\Users\joeh2\OneDrive - University of Southampton\Documents\Southampton\GDP\General - Small Joint Implant Testing Rig\11 - Code\GDP_47\Flight_Mission_Cycle.xlsx'
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

settings = list(mission_cycle['Setting']) # Gathering setting names

### Plotting mission cycle timeline
error = plot_timeline(mission_cycle)
if error:
    exit()

### Plotting setting graphs
for setting in settings:
    print(f'Processing {setting} settings...')
    if setting in excel.sheet_names:
        # Reading setting sheet
        df = read_setting(file_location, setting)
        df, error = prepare_setting(df)

        if not error:
            # Creating figure plot with mosaic
            fig, axs = plt.subplot_mosaic('''   aaa
                                                bbc''', figsize=(10, 8))
            # a for force time graph, b for degree time graph, c for angle visual

            fig.suptitle(f'{setting} settings', fontsize = 20) # adding title

            plot_force_vs_time(df, axs['a'])
            plot_degree_vs_time(df, axs['b'])
            plot_angle_visual(df, axs['c'])
        else:
            print(f'ERROR: {setting} not processed due to error(s). See error message(s) above')
    else:
        print(f'Warning: {setting} sheet not found')

plt.show()