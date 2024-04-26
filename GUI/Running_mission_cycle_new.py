''' This code is for running the small joint implant tests. After establishing a connection with the Arduino,
the code will run through the list of activities stored in the mission cycle. During each activity the code will show
the percentage of the activity that has been completed. The code will also display information on the force, rom and temperature
'''

# Importing the necessary libraries
import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
import serial

from running_mission_cycle_gui_new import RunningFlightMissionCycle
import time

def run_mission_cycle(code_location):
    # Get list of mission cycles
    try:
        mission_cycles = os.listdir(code_location + '/Flight_Mission_Cycles')
        print('Getting list of mission cycles in {}'.format(code_location + '/Flight_Mission_Cycles'))
        if len(mission_cycles) == 0:
            print('No mission cycles found')
            return('first')
    except FileNotFoundError:
        print('Flight_Mission_Cycles folder not found')
        return('first')

    # Dispaying the start up GUI
    print('Displaying GUI')
    class StartUpGUI():
        def __init__(self):
            self.selection = None

            self.master = tk.Tk()
            self.master.title('Running the mission cycle')
            self.master.geometry('300x100')

            self.title = tk.Label(self.master, text='Please select the mission cycle you would like to run')
            self.title.grid(row=0, column=0, columnspan=2)

            # Create drop down list of mission cycles
            self.selected_mission_cycle = tk.StringVar()
            self.selected_mission_cycle.set('Please select a mission cycle')
            self.mission_cycle_menu = tk.OptionMenu(self.master, self.selected_mission_cycle, *mission_cycles)
            self.mission_cycle_menu.grid(row=1, column=0, columnspan=2)

            # Confirm button
            self.confirm_button = tk.Button(self.master, text='Confirm', command=self.confirm, width=10)  # Set width to 10
            self.confirm_button.grid(row=2, column=0)

            # Cancel button
            self.cancel_button = tk.Button(self.master, text='Cancel', command=self.cancel, width=10)  # Set width to 10
            self.cancel_button.grid(row=2, column=1)

            self.master.mainloop()

        def confirm(self):
            selection = self.selected_mission_cycle.get()
            if selection == 'Please select a mission cycle':
                print('Please select a mission cycle')
            else:
                print('Selected mission cycle: {}'.format(selection))
                self.selection = selection
                self.master.destroy()

        def cancel(self):
            print('Exiting program')
            self.master.destroy()
            return('first')

        def find_selection(self):
            return self.selection
        
    class GetCom():
        def __init__(self):
            self.selection = None

            self.master = tk.Tk()
            self.master.title('Establishing connection with Arduino')
            self.master.geometry('400x150')

            self.title = tk.Label(self.master, text='Please connect the arduino the the PC.') 
            self.title.grid(row=0, column=0, columnspan=2)

            self.blank = tk.Label(self.master, text='')
            self.blank.grid(row=1, column=0, columnspan=2)

            self.title = tk.Label(self.master, text='When connected, please select the COM port the Arduino is connected to')
            self.title.grid(row=2, column=0, columnspan=2)

            # Create a drop down list of COM ports
            self.comp_ports = ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10']
            self.selected_com = tk.StringVar()
            self.selected_com.set('Please select a COM port')
            self.com_menu = tk.OptionMenu(self.master, self.selected_com, *self.comp_ports)
            self.com_menu.grid(row=3, column=0, columnspan=2)

            # Confirm button
            self.confirm_button = tk.Button(self.master, text='Confirm', command=self.confirm, width=10)  # Set width to 10
            self.confirm_button.grid(row=4, column=0)

            # Cancel button
            self.cancel_button = tk.Button(self.master, text='Cancel', command=self.cancel, width=10)
            self.cancel_button.grid(row=4, column=1)

            self.master.mainloop()

        def confirm(self):
            selection = self.selected_com.get()
            if selection == 'Please select a COM port':
                print('Please select a COM port')
            else:
                print('Selected COM port: {}'.format(selection))
                self.selection = selection
                self.master.destroy()

        def cancel(self):
            print('Exiting program')
            self.master.destroy()
            return('first')
        
        def confirm_com(self):
            return self.selection


    selection = StartUpGUI().find_selection()
    if selection == 'first':
        return('first')

    # Read the selected mission cycle
    file_location = os.path.join(code_location, 'Flight_Mission_Cycles', selection)
    try:
        df = pd.read_excel(file_location, sheet_name='Activities')
        PC_activities = df['Activities'].tolist()
    except:
        print('Error reading the selected mission cycle')
        return('first')
    
    correct_com = False
    # Create a window with a drop down list of difference coms
    while correct_com == False:
        com = GetCom().confirm_com()
        # Establishing a connection with the Arduino
        try:
            ser = serial.Serial(com, 9600)
            correct_com = True
            print('Connected to the Arduino')
        except:
            messagebox.showerror(message='Error connecting to the Arduino')

    success = False
    while not success:
        start_time = time.time()
        while ser.in_waiting == 0:
            if time.time() - start_time > 10:
                print('Timeout occurred')
                return('first')
        data = ser.readline().decode().strip()
        print(data)
        if data == 'Arduino running, computer respond?':
            ser.write(b'Computer respond')
            print('Connection established')
            success = True
        else:
            print('Data received: {}'.format(data))

    # Collect information on the activities stored on the arduino
    data = ser.readline().decode().strip()
    arduino_activities = data.split(', ')

    missing_activities = []
    for activity in PC_activities:
        if activity not in arduino_activities:
            if activity not in missing_activities:
                missing_activities.append(activity)

    if len(missing_activities) > 0:
        messagebox.showerror(message='Warning {} not found in mission cycle file. Terminating'.format(missing_activities))
        return('first')

    # Confirmation to start the test
    result = messagebox.askokcancel(message='Connection established. Do you want to initiate the test?')

    # if not result:
    #     return()

    # Running the mission cycle
    app = RunningFlightMissionCycle(PC_activities, ser)
    messagebox.showinfo(message='Mission cycle completed')
    return('first')

if '__name__' == '__main__':
    code_location = os.path.dirname(os.path.realpath(__file__))
    next = run_mission_cycle(code_location)