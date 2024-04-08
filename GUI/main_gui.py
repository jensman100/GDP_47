'''
This code contains the Class to create the main GUI
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

import pandas as pd
import os


class Main_GUI:
    def __init__(self, current_dir):
        print('Opening Main Window')
        self.what_next = None
        ### Create the main window
        self.window = tk.Tk()
        self.window.configure(bg='#ADD8E6')

        # window.geometry("625x500")
        self.window.minsize(width=700, height=500)
        self.window.maxsize(width=700, height=500)

        self.window.title("Flight Mission Cycle Control Panel")

        ### Initalize the frames which change

        ## Creating buttons for save and open
        self.frame_top_button = tk.Frame(bg="#ADD8E6")
        ## Create input for flight mission cycle name
        self.frame_FMC_name = tk.Frame(bg="#ADD8E6")
        # Create a space for added activities
        self.frame_show_activity = tk.Frame(bg="#ADD8E6")
        # Create input for batch cycles
        self.frame_batch_cycles = tk.Frame(bg="#ADD8E6")

        ### Initialize the activity setting stores
        self.activity_settings = {} # Dictionary of imported activities
        self.activity_list = []     # List of all activities in order
        self.checkboxes = []        # Stores whether activity is selected
        self.cycles = []            # Stores the number of cycles for each activity

        ### Storing location for reading/saving files
        self.current_dir = current_dir

        ### Creating the fonts
        self.bold_font_large = ('Helvetica', 12, 'bold')
        self.bold_font_small = ('Helvetica', 10, 'bold')

        ###  Creating the GUI
        ## Creating title
        label_title = tk.Label(
            text="Follow the steps below to complete the mission cycle setup.",
            font=self.bold_font_large,
            fg="black",
            bg="#ADD8E6",
            width=60,
            height=2,
        )
        
        label_title.pack()

        ## Buttons for saving GUI or opening a previous Mission Cycle
        button_open = tk.Button(
            master=self.frame_top_button,
            command=self.open_FMC,
            text="Open",
            width=10,
            height=2,
            bg="white",
            fg="black",
        )

        button_save_as = tk.Button(
            master=self.frame_top_button,
            command=self.save_FMC,
            text="Save As",
            width=10,
            height=2,
            bg="white",
            fg="black",
        )

        ## Add button to generate C++
        button_generate_cpp = tk.Button(
            master=self.frame_top_button,
            command=self.generate_cpp,
            text="Generate C++",
            width=10,
            height=2,
            bg="white",
            fg="black",
        )

        ## Add close button
        button_close = tk.Button(
            master=self.frame_top_button,
            text="Back",
            command=self.close_all,
            width=10,
            height=2,
            bg="white",
            fg="black",
        )

        button_save_as.grid(row=0, column=0, padx=(0,5))
        button_open.grid(row=0, column=1, padx=(5,0))
        button_generate_cpp.grid(row=0, column=2, padx=(5,0))
        button_close.grid(row=0, column=3, padx=(5,0))

        ## Create label and entry for flight mission name

        label_define_FMC = tk.Label(
            master=self.frame_FMC_name,
            text="Define a New Flight Mission Cycle:",
            font=self.bold_font_large,
            width=40,
            height=2,
            bg="#ADD8E6",
        )

        label_define_FMC.grid(row=0, column=0)

        ## Adding titles for the activity space
        self.label_active = tk.Label(self.frame_show_activity,
            text="Select Activities to Form a Flight Mission Cycle Batch:",
            font=self.bold_font_small,
            width=42,
            height=2,
            bg="#ADD8E6",
        )

        self.label_activity = tk.Label(self.frame_show_activity,
            text="Activity:",
            font=self.bold_font_small,
            width=8,
            height=1,
            bg="#ADD8E6",
        )
        self.label_selected = tk.Label(self.frame_show_activity,
            text="Selected:",
            font=self.bold_font_small,
            width=8,
            height=1,
            bg="#ADD8E6",
        )

        self.label_cycles = tk.Label(self.frame_show_activity,
            text="Cycles:",
            font=self.bold_font_small,
            width=8,
            height=1,
            bg="#ADD8E6",
        )

        self.label_blank = tk.Label(self.frame_show_activity,
            text="",
            font=self.bold_font_small,
            width=8,
            height=1,
            bg="#ADD8E6")

        ## Adding button to add next activity
        self.label_import_activity = tk.Label(self.frame_show_activity,
            text='Input activity name and select "Add Activity":',
            font=self.bold_font_small,
            height=1,
            bg="#ADD8E6")
        
        self.entry_import_activity = tk.Entry(self.frame_show_activity)
        self.entry_import_activity.insert(0, "Enter activity name")
        self.entry_import_activity.bind("<FocusIn>", lambda event: self.entry_import_activity.delete(0, tk.END) if self.entry_import_activity.get() == "Enter activity name" else None)
        self.entry_import_activity.bind("<FocusOut>", lambda event: self.entry_import_activity.insert(0, "Enter activity name") if self.entry_import_activity.get() == "" else None)

        self.button_import_activity = tk.Button(self.frame_show_activity, 
            command=self.import_activity,
            text="Add Activity",
            width=12,
            height=1,
            bg="white",
            fg="black",
        )

        self.label_active.grid(row=0, column=0, columnspan=3)

        self.entry_import_activity.grid(row=1, column=0, columnspan=2)
        self.button_import_activity.grid(row=1, column=2)

        self.label_blank.grid(row=2, column=0)

        self.label_activity.grid(row=3, column=0)
        self.label_selected.grid(row=3, column=1)
        self.label_cycles.grid(row=3, column=2)
        self.label_blank.grid(row=4, column=0)

        self.next_row = 4

        ## Adding number of cycles for the batch
        label_batch_cycles = tk.Label(
            master=self.frame_batch_cycles,
            text="Cycles of Activity Batch:",
            font=self.bold_font_small,
            width=20,
            height=1,
            bg="#ADD8E6",
        )

        self.entry_batch_cycles = tk.Entry(self.frame_batch_cycles, width=8)
        self.entry_batch_cycles.insert(0, "1")
        self.entry_batch_cycles.configure(justify=tk.CENTER)

        label_batch_cycles.grid(row=0, column=0)
        self.entry_batch_cycles.grid(row=0, column=1)

        ### Pack the frames
        self.frame_top_button.pack()
        self.frame_FMC_name.pack()
        self.frame_show_activity.pack()
        self.frame_batch_cycles.pack()

        self.window.mainloop()

    ### Class functions
    ## When save as pressed
    def open_FMC(self):
        response = simpledialog.askstring("Open FMC", 
                                          "Please enter the name of the Flight mission cycle to open:")
        if response is None or response == "":
            return
            
        else:
            if response[:-5] != '.xlsx':
                response = response + '.xlsx'
            # remove spaces
            FMC_file_name = response.replace(' ', '_')

        FMC_dir = os.path.join(self.current_dir, 'Flight_Mission_Cycles')
        try:
            df_activities = pd.read_excel(os.path.join(FMC_dir, FMC_file_name), sheet_name='Activities')
            df_settings = pd.read_excel(os.path.join(FMC_dir, FMC_file_name), sheet_name='Settings', index_col=0)

            activities = df_activities['Activities'].to_list()
            saved_activities = df_settings.index.to_list()
            for activity_setting in saved_activities:
                if activity_setting not in self.activity_settings.keys(): # If activity has not yet been read
                    # create a dictionary with key as activity name and value as settings
                    self.activity_settings[activity_setting] = df_settings.loc[activity_setting].to_list()
                else:
                    print(f'"{activity_setting}" already imported, skipping.')
                    existing_setting = self.activity_settings[activity_setting]
                    messagebox.showinfo("Info", f'"{activity_setting}" already defined.Using the existing settings: \n [Dur, Max Force, Min Force, ROM Max, Rom Min] \n {existing_setting}')

                self.activity_list.append(activities)
                for activity in activities:
                    self.add_activity_to_gui(activity)

        except:
            print('Error opening file')
            messagebox.showerror("Error", "Error opening file, please make sure file exists and is formatted correctly and try again.")
            return
        

    def save_FMC(self):
        print('Checking FMC')
        checked_count = [var.get() for var in self.checkboxes]
        cycles_list = [self.cycles[i] for i in range(len(self.cycles)) if checked_count[i]]
        activies_list = [self.activity_list[i] for i in range(len(self.activity_list)) if checked_count[i]]
        batch_cycles = self.entry_batch_cycles.get()

        # Make sure positive integers are inputted for cycles
        try: # Try to change to integer
            cycles_list_int = [int(entry.get()) for entry in cycles_list]
            batch_cycles = int(batch_cycles)
            # Raise error if less than 1
            for value in cycles_list_int:
                if value < 1: 
                    raise ValueError
            if batch_cycles < 1:
                raise ValueError
        except:
            print('Value error reading cycles.')
            messagebox.showerror("Error", "Error reading cycles, please make sure cycle number is a positive integer.")
            return

        if len(activies_list) == 0: # If no activities selected
            print('No activities selected.')
            messagebox.showerror("Error", "No activities selected, please select at least one activity.")
            return
        
        response = simpledialog.askstring("Save As", 
                                          "Please enter the name to save the flight mission cycle as:")
        if response is None or response == "":
            return
        else:
            if response[:-5] != '.xlsx':
                response = response + '.xlsx'
            # remove spaces
            FMC_file_name = response.replace(' ', '_')

        ## Multiplying the activities by the number of cycles
        FMC_activities = []
        for i in range(len(activies_list)):
            FMC_activities += [activies_list[i]] * cycles_list_int[i]

        FMC_activities = FMC_activities * batch_cycles
        
        print('Saving FMC')
        ### Save to excel
        ### activites sheet is a list of activities
        ### Second sheet is the settings for each activity

        ## Check if file already exists
        FMC_dir = os.path.join(self.current_dir, 'Flight_Mission_Cycles')

        if FMC_file_name in os.listdir(FMC_dir):
            print('File already exists')
            overwrite = messagebox.askyesno("File Exists", "File already exists, do you want to overwrite the file?")
            if not overwrite:
                return
        try:    
            with pd.ExcelWriter(os.path.join(FMC_dir, FMC_file_name)) as writer:
                df = pd.DataFrame(FMC_activities, columns=['Activities'])
                df.to_excel(writer, sheet_name='Activities', index=False)

                # write dictionary to settings sheet with headings activity name, duration, force max, force min, rom max, rom min
                df = pd.DataFrame(self.activity_settings).T
                df.columns = ["Duration", "Force Max", "Force Min", "ROM Max", "ROM Min"]
                df.to_excel(writer, sheet_name='Settings')

            print(f'Flight mission cycle saved as {FMC_file_name}. Success')
            again = messagebox.askyesno("Success", f'Flight mission cycle saved as {FMC_file_name}. Do you want to create another flight mission cycle?')
            if again:
                return
            else:
                self.close_all()
        except:
            print('Error opening and saving file')
            messagebox.showerror("Error", "Error saving file, please make sure file is closed and try again.")
            return
        
    def generate_cpp(self):
        self.close_all()
        self.what_next = 'cpp'

    ## Called during import activity to show activity in GUI
    def add_activity_to_gui(self, activity_name):
        # Add activity to GUI
        self.label_imported_activity = tk.Label(self.frame_show_activity,
            text= f'{activity_name}',
            font=self.bold_font_small,
            width=8,
            height=1,
            bg="#ADD8E6")
        
        checkbox_var = tk.BooleanVar()
        
        self.checkbox_imported_activity = tk.Checkbutton(self.frame_show_activity, variable=checkbox_var)
        self.checkbox_imported_activity.select()

        self.entry_imported_cycles = tk.Entry(self.frame_show_activity, width=8)
        self.entry_imported_cycles.insert(0, 1)

        self.label_imported_activity.grid(row=self.next_row, column=0)
        self.checkbox_imported_activity.grid(row=self.next_row, column=1)
        self.entry_imported_cycles.grid(row=self.next_row, column=2)

        self.checkboxes.append(checkbox_var)
        self.cycles.append(self.entry_imported_cycles)

        self.next_row += 1

    ## Called when add activity button is pressed
    def import_activity(self):
        # Read name inputted in GUI
        activity_name = self.entry_import_activity.get()

        if activity_name not in self.activity_settings.keys(): # If activity has not yet been read
            print(f'"{activity_name}" is not yet imported, attempting to add "{activity_name}" to the list of activities.')
            file_name = activity_name + '.xlsx'
            activity_dir = os.path.join(self.current_dir, 'Activities')
            
            if file_name in os.listdir(activity_dir): # Check if activity exists in activity folder
                try:        # If in the folder, try to read the activity
                    df = pd.read_excel(os.path.join(activity_dir, file_name), sheet_name='settings', )
                    settings = df.iloc[0].to_list()[1:]
                    # Add settings to list of activities
                    self.activity_settings[activity_name] = settings
                    self.activity_list.append(activity_name)

                    self.add_activity_to_gui(activity_name)
                    print(f'Succesfully imported "{activity_name}" and added to activity list.')

                except:     # If error reading the file, show error
                    print(f'Error reading "{activity_name}" from activities folder.')
                    messagebox.showerror("Error", f'Error reading "{activity_name}" from activities folder, please check the format of the file.')

            else:
                # If not in the folder, show error, show which activities are available
                print(f'{activity_name} not found in activities folder.')
                activities_available = [file.split('.')[0] for file in os.listdir(activity_dir)]
                messagebox.showerror("Error", f'''"{activity_name}" not found in activities folder. 
The following activities are available: {activities_available}''')
        else: # If activity has already been impored
            print(f'"{activity_name}" already imported, adding to activity list.')
            self.activity_list.append(activity_name)
            self.add_activity_to_gui(activity_name)
            return
        
    def close_all(self):
        print('Closing Main Window')
        self.window.destroy()
        self.what_next = 'first'

    def get_result(self):
        return self.what_next