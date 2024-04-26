''' This file is called from the other GUIS. It contains a class used to generate a C++ file from previously made mission cycles.
    1. Read mission cycle, if not one added then need to add one, if one then double check
    2. Extract information from mission cycle and turn into raw data
    3. Write raw data to C++ file
'''

import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Create_CPP_File():
    def __init__(self, current_dir, mission_cycle = None):
        # find where the script is being run from

        self.mission_cycle = mission_cycle
        self.next_action = 'first'
        self.current_dir = current_dir
        self.cancel = False
        self.move_on = False
        self.display_mission_cycle = False

        while not self.move_on:
            if self.cancel:

                return

            if self.mission_cycle == None: # If no mission cycle added
                print('No mission cycle added')
                
                # Look in mission cycle folder for mission cycles
                try:
                    mission_cycles = os.listdir('Flight_Mission_Cycles')
                except:
                    print('Flight mission cycle not found')
                    messagebox.showerror('Error', 'Mission cycle folder not found. Please create a mission cycle first.')
                    return
                
                if len(mission_cycles) == 0:
                    print('No mission cycles found')
                    messagebox.showerror('Error', 'No mission cycles found. Please create a mission cycle first.')
                    return
                
                # If mission cycles found then ask user to select one
                self.window = tk.Tk()
                self.window.title('Select Mission Cycle')
                self.window.geometry('400x150')
                self.window.maxsize(400, 150)
                self.window.minsize(400, 150)
                self.window.configure(bg='#ADD8E6')

                self.label = tk.Label(self.window, text='Please select a mission cycle from the list below:')
                self.label.configure(bg='#ADD8E6', height=2, width=50)
                self.label.place(relx=0.5, rely=0.2, anchor='center')

                self.selection = tk.StringVar()
                self.selection.set('Click here to view mission cycle')
                self.selection_menu = tk.OptionMenu(self.window, self.selection, *mission_cycles)
                self.selection_menu.configure(bg='#ADD8E6', height=1, width=50)
                self.selection_menu.place(relx=0.5, rely=0.4, anchor='center')

                self.select_button = tk.Button(self.window, text='Select', command=self.select)
                self.select_button.configure(bg='#ADD8E6', height=2, width=10)
                self.select_button.place(relx=0.3, rely=0.8, anchor='center')

                self.go_back_button = tk.Button(self.window, text='Cancel', command=self.go_back)
                self.go_back_button.configure(bg='#ADD8E6', height=2, width=10)
                self.go_back_button.place(relx=0.7, rely=0.8, anchor='center')

                self.window.mainloop()
                if not self.mission_cycle == None:
                    self.double_check_mission_cycle()

            else:
                # If mission cycle added then check if it is correct
                print('Mission cycle added')
                print(f'Mission cycle: {self.mission_cycle}')

                # Look in mission cycle folder for mission cycles
                try:
                    mission_cycles = os.listdir('Flight_Mission_Cycles')
                except:
                    print('Flight mission cycle not found')
                    messagebox.showerror('Error', 'Mission cycle folder not found. Please create a mission cycle first.')
                    return
                
                if self.mission_cycle not in mission_cycles:
                    print('Mission cycle not found')
                    messagebox.showerror('Error', 'Mission cycle not found. Please create a mission cycle first.')
                    return
                
                self.double_check_mission_cycle()

            if self.display_mission_cycle:
                # Extract information from mission cycle
                # Read mission cycle excel file
                print('Reading Mission Cycle')
                try:
                    activities_df = pd.read_excel(f'Flight_Mission_Cycles/{self.mission_cycle}', sheet_name='Activities')
                    settings_df = pd.read_excel(f'Flight_Mission_Cycles/{self.mission_cycle}', sheet_name='Settings', index_col=0)
                except:
                    print('Error reading mission cycle')
                    messagebox.showerror('Error', 'Error reading mission cycle. Please try again')
                    return

                print('Preparing Mission Cycle')
                raw_activities = {}
                for index, row in settings_df.iterrows():
                    times, angles = self.create_waveform(row['ROM Min'], row['ROM Max'], row['Duration'])
                    times, forces = self.create_waveform(row['Force Min'], row['Force Max'], row['Duration'], times)
                    
                    angle_multiples = [angle//1.8 for angle in angles]

                    # get a list of the times the multiple changes compared to previous value
                    angle_changes = [True]
                    for count, multiple in enumerate(angle_multiples):
                        if count == 0:
                            continue
                        if multiple != angle_multiples[count - 1]:
                            angle_changes.append(True)
                        else:
                            angle_changes.append(False)
                    
                    # get a list of the times the force changes compared to previous value
                    force_changes = [True]
                    for count, force in enumerate(forces):
                        if count == 0:
                            continue
                        if force != forces[count - 1]:
                            force_changes.append(True)
                        else:
                            force_changes.append(False)

                    force_times = []
                    angle_times = []
                    force_values = []
                    angle_values = []
                    angle_change = []
                    delay = []

                    last_time = times[-1]
                    last_angle = angle_multiples[-1]

                    # remove row if both angle and force are the same as previous row
                    for count in reversed(range(len(times))):
                        if count == 0:
                            force_times.append(times[count])
                            force_values.append(forces[count])
                            angle_times.append(times[count])
                            angle_values.append(angle_multiples[count])
                            angle_change.append(last_angle - angle_multiples[count])
                            delay.append(last_time - times[count])

                        if not angle_changes[count] and forces[count] == forces[count - 1]:
                            times = np.delete(times, count)
                            angles = np.delete(angles, count)
                            forces = np.delete(forces, count)
                            angle_multiples.pop(count)
                            angle_changes.pop(count)
                            force_changes.pop(count)
                        
                        elif not angle_changes[count]:
                            force_times.append(times[count])
                            force_values.append(forces[count])
                            delay.append(last_time - times[count])
                            last_time = times[count]

                        else:
                            force_times.append(times[count])
                            force_values.append(forces[count])
                            angle_times.append(times[count])
                            angle_values.append(angle_multiples[count])
                            angle_change.append(last_angle - angle_multiples[count])
                            delay.append(last_time - times[count])
                            last_time = times[count]
                            last_angle = angle_multiples[count]                   

                    force_times.reverse()
                    force_values.reverse()
                    angle_times.reverse()
                    angle_values.reverse()
                    angle_change.reverse()
                    delay.reverse()

                    raw_activities[index] = [times, force_times, force_values, angle_times, angle_values, angle_change, delay]

                last_end_time = 0

                activities = list(activities_df['Activities'])
                forces = []
                angles = []
                all_timings = []
                angle_timings = []
                force_timings = []
                list_of_activities_and_timings = [] # In format {activity: [start_time, end_time]}

                for activity in activities:
                    forces.extend(raw_activities[activity][2])
                    angles.extend(multiple * 1.8 for multiple in raw_activities[activity][4])

                    all_timings.extend(time + last_end_time for time in raw_activities[activity][0])
                    angle_timings.extend(time + last_end_time for time in raw_activities[activity][3])
                    force_timings.extend(time + last_end_time for time in raw_activities[activity][1])
                    list_of_activities_and_timings.append([activity, last_end_time, all_timings[-1]])
                    last_end_time = all_timings[-1]

                # add the final angle time and angle to the list
                angle_timings.append(all_timings[-1])
                angles.append(angles[-1])

                # Creating figure
                fig, axs = plt.subplot_mosaic('''a
                                    b
                                    c''', figsize=(10, 8))
                
                # Plotting summary of mission cycle
                axs['a'].set_ylim([-0.5, 1])            # setting y limits
                axs['a'].set_yticks([])                 # removing y ticks
                for spine in axs['a'].spines.values():  # Remove the box around the outside of the plot
                    spine.set_visible(False)
                axs['a'].set_xlim([-1, all_timings[-1] + 1])  # setting x limits
                # axs.set_title('Timeline')  # adding title
                axs['a'].set_xlabel('Time (seconds)', fontsize = 15) # adding x label
                axs['a'].tick_params(axis='x', labelsize=15)

                # Plot each event as a colored section
                for activity_settings in list_of_activities_and_timings:
                    activity = activity_settings[0]
                    start_time = activity_settings[1]
                    duration = activity_settings[2] - start_time
                    center = start_time + duration/2
                    axs['a'].barh(y=0, height=1, width=duration, left=start_time, edgecolor='black', label = activity)
                    axs['a'].text(center, 0, activity, ha='center', va='center', color='black', fontsize = 15)

                axs['a'].set_title('Summary Mission Cycle', fontsize = 20)

                # Plotting force and angle
                axs['b'].plot(force_timings, forces)
                axs['b'].set_title('Force', fontsize = 20)
                axs['b'].set_xlabel('Time (seconds)', fontsize = 15)
                axs['b'].set_ylabel('Force (N)', fontsize = 15)

                axs['c'].plot(angle_timings, angles)
                axs['c'].set_title('Angle', fontsize = 20)
                axs['c'].set_xlabel('Time (seconds)', fontsize = 15)
                axs['c'].set_ylabel('Angle (degrees)', fontsize = 15)
                
                print('Displaying Mission Cycle')
                plt.tight_layout()
                plt.show(block=False)
                
                print('Has the mission cycle loaded correctly?')
                
                # Create a tkinter window
                self.new_window = tk.Tk()
                self.new_window.configure(bg='#ADD8E6')  # Set background color to #ADD8E6

                # Create a label to display the mission cycle confirmation message
                label = tk.Label(self.new_window, text="Is the mission cycle correct?", font=("Arial", 20), bg='#ADD8E6', fg='white')
                label.pack(pady=20)

                # Create yes, no, and cancel buttons
                button_frame = tk.Frame(self.new_window, bg='#ADD8E6')
                button_frame.pack(pady=20)

                yes_button = tk.Button(button_frame, text="Yes", command=self.yes_window, font=("Arial", 16), bg='white', fg='#ADD8E6', padx=20, pady=10)
                yes_button.pack(side=tk.LEFT, padx=10)

                no_button = tk.Button(button_frame, text="No", command=self.no_window, font=("Arial", 16), bg='white', fg='#ADD8E6', padx=20, pady=10)
                no_button.pack(side=tk.LEFT, padx=10)

                self.output = None

                self.new_window.mainloop()

                
                if self.output == None:
                    print('Cancelled')
                    self.cancel = True
                    plt.close('all')

                elif self.output:
                    print('Yes. Mission cycle correct')
                    self.move_on = True
                    plt.close('all')

                else:
                    print('No. Mission cycle incorrect')
                    self.mission_cycle = None
                    plt.close('all')

        # Write raw data to C++ file
        print('Writing to C++ file')
        # Try to open blank mission cycle
        try:
            # look for blacnk_mission_cycle.txt in foler called cpp_mission_cycles
            blank_mission_cycle = os.path.join(self.current_dir, 'cpp_mission_cycles', 'blank_mission_cycle.txt')
            with open(blank_mission_cycle, 'r') as file:
                file_content = file.readlines()
        except:
            print('Error opening blank mission cycle')
            messagebox.showerror('Error', 'Could not find "blank_mission_cycle.txt" in the folder "cpp_mission_cycles". Please try again')
            self.cancel = True
            return

        print('Successfully opened blank mission cycle')

        # Adding Mission Cycle Activity
        activity_list_start = file_content.index('// ADD LIST OF ACTIVITIES\n') + 1
        activity_string = 'String activities = "' + ', '.join(settings_df.index) + '";\n'
        file_content.insert(activity_list_start, activity_string)
        # Adding Switch Values
        switch_start = file_content.index('// ADD SWITCH VALUES HERE\n') + 1
        
        for count, setting in enumerate(settings_df.index, 2):
            file_content.insert(switch_start, f'else if (instruction.equals("{setting}")){{\n')
            file_content.insert(switch_start + 1, f'  activity = {count};\n')
            file_content.insert(switch_start + 2, f'}}\n')
            switch_start += 3

        # Adding Switch Cases
        switch_start = file_content.index('// ADD SWITCH CASES HERE\n') + 1
        for count, setting in enumerate(settings_df.index, 2):
            file_content.insert(switch_start, f'case {count}:\n')
            file_content.insert(switch_start + 1, f'  {setting}();\n')
            file_content.insert(switch_start + 2, f'  break;\n')
            switch_start += 3

        # Adding Functions
        function_start = file_content.index('// ADD ACTIVITY FUNCTIONS HERE\n') + 1
        for activity in settings_df.index:
            last_time = 0
            file_content.insert(function_start, f'void {activity}(){{\n')
            function_start += 1

            # Set the angle to the desired angle
            file_content.insert(function_start, f'  turn_steps({raw_activities[activity][4][0]});\n')
            function_start += 1
            file_content.insert(function_start, f'  delay(100);\n')
            function_start += 1
            # raw_activities[index] = [times, force_times, force_values, angle_times, angle_values, angle_change, delay]

            for count, time in enumerate(raw_activities[activity][1]):

                if time in raw_activities[activity][3]:
                    angle = raw_activities[activity][5][raw_activities[activity][3].index(time)]
                    file_content.insert(function_start, f'  turn_steps({angle});\n')
                    function_start += 1
                    delay = raw_activities[activity][6][count] - 10
                else:
                    delay = raw_activities[activity][6][count]

                force = raw_activities[activity][2][count]
                file_content.insert(function_start, f'  set_load({force:.0f}, {int(delay*1000)});\n')
                function_start += 1

            # Return angle to 0
            file_content.insert(function_start, f'  turn_steps({-(raw_activities[activity][4][0])});\n')
            function_start += 1
            file_content.insert(function_start, f'  delay(100);\n')
            function_start += 1

            # Write back to PC
            file_content.insert(function_start, '  Serial.println("Activity Complete");\n')
            function_start += 1
            file_content.insert(function_start, '}\n')
            function_start += 1
        
        # Saving the modified file as a c++ file
        file_name = self.mission_cycle.split('.')[0]
        folder_location = os.path.join(self.current_dir, 'cpp_mission_cycles', f'{file_name}')
        try:
            os.makedirs(folder_location)
        except:
            pass
        file_location = os.path.join(folder_location, f'{file_name}.ino')
        with open(file_location, 'w') as file:
            file.writelines(file_content)
        print('Successfully written to C++ file')
        messagebox.showinfo('Success', 'Successfully written to C++ file')
        self.go_back()

    def yes_window(self):
        self.new_window.destroy()
        self.output = True
    
    def no_window(self):
        self.new_window.destroy()
        self.output = False

    def get_next_action(self):
        return self.next_action
        
    def select(self):
        # extract string from self.selection
        selection = self.selection.get()
        if selection == 'Click here to view mission cycle':
            print('No mission cycle selected, try again')
            messagebox.showerror('Error', 'Please select a mission cycle')
            return
        else:
            print(f'Mission cycle selected: {selection}')
            self.window.destroy()
            self.mission_cycle = selection

    def yes(self):
        self.window.destroy()
        self.display_mission_cycle = True
        print('Proceeding with generating C++ file')

    def no(self):
        self.window.destroy()
        self.mission_cycle = None
        self.move_on = False
        self.display_mission_cycle = False

    def double_check_mission_cycle(self):
        # Confirm that the mission cycle is correct with user
        self.window = tk.Tk()
        self.window.title('Confirm Mission Cycle')
        self.window.geometry('400x150')
        self.window.maxsize(400, 150)
        self.window.minsize(400, 150)
        self.window.configure(bg='#ADD8E6')

        self.label = tk.Label(self.window, text=f'The mission cycle chosen is {self.mission_cycle} \n Proceed?')
        self.label.configure(bg='#ADD8E6', height=2, width=50)
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.yes_button = tk.Button(self.window, text='Yes', command=self.yes)
        self.yes_button.configure(bg='#ADD8E6', height=2, width=10)
        self.yes_button.place(relx=0.3, rely=0.7, anchor='center')

        self.no_button = tk.Button(self.window, text='No', command=self.no)
        self.no_button.configure(bg='#ADD8E6', height=2, width=10)
        self.no_button.place(relx=0.7, rely=0.7, anchor='center')

        self.window.mainloop()

    def go_back(self):
        try:
            self.window.destroy()
        except:
            pass
        self.cancel = True

    def create_waveform(self, min, max, duration, time = None):
        '''
        This function creates raw from min and max amplitudes and the period
        '''
        if time is None:
            time = np.linspace(0, duration, 50)

        amplitude = (max - min)/2
        y_offset = (max + min)/2
        if max < 0 or min > 0 or amplitude == 0:
            x_offset = 0
        else:
            x_offset =np.arcsin(-y_offset/amplitude)
        wave = amplitude * np.sin(2 * np.pi * time/duration + x_offset) + y_offset
        return time, wave
