''' This script creates a GUI which helps the user create an activity to add to the mission cycle.
'''

# Importing libraries
import os

from Main_Menu import Main_Menu
from Create_Mission_Cycle import Create_Mission_Cycle
from Create_Activity import Create_Activity
from Create_CPP_File import Create_CPP_File
from Running_mission_cycle import run_mission_cycle

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


action = 'first'
run_loop = True

while run_loop:
    if action == 'first':
        try:
            action = Main_Menu().get_next_action()
        except:
            run_loop = False

    elif action == 'activity':
        try:
            action = Create_Activity(current_dir).get_next_action()
        except:
            action = 'first'

    elif action == 'FMC':
        try:
            action = Create_Mission_Cycle(current_dir).get_next_action()
        except:
            action = 'first'

    elif action == 'cpp':
        try:
            action = Create_CPP_File(current_dir).get_next_action()
        except:
            action = 'first'

    elif action =='run_mission_cycle':
        try:
            action = run_mission_cycle(current_dir)
        except:
            action = 'first'

    else:
        run_loop = False
        print('Exiting program')
        break
