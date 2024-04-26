import tkinter as tk
import random
import threading
import time
from tkinter import messagebox

''' This file is for creating the running flight mission cycle gui'''


class RunningFlightMissionCycle():
    def __init__(self, activities):
        self.activities = activities
        self.len_activities = len(activities)
        self.activity_index = 0
        self.current_activity = self.activities[self.activity_index]

        if self.len_activities == 1:
            self.next_activity = 'Test Finish'
        elif not self.activity_index == self.len_activities:
            self.next_activity = self.activities[self.activity_index + 1]
        else:
            self.next_activity = 'Test Finish'

        self.started = False

        self.progression = 0
        self.bar_total_length = 250

        self.root = tk.Tk()
        self.root.title('Running Flight Mission Cycle')
        self.paused = True

        self.set_force_value = 0
        self.actual_force_value = 0

        self.set_rom_value = 0
        self.actual_rom_value = 0

        self.set_temp_value = 0
        self.actual_temp_value = 0

        self.run_thread = True
        self.test_finished = False

        # Setting up code to run continuously to read the serial data
        self.serial_thread = threading.Thread(target=self.listen_for_serial_data)
        self.serial_thread.start()

        self.create_widgets()

        self.root.mainloop()

        self.run_thread = False
        self.serial_thread.join(timeout=2)
        ### WRITE LINE TO ARDUINO TO STOP
        print('CLOSING GUI')
        return

        
    def create_widgets(self):
        self.top = tk.Frame(self.root)
        self.top.pack(fill=tk.BOTH, expand=True, anchor='center')

        self.top_text = tk.Label(self.top, text='Running Flight Mission Cycle')
        self.top_text.pack(fill=tk.BOTH, expand=True)

        self.running_indicator = tk.Label(self.top, text='Press Play/Pause to start the test', fg='red') 
        self.running_indicator.pack(fill=tk.BOTH, expand=True)

        self.information = tk.Frame(self.root)
        self.information.pack(fill=tk.BOTH, expand=True, anchor='center')

        for i in range(5):
            self.information.grid_columnconfigure(i, weight=1)
            self.information.grid_rowconfigure(0, weight=1)

        self.set_force_text = tk.Label(self.information, text='Set Force:')
        self.set_force_text.grid(row=0, column=0, columnspan=2)

        self.set_force_value_text = tk.Label(self.information, text=self.set_force_value)
        self.set_force_value_text.grid(row=0, column=2)

        self.actual_force_text = tk.Label(self.information, text='Actual Force:')
        self.actual_force_text.grid(row=0, column=3, columnspan=2)

        self.actual_force_value_text = tk.Label(self.information, text=self.actual_force_value)
        self.actual_force_value_text.grid(row=0, column=5)

        self.set_rom_text = tk.Label(self.information, text='Set ROM:')
        self.set_rom_text.grid(row=1, column=0, columnspan=2)

        self.set_rom_value_text = tk.Label(self.information, text=self.set_rom_value)
        self.set_rom_value_text.grid(row=1, column=2)

        self.actual_rom_text = tk.Label(self.information, text='Actual ROM:')
        self.actual_rom_text.grid(row=1, column=3, columnspan=2)

        self.actual_rom_value_text = tk.Label(self.information, text=self.actual_rom_value)
        self.actual_rom_value_text.grid(row=1, column=5)

        self.set_temp_text = tk.Label(self.information, text='Set Temperature:')
        self.set_temp_text.grid(row=2, column=0, columnspan=2)

        self.set_temp_value_text = tk.Label(self.information, text=self.set_temp_value)
        self.set_temp_value_text.grid(row=2, column=2)

        self.actual_temp_text = tk.Label(self.information, text='Actual Temperature:')
        self.actual_temp_text.grid(row=2, column=3, columnspan=2)

        self.actual_temp_value_text = tk.Label(self.information, text=self.actual_temp_value)
        self.actual_temp_value_text.grid(row=2, column=5)

        self.current_activity_text = tk.Label(self.information, text='Current Activity:')
        self.current_activity_text.grid(row=3, column=1, columnspan=2)

        self.current_activity_value_text = tk.Label(self.information, text=self.current_activity)
        self.current_activity_value_text.grid(row=3, column=4)

        self.next_activity_text = tk.Label(self.information, text='Next Activity:')
        self.next_activity_text.grid(row=4, column=1, columnspan=2)

        self.next_activity_value_text = tk.Label(self.information, text=self.next_activity)
        self.next_activity_value_text.grid(row=4, column=4)

        self.progress_bar = tk.Frame(self.root)
        self.progress_bar.pack(fill=tk.BOTH, expand=True, anchor='center')

        self.progress_bar_text = tk.Label(self.progress_bar, text='Progression through flight mission cycle')
        self.progress_bar_text.pack(fill=tk.BOTH, expand=True, anchor='center')

        self.progress_bar = tk.Canvas(self.progress_bar, width=self.bar_total_length, height=20)
        self.progress_bar.pack(fill=tk.BOTH, expand=True, anchor='center')

        self.progress_bar.create_rectangle(0, 0, self.bar_total_length, 20, fill='grey')
        self.progress_bar.create_rectangle(0, 0, self.progression, 20, fill='green')
        self.progress_bar.create_text(self.bar_total_length/2, 10, text=f'{self.len_activities - self.activity_index} activities remaining', fill='black', tags="progress_text")

        self.buttons = tk.Frame(self.root)
        self.stop_button = tk.Button(self.buttons, text='Stop', command=self.stop, width=10, height=2)
        self.stop_button.grid(row=0, column=0, padx=10, pady=10)

        self.playpause_button = tk.Button(self.buttons, text='Play/Pause', command=self.playpause, width=10, height=2)
        self.playpause_button.grid(row=0, column=1, padx=10, pady=10)

        self.buttons.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def close_window(self):
        self.root.destroy()

    def stop(self):
        print('STOP')
        self.run_thread = False
        self.close_window()

        
    def playpause(self):
        if not self.started:
            self.started = True
            self.paused = False
            ### WRITE LINE TO ARDUINO TO START
            print(str(self.current_activity))
        elif self.paused:
            self.paused = False
            ### WRITE LINE TO ARDUINO TO PLAY
            print('PLAY')
        else:
            self.paused = True
            ### WRITE LINE TO ARDUINO TO PAUSE
            print('PAUSE')
        self.update_running_indicator()

    def update_running_indicator(self):
        if self.paused:
            self.running = 'Paused'
            colour = 'red'
        else:
            self.running = 'Running'
            colour = 'green'
        if hasattr(self, 'running_indicator'):
            self.running_indicator.destroy()

        self.running_indicator = tk.Label(self.top, text=self.running, fg=colour) 
        self.running_indicator.pack(fill=tk.BOTH, expand=True)

    def update_activity(self):
        self.activity_index += 1
        self.progression = int((self.activity_index) * (self.bar_total_length / self.len_activities))
        if self.activity_index < self.len_activities - 1 and self.run_thread:
            self.current_activity = self.activities[self.activity_index]
            self.next_activity = self.activities[self.activity_index + 1]
            self.progress_bar.create_rectangle(0, 0, self.progression, 20, fill='green')

            self.progress_bar.delete("progress_text")

            remaining_activities = self.len_activities - self.activity_index
            self.progress_bar.create_text(self.bar_total_length/2, 10, text=f'{remaining_activities} activities remaining', tags="progress_text")

            # Write to arduino to move to next activity
            print(str(self.current_activity))

        elif self.activity_index == self.len_activities - 1 and self.run_thread:
            self.current_activity = self.activities[self.activity_index]
            self.next_activity = 'Test Finish'
            self.progress_bar.create_rectangle(0, 0, self.progression, 20, fill='green')
            self.progress_bar.delete("progress_text")
            remaining_activities = self.len_activities - self.activity_index
            self.progress_bar.create_text(self.bar_total_length/2, 10, text=f'{remaining_activities} activity remaining', tags="progress_text")
            
            # Write to arduino to move to next activity
            print(str(self.current_activity))

        else:
            self.progress_bar.create_rectangle(0, 0, self.bar_total_length, 20, fill='green')
            self.progress_bar.delete("progress_text")
            self.progress_bar.create_text(self.bar_total_length/2, 10, text='0 activities remaining', tags="progress_text")
            self.current_activity = 'Test Finish'
            self.next_activity = 'Test Finish'
            return False

        self.current_activity_value_text.config(text=self.current_activity)
        self.next_activity_value_text.config(text=self.next_activity)
        return True

    def listen_for_serial_data(self):
    ### NEEDS UPDATING WITH ARDUINO
        count = 0
        while self.run_thread:
            while not self.paused:
                if not self.run_thread:
                    self.root.after(1000, self.close_window)
                    break
                self.collect_values()
                self.root.after(0, self.update_values)
                time.sleep(0.1)
                count += 1
                if count == 2:
                    self.run_thread = self.update_activity()
                    a = self.run_thread
                    count = 0
            time.sleep(0.1)
        
        print('Thread finished')
        
    ### Different values to collect
    # Update info values
    # Update moving on to next activity
            
    def update_values(self):
        if self.test_finished:
            self.root.destroy()
            self.run_thread = False

        self.set_force_value_text.config(text=self.set_force_value)
        self.actual_force_value_text.config(text=self.actual_force_value)

        self.set_rom_value_text.config(text=self.set_rom_value)
        self.actual_rom_value_text.config(text=self.actual_rom_value)

        self.set_temp_value_text.config(text=self.set_temp_value)
        self.actual_temp_value_text.config(text=self.actual_temp_value)

    def collect_values(self):
        ### NEEDS UPDATING WITH ARDUINO
        self.set_force_value = random.randint(0, 100)
        self.actual_force_value = random.randint(0, 100)

        self.set_rom_value = random.randint(0, 100)
        self.actual_rom_value = random.randint(0, 100)

        self.set_temp_value = random.randint(0, 100)
        self.actual_temp_value = random.randint(0, 100)


if __name__ == '__main__':
    RunningFlightMissionCycle(['Start', 'Middle', 'End'])
