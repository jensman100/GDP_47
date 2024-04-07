''' This script creates a GUI which helps the user create an activity to add to the mission cycle.
    The inputs required are the activity name, the duration of the activity, and the frequency and amplitudes of the force and ROM waveforms.
    The output is an excel spreadsheet which contains the activity information.
'''

### Importing libraries
from Functions_for_GUI import *

from tkinter import messagebox

import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

### Inputs
activity_name = 'Activity 1'
duration = 10

force_max = 30
force_min = -30

ROM_max = 80
ROM_min = -20

### Functions
# Creating GUI
print('Creating GUI')

root = tk.Tk()
root.title("Activity Generator")

# Activity Name
activity_label = ttk.Label(root, text="Activity Name:")
activity_label.grid(row=0, column=0, padx=10, pady=10)
activity_entry = ttk.Entry(root)
activity_entry.insert(0, "Enter activity name")  # Instruction for activity name
activity_entry.bind("<FocusIn>", lambda event: activity_entry.delete(0, tk.END) if activity_entry.get() == "Enter activity name" else None)  # Remove instruction on click
activity_entry.bind("<FocusOut>", lambda event: activity_entry.insert(0, "Enter activity name") if activity_entry.get() == "" else None)  # Re-insert instruction if input is blank
activity_entry.grid(row=0, column=1, padx=10, pady=10)

# Duration
duration_label = ttk.Label(root, text="Duration:")
duration_label.grid(row=1, column=0, padx=10, pady=10)
duration_entry = ttk.Entry(root)
duration_entry.insert(0, "Enter duration")  # Instruction for duration
duration_entry.bind("<FocusIn>", lambda event: duration_entry.delete(0, tk.END) if duration_entry.get() == "Enter duration" else None)  # Remove instruction on click
duration_entry.bind("<FocusOut>", lambda event: duration_entry.insert(0, "Enter duration") if duration_entry.get() == "" else None)  # Re-insert instruction if input is blank
duration_entry.grid(row=1, column=1, padx=10, pady=10)

# Force Max
force_max_label = ttk.Label(root, text="Force Max:")
force_max_label.grid(row=2, column=0, padx=10, pady=10)
force_max_entry = ttk.Entry(root)
force_max_entry.insert(0, "Enter force max")  # Instruction for force max
force_max_entry.bind("<FocusIn>", lambda event: force_max_entry.delete(0, tk.END) if force_max_entry.get() == "Enter force max" else None)  # Remove instruction on click
force_max_entry.bind("<FocusOut>", lambda event: force_max_entry.insert(0, "Enter force max") if force_max_entry.get() == "" else None)  # Re-insert instruction if input is blank
force_max_entry.grid(row=2, column=1, padx=10, pady=10)

# Force Min
force_min_label = ttk.Label(root, text="Force Min:")
force_min_label.grid(row=3, column=0, padx=10, pady=10)
force_min_entry = ttk.Entry(root)
force_min_entry.insert(0, "Enter force min")  # Instruction for force min
force_min_entry.bind("<FocusIn>", lambda event: force_min_entry.delete(0, tk.END) if force_min_entry.get() == "Enter force min" else None)  # Remove instruction on click
force_min_entry.bind("<FocusOut>", lambda event: force_min_entry.insert(0, "Enter force min") if force_min_entry.get() == "" else None)  # Re-insert instruction if input is blank
force_min_entry.grid(row=3, column=1, padx=10, pady=10)

# ROM Max
rom_max_label = ttk.Label(root, text="ROM Max:")
rom_max_label.grid(row=4, column=0, padx=10, pady=10)
rom_max_entry = ttk.Entry(root)
rom_max_entry.insert(0, "Enter ROM max")  # Instruction for ROM max
rom_max_entry.bind("<FocusIn>", lambda event: rom_max_entry.delete(0, tk.END) if rom_max_entry.get() == "Enter ROM max" else None)  # Remove instruction on click
rom_max_entry.bind("<FocusOut>", lambda event: rom_max_entry.insert(0, "Enter ROM max") if rom_max_entry.get() == "" else None)  # Re-insert instruction if input is blank
rom_max_entry.grid(row=4, column=1, padx=10, pady=10)

# ROM Min
rom_min_label = ttk.Label(root, text="ROM Min:")
rom_min_label.grid(row=5, column=0, padx=10, pady=10)
rom_min_entry = ttk.Entry(root)
rom_min_entry.insert(0, "Enter ROM min")  # Instruction for ROM min
rom_min_entry.bind("<FocusIn>", lambda event: rom_min_entry.delete(0, tk.END) if rom_min_entry.get() == "Enter ROM min" else None)  # Remove instruction on click
rom_min_entry.bind("<FocusOut>", lambda event: rom_min_entry.insert(0, "Enter ROM min") if rom_min_entry.get() == "" else None)  # Re-insert instruction if input is blank
rom_min_entry.grid(row=5, column=1, padx=10, pady=10)

