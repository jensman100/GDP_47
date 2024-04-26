import tkinter as tk

class Main_Menu():
    def __init__(self):
        print('Opening First Window')
        self.window = tk.Tk()
        self.window.title('What would you like to do?')
        self.window.geometry('600x150')
        # self.window.maxsize(400, 150)
        # self.window.minsize(400, 150)
        self.window.configure(bg='#ADD8E6')

        self.next_action = None
        
        self.create_widgets()
        self.window.mainloop()
        
    def create_widgets(self):
        label = tk.Label(self.window, text='Welcome to the Mission Cycle Creator! \n Please select an option below.')
        label.configure(bg='#ADD8E6', height=2)
        label.grid(row=0, column=0, columnspan=4)

        create_activity_button = tk.Button(self.window, text='Create \nActivity', command=self.create_activity)
        create_activity_button.configure(bg='#ADD8E6', height=2, width=20)
        create_activity_button.grid(row=1, column=0)

        create_FMC_button = tk.Button(self.window, text='Create \nFlight Mission Cycle', command=self.create_FMC)
        create_FMC_button.configure(bg='#ADD8E6', height=2, width=20)
        create_FMC_button.grid(row=1, column=1)

        write_to_cpp_button = tk.Button(self.window, text='Write \nto C++', command=self.write_to_cpp)
        write_to_cpp_button.configure(bg='#ADD8E6', height=2, width=20)
        write_to_cpp_button.grid(row=1, column=2)

        run_mission_cycle_button = tk.Button(self.window, text='Run \nMission Cycle', command=self.run_mission_cycle)
        run_mission_cycle_button.configure(bg='#ADD8E6', height=2, width=20)
        run_mission_cycle_button.grid(row=1, column=3)

        blank_label = tk.Label(self.window, text='')
        blank_label.configure(bg='#ADD8E6')
        blank_label.grid(row=2, column=0, columnspan=3)

        close_button = tk.Button(self.window, text='Close', command=self.close)
        close_button.configure(bg='#ADD8E6', height=2, width=10)
        close_button.grid(row=3, column=1, columnspan=2)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        
    def create_activity(self):
        # If pressed then return the integer 1 to the main script
        self.next_action = 'activity'
        print('Displaying Activity Generator...')
        self.window.destroy()
    
    def create_FMC(self):
        self.next_action = 'FMC'
        print('Displaying Flight Mission Cycle Generator...')
        self.window.destroy()
    
    def write_to_cpp(self):
        self.next_action = 'cpp'
        self.window.destroy()

    def run_mission_cycle(self):
        self.next_action = 'run_mission_cycle'
        print('Displaying Mission Cycle Runner...')
        self.window.destroy()

    def close(self):
        self.next_action = None
        print('Closing Application')
        self.window.destroy()
    
    def get_next_action(self):
        print('Closing First Window')
        return self.next_action
