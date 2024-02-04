''' The is used to create a script to control the implant testing rig
    1. First it reads an excel file containing steps for a 'mission flight cycle'.
    2. Next excel data is converted to force and rotation values.
    3. Finally a templatecode is converted run the flight mission cycle for an arduino.
'''

### Importing Libraries
import pandas as pd
import numpy as np

### Reading Excel File
file_location = r'C:\Users\joeh2\OneDrive - University of Southampton\Documents\Southampton\GDP\General - Small Joint Implant Testing Rig\11 - Code\GDP_47\Flight_Mission_Cycle.xlsx'
df_fms = pd.read_excel(file_location, sheet_name='Flight Mission Cycle')
df_settings = pd.read_excel(file_location, sheet_name='Settings')

print(df_fms)