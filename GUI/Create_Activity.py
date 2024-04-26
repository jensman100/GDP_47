import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import pandas as pd
import numpy as np

''' This script creates a GUI which helps the user create an activity to add to the mission cycle.
    The inputs required are the activity name, the duration of the activity, and the frequency and amplitudes of the force and ROM waveforms.
    The output is an excel spreadsheet which contains the activity information.
'''

### Importing libraries
import matplotlib.pyplot as plt

class Create_Activity():
    def __init__(self, current_dir):
        print('Opening Activity Generator')

        self.what_next = 'first'

        self.root = tk.Tk()
        self.root.bind('<Destroy>', self.close_plot)
        self.root.title("Activity Generator")
        self.current_dir = current_dir

        activity_label = ttk.Label(self.root, text="Activity Name:")
        activity_label.grid(row=0, column=0, padx=10, pady=10)
        self.activity_entry = ttk.Entry(self.root)
        self.activity_entry.insert(0, "Enter activity name")  # Instruction for activity name
        self.activity_entry.bind("<FocusIn>", lambda event: self.activity_entry.delete(0, tk.END) if self.activity_entry.get() == "Enter activity name" else None)  # Remove instruction on click
        self.activity_entry.bind("<FocusOut>", lambda event: self.activity_entry.insert(0, "Enter activity name") if self.activity_entry.get() == "" else None)  # Re-insert instruction if input is blank
        self.activity_entry.grid(row=0, column=1, padx=10, pady=10)

        # Duration
        duration_label = ttk.Label(self.root, text="Duration (s):")
        duration_label.grid(row=1, column=0, padx=10, pady=10)
        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.insert(0, "Enter duration")  # Instruction for duration
        self.duration_entry.bind("<FocusIn>", lambda event: self.duration_entry.delete(0, tk.END) if self.duration_entry.get() == "Enter duration" else None)  # Remove instruction on click
        self.duration_entry.bind("<FocusOut>", lambda event: self.duration_entry.insert(0, "Enter duration") if self.duration_entry.get() == "" else None)  # Re-insert instruction if input is blank
        self.duration_entry.grid(row=1, column=1, padx=10, pady=10)

        # Force Max
        force_max_label = ttk.Label(self.root, text="Force Max (N):")
        force_max_label.grid(row=2, column=0, padx=10, pady=10)
        self.force_max_entry = ttk.Entry(self.root)
        self.force_max_entry.insert(0, "Enter force max")  # Instruction for force max
        self.force_max_entry.bind("<FocusIn>", lambda event: self.force_max_entry.delete(0, tk.END) if self.force_max_entry.get() == "Enter force max" else None)  # Remove instruction on click
        self.force_max_entry.bind("<FocusOut>", lambda event: self.force_max_entry.insert(0, "Enter force max") if self.force_max_entry.get() == "" else None)  # Re-insert instruction if input is blank
        self.force_max_entry.grid(row=2, column=1, padx=10, pady=10)

        # Force Min
        force_min_label = ttk.Label(self.root, text="Force Min (N):")
        force_min_label.grid(row=3, column=0, padx=10, pady=10)
        self.force_min_entry = ttk.Entry(self.root)
        self.force_min_entry.insert(0, "Enter force min")  # Instruction for force min
        self.force_min_entry.bind("<FocusIn>", lambda event: self.force_min_entry.delete(0, tk.END) if self.force_min_entry.get() == "Enter force min" else None)  # Remove instruction on click
        self.force_min_entry.bind("<FocusOut>", lambda event: self.force_min_entry.insert(0, "Enter force min") if self.force_min_entry.get() == "" else None)  # Re-insert instruction if input is blank
        self.force_min_entry.grid(row=3, column=1, padx=10, pady=10)

        # Force phase difference
        force_phase_label = ttk.Label(self.root, text="Phase Difference (°):")
        force_phase_label.grid(row=4, column=0, padx=10, pady=10)
        self.force_phase_entry = ttk.Entry(self.root)
        self.force_phase_entry.insert(0, "Enter phase difference")
        self.force_phase_entry.bind("<FocusIn>", lambda event: self.force_phase_entry.delete(0, tk.END) if self.force_phase_entry.get() == "Enter force phase difference" else None)
        self.force_phase_entry.bind("<FocusOut>", lambda event: self.force_phase_entry.insert(0, "Enter phase difference") if self.force_phase_entry.get() == "" else None)
        self.force_phase_entry.grid(row=4, column=1, padx=10, pady=10)

        # ROM Max
        rom_max_label = ttk.Label(self.root, text="ROM Max (°):")
        rom_max_label.grid(row=5, column=0, padx=10, pady=10)
        self.rom_max_entry = ttk.Entry(self.root)
        self.rom_max_entry.insert(0, "Enter ROM max")  # Instruction for ROM max
        self.rom_max_entry.bind("<FocusIn>", lambda event: self.rom_max_entry.delete(0, tk.END) if self.rom_max_entry.get() == "Enter ROM max" else None)  # Remove instruction on click
        self.rom_max_entry.bind("<FocusOut>", lambda event: self.rom_max_entry.insert(0, "Enter ROM max") if self.rom_max_entry.get() == "" else None)  # Re-insert instruction if input is blank
        self.rom_max_entry.grid(row=5, column=1, padx=10, pady=10)

        # ROM Min
        rom_min_label = ttk.Label(self.root, text="ROM Min (°):")
        rom_min_label.grid(row=6, column=0, padx=10, pady=10)
        self.rom_min_entry = ttk.Entry(self.root)
        self.rom_min_entry.insert(0, "Enter ROM min")  # Instruction for ROM min
        self.rom_min_entry.bind("<FocusIn>", lambda event: self.rom_min_entry.delete(0, tk.END) if self.rom_min_entry.get() == "Enter ROM min" else None)  # Remove instruction on click
        self.rom_min_entry.bind("<FocusOut>", lambda event: self.rom_min_entry.insert(0, "Enter ROM min") if self.rom_min_entry.get() == "" else None)  # Re-insert instruction if input is blank
        self.rom_min_entry.grid(row=6, column=1, padx=10, pady=10)

        # Submit Button
        view_button = ttk.Button(self.root, text="View", command=self.view)
        view_button.grid(row=8, column=0, padx=10, pady=10)

        # Default Button
        import_button = ttk.Button(self.root, text="Read Activity", command=self.import_activity)
        import_button.grid(row=8, column=1, padx=10, pady=10)

        confirm_button = ttk.Button(self.root, text="Confirm", command=self.confirm)
        confirm_button.grid(row=8, column=2, padx=10, pady=10)

        close_button = ttk.Button(self.root, text="Back", command=self.close)
        close_button.grid(row=8, column=3, padx=10, pady=10)

        self.root.mainloop()

    def test(self):

        try:
            duration = float(self.duration_entry.get())
            force_max = float(self.force_max_entry.get())
            force_min = float(self.force_min_entry.get())
            force_phase = float(self.force_phase_entry.get())
            rom_max = float(self.rom_max_entry.get())
            rom_min = float(self.rom_min_entry.get())
        except:
            messagebox.showerror("Error", "Please enter numbers for the duration, force and ROM values")
            return None, None, None, None, None, None

        if duration <= 0:
            messagebox.showerror("Error", "Duration must be greater than 0")
            return None, None, None, None, None, None
        
        if force_max < 0 or force_min < 0:
            messagebox.showerror("Error", "Force values must be positive")
            return None, None, None, None, None, None
        
        return duration, force_max, force_min, force_phase, rom_max, rom_min

    def view(self):
        self.activity_name = self.activity_entry.get()
        print(f'Displaying {self.activity_name} with current settings')

        # Close the last graph created
        plt.close('all')

        # Check that inputs are floats
        duration, force_max, force_min, force_phase, rom_max, rom_min = self.test()

        if duration is None:
            return
        
        # Create waveforms
        time, angle = self.create_waveform(rom_min, rom_max, duration)
        time, force = self.create_waveform(force_min, force_max, duration, time, force_phase)

        self.create_force_rom_plot(self.activity_name, time, force, angle)

    def confirm_import(self):
        activity_selected = self.activity_var.get()
        if activity_selected == 'Please select an activity from the list':
            messagebox.showerror("Error", "Please select an activity from the list")
            return
        self.activity_name = activity_selected
        self.import_activity_window.destroy()
        self.activity_name, duration, force_max, force_min, rom_max, rom_min, time, angle, force = self.read_activity(self.activity_name)
        if self.activity_name is None:
            return
        else:
            self.activity_entry.delete(0, tk.END)
            self.activity_entry.insert(0, self.activity_name)
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, duration)
            self.force_max_entry.delete(0, tk.END)
            self.force_max_entry.insert(0, force_max)
            self.force_min_entry.delete(0, tk.END)
            self.force_min_entry.insert(0, force_min)
            self.rom_max_entry.delete(0, tk.END)
            self.rom_max_entry.insert(0, rom_max)
            self.rom_min_entry.delete(0, tk.END)
            self.rom_min_entry.insert(0, rom_min)
            print(f'{self.activity_name} has been inputted successfully')


            return

    def import_activity(self):
        # Create a new window with a dropdown list of activities stored in the activities folder

        # Get the list of activities
        activity_folder_path = os.path.join(self.current_dir, 'Activities')
        activities = os.listdir(activity_folder_path)
        activities = [activity.split('.')[0] for activity in activities]

        if len(activities) == 0:
            messagebox.showerror("Error", "No activities found. Please create an activity first.")
            return

        # Create a new window
        self.import_activity_window = tk.Toplevel(self.root)
        self.import_activity_window.grab_set()
        self.import_activity_window.title("Import Activity")
        self.import_activity_window.geometry("300x200")

        # Create a label
        label = ttk.Label(self.import_activity_window, text="Select an activity to import:")
        label.pack(pady=10)

        # Create a dropdown list
        self.activity_var = tk.StringVar(self.import_activity_window)
        self.activity_var.set('Please select an activity from the list')  # Set the default option
        dropdown = tk.OptionMenu(self.import_activity_window, self.activity_var, *activities)
        dropdown.pack(pady=10)

        # Create a button to confirm the selection
        confirm_button = ttk.Button(self.import_activity_window, text="Confirm", command=self.confirm_import)
        confirm_button.pack(pady=10)

        # Create a back button
        back_button = ttk.Button(self.import_activity_window, text="Cancel", command=self.import_activity_window.destroy)
        back_button.pack(pady=10)

        self.import_activity_window.mainloop()

    def confirm(self):
        print('Attempting to Save Activity to Excel')
        # Check that inputs are floats
        duration, force_max, force_min, force_phase, rom_max, rom_min = self.test()

        if duration is None:
            return

        # Remove spaces from activity name and replace with _
        self.activity_name = self.activity_entry.get()
        self.activity_name = self.activity_name.replace(' ', '_')

        # Save to excel named self.activity_name.xlsx
        # See if the file already exists
        folder_path = os.path.join(self.current_dir, 'Activities')
        file_path = os.path.join(folder_path, self.activity_name + '.xlsx')

        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            print('Activities folder does not exist. Creating folder')
            os.makedirs(folder_path)

        try:
            df = pd.read_excel(file_path)
            print('Overwrite?')
            overwrite = messagebox.askyesno("File Exists", "The file already exists. Do you want to overwrite it?")
            if not overwrite:
                print(' No. Confirm Cancelled')
                return
            else:
                print(' Yes. Overwriting File')
        except:
            pass

        # Save the key inputs to a sheet in the excel file named settings
        settings = pd.DataFrame({'Activity Name': [self.activity_name],
                                 'Duration': [duration],
                                 'Force Max': [force_max],
                                 'Force Min': [force_min],
                                 'Force Phase': [force_phase],
                                 'ROM Max': [rom_max],
                                 'ROM Min': [rom_min]})

        # Save the waveforms to a sheet in the excel file named waveforms
        time, angle = self.create_waveform(rom_min, rom_max, duration)
        time, force = self.create_waveform(force_min, force_max, duration, time)

        waveforms = pd.DataFrame({'Time': time, 'Angle': angle, 'Force': force})

        with pd.ExcelWriter(file_path) as writer:
            settings.to_excel(writer, sheet_name='settings', index=False)
            waveforms.to_excel(writer, sheet_name='waveforms', index=False)

        messagebox.showinfo("Success", f"{self.activity_name} has been saved to " + file_path)
        print('Activity Successfully Saved to Excel')
        exit = messagebox.askyesno("Exit", "Do you want to exit the program?")

        if exit:
            self.close()
            return

    def close(self):
        print('Clsoing Activity Generator')
        self.root.destroy()
        self.what_next = 'first'
        plt.close('all')

    def create_waveform(self, min, max, duration, time = None, phase = 0):
        '''
        This function creates raw from min and max amplitudes and the period
        '''
        if time is None:
            time = np.linspace(0, duration, 30)

        amplitude = (max - min)/2
        y_offset = (max + min)/2
        if max < 0 or min > 0 or amplitude == 0:
            x_offset = 0
        else:
            x_offset =np.arcsin(-y_offset/amplitude)
        wave = amplitude * np.sin(2 * np.pi * time/duration + x_offset - phase/180 * np.pi) + y_offset
        return time, wave
    
    def create_force_rom_plot(self, activity_name, time, force, angle):
        ''' This function creates a plot of the force and ROM waveforms for a given activity from raw time data
        
        '''
        # Create plot
        plt.figure()  # Create a new figure
        # Set suptitle
        plt.suptitle(self.activity_name)

        # Plot Force
        plt.subplot(2, 1, 1)
        plt.plot(time, force)
        plt.xlabel('Time (s)')
        plt.ylabel('Force (N)')
        plt.title('Force')
        plt.tight_layout()  # Add this line to adjust the spacing between subplots

        # Plot ROM
        plt.subplot(2, 1, 2)
        plt.plot(time, angle)
        plt.xlabel('Time (s)')
        plt.ylabel('Angle (degrees)')
        plt.title('ROM')
        plt.tight_layout()  # Add this line to adjust the spacing between subplots

        # Show plot
        plt.show()

    def get_next_action(self):
        return self.what_next
    
    def read_activity(self, activity):
        ''' This function reads an activity stored in an excel file within the activity folder.
            The activity settings are stored in a sheet called 'settings' and the columns are:
            - Activity Name
            - Duration
            - Force Max
            - Force Min
            - Force Phase
            - ROM Max
            - ROM Min

            The raw data is stored in a sheet called 'waveforms' and the columns are:
            - Time
            - Angle
            - Force
    '''
        # Read the settings
        code_path = os.getcwd()
        activity_folder_path = os.path.join(code_path, 'Activities')
        activity_file_name = os.path.join(activity_folder_path, activity + '.xlsx')
        try:
            settings = pd.read_excel(activity_file_name, sheet_name='settings')
            print('File read successfully.')
        except:
            print('Unable to read the file. Check the file name and whether the file is open.')
            return None, None, None, None, None, None, None, None, None
        
        self.activity_name = settings['Activity Name'][0]
        duration = settings['Duration'][0]
        force_max = settings['Force Max'][0]
        force_min = settings['Force Min'][0]
        force_phase = settings['Force Phase'][0]
        rom_max = settings['ROM Max'][0]
        rom_min = settings['ROM Min'][0]

        # Read the waveforms
        waveforms = pd.read_excel(activity_file_name, sheet_name='waveforms')
        time = waveforms['Time']
        angle = waveforms['Angle']
        force = waveforms['Force']

        return self.activity_name, duration, force_max, force_min, force_phase, rom_max, rom_min, time, angle, force
    
    def close_plot(self, event):
        try:
            plt.close('all')
        except:
            pass