# Submit Button
def view():
    activity_name = activity_entry.get()
    print(f'Displaying {activity_name} with Current Settings')

    # Close the last graph created
    plt.close('all')

    # Check that inputs are floats
    try:
        duration = float(duration_entry.get())
        force_max = float(force_max_entry.get())
        force_min = float(force_min_entry.get())
        rom_max = float(rom_max_entry.get())
        rom_min = float(rom_min_entry.get())
    except:
        messagebox.showerror("Error", "Please enter numbers for the duration, force and ROM values")
        return

    if duration <= 0:
        messagebox.showerror("Error", "Duration must be greater than 0")
        return
    
    # Create waveforms
    time, angle = create_waveform(rom_min, rom_max, duration)
    time, force = create_waveform(force_min, force_max, duration, time)
    
    create_force_rom_plot(activity_name, time, force, angle)

view_button = ttk.Button(root, text="View", command=view)
view_button.grid(row=7, column=0, padx=10, pady=10)

# Default Button
def import_activity():
    activity = activity_entry.get()
    print(f'Attempting to read {activity}')
    activity_name, duration, force_max, force_min, rom_max, rom_min, time, angle, force = read_activity(activity)
    if activity_name is None:
        return
    else:
        activity_entry.delete(0, tk.END)
        activity_entry.insert(0, activity_name)
        duration_entry.delete(0, tk.END)
        duration_entry.insert(0, duration)
        force_max_entry.delete(0, tk.END)
        force_max_entry.insert(0, force_max)
        force_min_entry.delete(0, tk.END)
        force_min_entry.insert(0, force_min)
        rom_max_entry.delete(0, tk.END)
        rom_max_entry.insert(0, rom_max)
        rom_min_entry.delete(0, tk.END)
        rom_min_entry.insert(0, rom_min)
        print(f'{activity} has been inputted successfully')

import_button = ttk.Button(root, text="Read Activity", command=import_activity)
import_button.grid(row=7, column=1, padx=10, pady=10)

def confirm():
    print('Attempting to Save Activity to Excel')
    activity_name = activity_entry.get()
    try:
        duration = float(duration_entry.get())
        force_max = float(force_max_entry.get())
        force_min = float(force_min_entry.get())
        rom_max = float(rom_max_entry.get())
        rom_min = float(rom_min_entry.get())
    except:
        messagebox.showerror("Error", "Please enter numbers for the duration, force and ROM values")
        print('Error: Please enter numbers for the duration, force and ROM values')
        return
    
    if duration <= 0:
        messagebox.showerror("Error", "Duration must be greater than 0")
        print('Error: Duration must be greater than 0')
        return
    
    # Remove spaces from activity name and replace with _
    activity_name = activity_name.replace(' ', '_')

    # Save to excel named activity_name.xlsx
    # See if the file already exists
    code_path = os.getcwd()
    folder_path = os.path.join(code_path, 'Activities')
    file_path = os.path.join(folder_path, activity_name + '.xlsx')

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
    settings = pd.DataFrame({'Activity Name': [activity_name],
                                'Duration': [duration],
                                'Force Max': [force_max],
                                'Force Min': [force_min],
                                'ROM Max': [rom_max],
                                'ROM Min': [rom_min]})

    # Save the waveforms to a sheet in the excel file named waveforms
    time, angle = create_waveform(rom_min, rom_max, duration)
    time, force = create_waveform(force_min, force_max, duration, time)

    waveforms = pd.DataFrame({'Time': time, 'Angle': angle, 'Force': force})

    with pd.ExcelWriter(file_path) as writer:
        settings.to_excel(writer, sheet_name='settings', index=False)
        waveforms.to_excel(writer, sheet_name='waveforms', index=False)

    messagebox.showinfo("Success", f"{activity_name} has been saved to " + file_path)
    print('Activity Successfully Saved to Excel')
    exit = messagebox.askyesno("Exit", "Do you want to exit the program?")

    if exit:
        print('Exiting Program')
        root.destroy()
        plt.close('all')
        return       

confirm_button = ttk.Button(root, text="Confirm", command=confirm)
confirm_button.grid(row=7, column=2, padx=10, pady=10)

def close():
    print('Exiting Programme')
    root.destroy()
    plt.close('all')

close_button = ttk.Button(root, text="Close", command=close)
close_button.grid(row=7, column=3, padx=10, pady=10)

root.mainloop()