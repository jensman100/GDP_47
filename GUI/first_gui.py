import tkinter as tk

class FirstWindow():
    def __init__(self):
        print('Opening First Window')
        self.window = tk.Tk()
        self.window.title('What would you like to do?')
        self.window.geometry('500x100')
        self.window.maxsize(500, 100)
        self.window.minsize(500, 100)
        self.window.configure(bg='#ADD8E6')

        self.result = None
        
        self.create_widgets()
        self.window.mainloop()
        
    def create_widgets(self):
        label = tk.Label(self.window, text='Welcome to the Mission Cycle Creator! \n Please select an option below.')
        label.configure(bg='#ADD8E6', height=2, width=50)
        label.grid(row=0, column=0, columnspan=3)

        create_activity_button = tk.Button(self.window, text='Create Activity', command=self.create_activity)
        create_activity_button.configure(bg='#ADD8E6', height=2, width=15)
        create_activity_button.grid(row=1, column=0)

        create_FMC_button = tk.Button(self.window, text='Create Flight Mission Cycle', command=self.create_FMC)
        create_FMC_button.configure(bg='#ADD8E6', height=2, width=25)
        create_FMC_button.grid(row=1, column=1)

        write_to_cpp_button = tk.Button(self.window, text='Write to C++', command=self.write_to_cpp)
        write_to_cpp_button.configure(bg='#ADD8E6', height=2, width=10)
        write_to_cpp_button.grid(row=1, column=2)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        
    def create_activity(self):
        # If pressed then return the integer 1 to the main script
        self.result = 'activity'
        print('Displaying Activity Generator...')
        self.window.destroy()
    
    def create_FMC(self):
        self.result = 'FMC'
        print('Displaying Flight Mission Cycle Generator...')
        self.window.destroy()
    
    def write_to_cpp(self):
        self.result = 'cpp'
        self.window.destroy()
    
    def get_result(self):
        print('Closing First Window')
        return self.result
