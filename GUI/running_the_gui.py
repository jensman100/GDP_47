import tkinter as tk
import os

from main_gui import Main_GUI
from first_gui import FirstWindow
from create_activity_gui import ActivityGenerator


''' This script creates a GUI which helps the user create an activity to add to the mission cycle.

To do:

Import activity button
'''

# Importing libraries

# Get location where file is being run
current_dir = os.path.dirname(os.path.realpath(__file__))
activity_dir = os.path.join(current_dir, 'Activities')
FMC_dir = os.path.join(current_dir, 'Flight_Mission_Cycles')

# Test if activities folder exists
if not os.path.exists(activity_dir):
    print('Activities folder not found. Creating activities folder.')
    os.mkdir(activity_dir)

# Test if Flight Mission Cycles folder exists
if not os.path.exists(FMC_dir):
    print('Flight Mission Cycles folder not found. Creating Flight Mission Cycles folder.')
    os.mkdir(FMC_dir)


# ### Call the GUI class
# app = main_GUI(current_dir)


action = 'first'
run_loop = True

while run_loop:
    if action == 'first':
        try:
            action = FirstWindow().get_result()
        except:
            run_loop = False

    elif action == 'activity':
        action = ActivityGenerator(current_dir).get_result()

    elif action == 'FMC':
        try:
            action = Main_GUI(current_dir).get_result()
        except:
            action = 'first'


    elif action == 'cpp':
        print('Not yet implemented')
        action = 'first'
        ### Need to add the C++ GUI here

    else:
        run_loop = False
        print('Exiting program')
        break
