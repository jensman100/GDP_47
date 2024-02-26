''' This script reads a template text file and inserts content from the flight mission cycle excel. 
    The text file is saved with a modified name.
    For Python 3.12.1 64-bit. 
    Author: Joe Hensman
'''

import pandas as pd

### Extracting information from the template text file
file_name = 'Arduino template.txt'
with open(file_name, 'r') as file:
    file_content = file.readlines()
### Reading the flight mission cycle excel
mission_cycle_file_name = 'Flight_Mission_Cycle.xlsx'
flight_mission_cycle = pd.read_excel(mission_cycle_file_name, sheet_name='Flight Mission Cycle', index_col=0)

# Extracting the settings
settings = list(flight_mission_cycle.index)

### Mofiying the text file
# Updating the first lane to state that the file has been modified
file_content[1] = 'This file has been modified\n'

# Updating variables
# Finding where the variables start
variable_1_location = file_content.index('key_variable = \n')
variable_2_location = file_content.index('key_variable_2 = \n')

# Updating the variables
file_content[variable_1_location] = 'key_variable = 100\n'
file_content[variable_2_location] = 'key_variable_2 = 200\n'

# Inserting main script
# Finding where the mission cycle starts
mission_cycle_start = file_content.index('// Add mission cycle here\n')
activity_start = mission_cycle_start + 1

# Inserting the mission cycle
for activity in flight_mission_cycle.iterrows():
    count = 0
    while count < activity[1]['No. of cycles']:
        file_content.insert(activity_start + count, f'{activity[0]}()\n')
        count += 1
    
    activity_start += activity[1]['No. of cycles']

### Saving the modified text file
new_file_name = 'Arduino template modified.txt'
with open(new_file_name, 'w') as new_file:
    new_file.writelines(file_content)

print('Complete')