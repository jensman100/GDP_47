import tkinter as tk

bold_font_large = ('Helvetica', 12, 'bold')
bold_font_small = ('Helvetica', 10, 'bold')

def create_main_window():
    window = tk.Tk()
    window.configure(bg='#ADD8E6')
    window.geometry("600x600")
    window.title("Flight Mission Cycle Control Panel")

    # Fix the window size (prevent resizing)
    # window.resizable(width=False, height=False)

    return window

def create_title_label(parent):
    label_title = tk.Label(
        parent,
        text="Follow the instructions below to complete the mission cycle setup.",
        font=bold_font_large,
        fg="black",
        bg="#ADD8E6",
        width=80,
        height=2
    )
    label_title.pack()

def create_buttons(parent):
    frame_a = tk.Frame(master=parent, relief=tk.GROOVE, borderwidth=2, bg="#ADD8E6")

    button_open = tk.Button(
        master=frame_a,
        text="Open",
        width=10,
        height=2,
        bg="white",
        fg="black",
    )

    button_save_as = tk.Button(
        master=frame_a,
        text="Save As",
        width=10,
        height=2,
        bg="white",
        fg="black",
    )

    frame_a.pack()
    button_save_as.grid(row=0, column=0, padx=(0,5))
    button_open.grid(row=0, column=5, padx=(5,0))

def create_name_entry(parent):
    frame_b = tk.Frame(master=parent, relief=tk.GROOVE, borderwidth=2, bg="#ADD8E6")

    label_FMC_name = tk.Label(
        master=frame_b,
        text="Flight Mission Cycle Name:",
        font=bold_font_small,
        width=40,
        height=2,
        bg="#ADD8E6",
        )
    entry_FMC_name = tk.Entry(
        master=frame_b,
        width=30,
    )
    def on_entry_focus_in(event):
        if entry_FMC_name.get() == "Enter Name Here":
            entry_FMC_name.delete(0, tk.END)

    def on_entry_focus_out(event):
        if entry_FMC_name.get() == "":
            entry_FMC_name.insert(0, "Enter Name Here")

    entry_FMC_name.insert(0, "Enter Name Here")
    entry_FMC_name.configure(justify=tk.CENTER)
    entry_FMC_name.bind("<FocusIn>", on_entry_focus_in)
    entry_FMC_name.bind("<FocusOut>", on_entry_focus_out)

    # Apply to all entries 


    frame_b.pack()
    label_FMC_name.grid(row=0, column=0)
    entry_FMC_name.grid(row=1, column=0)


def create_activity_selection(parent):
    frame_c = tk.Frame(master=parent, relief=tk.GROOVE, borderwidth=2, bg="#ADD8E6")

    label_active = tk.Label(
        master=frame_c,
        text="Select Activities to Form a Flight Mission Cycle:",
        font=bold_font_small,
        width=40,
        height=2,
        bg="#ADD8E6",
    )

    label_selected = tk.Label(
        master=frame_c,
        text="Selected:",
        font=bold_font_small,
        width=8,
        height=1,
        bg="#ADD8E6",
    )
    label_activity = tk.Label(
        master=frame_c,
        text="Activity:",
        font=bold_font_small,
        width=8,
        height=1,
        bg="#ADD8E6",
    )
    label_cycles = tk.Label(
        master=frame_c,
        text="Cycles:",
        font=bold_font_small,
        width=8,
        height=1,
        bg="#ADD8E6",
    )

    listbox = tk.Listbox(frame_c, width=25)
    listbox.grid(row=2, column=0, columnspan=3, sticky="nsew")

    for i in range(8):
        activity_frame = tk.Frame(listbox)
        activity_frame.pack(fill=tk.X)

        checkbox = tk.Checkbutton(activity_frame)
        checkbox.grid(row=0, column=1, padx=(70,0))

        activity_label = tk.Label(activity_frame, text="Activity" + str(i))
        activity_label.grid(row=0, column=0, padx=(25,0))

        entry_cycles = tk.Entry(activity_frame, width=8)
        entry_cycles.insert(0, "0")
        entry_cycles.configure(justify=tk.CENTER)
        entry_cycles.grid(row=0, column=2, sticky="e", padx=(65,0))
        
          

    scrollbar = tk.Scrollbar(frame_c, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.grid(row=2, column=3, sticky="ns")
    listbox.config(yscrollcommand=scrollbar.set)

    frame_c.pack()
    label_active.grid(row=0, column=0, columnspan=3)
    label_activity.grid(row=1, column=0)
    label_selected.grid(row=1, column=1)
    label_cycles.grid(row=1, column=2)


def create_activity(parent):
    frame_d = tk.Frame(master=parent, relief=tk.GROOVE, borderwidth=2, bg="#ADD8E6")

    label_new_activity = tk.Label(
        master=frame_d,
        text="Define a New Activity:",
        font=bold_font_small,
        width=40,
        height=2,
        bg="#ADD8E6",
    )

    label_new_activity_name = tk.Label(
        master=frame_d,
        text="New Activity Name:",
        font=bold_font_small,
        width=20,
        height=2,
        bg="#ADD8E6",
    )

    def on_entry_focus_in_activity(event):
        if entry_activity_name.get() == "Enter New Activity Name Here":
            entry_activity_name.delete(0, tk.END)

    def on_entry_focus_out_activity(event):
        if entry_activity_name.get() == "":
            entry_activity_name.insert(0, "Enter New Activity Name Here")
    
    entry_activity_name = tk.Entry(frame_d, width=30)
    entry_activity_name.insert(0, "Enter New Activity Name Here")
    entry_activity_name.configure(justify=tk.CENTER)
    entry_activity_name.grid(row=1, column=1, sticky="e", padx=(65,0))

    entry_activity_name.bind("<FocusIn>", on_entry_focus_in_activity)
    entry_activity_name.bind("<FocusOut>", on_entry_focus_out_activity)

    label_ROM = tk.Label(
        master=frame_d,
        text="Range of Motion Function:",
        font=bold_font_small,
        width=20,
        height=2,
        bg="#ADD8E6",
    )

    def on_entry_focus_in_ROM(event):
        if entry_ROM_function.get() == "Enter ROM Function Here":
            entry_ROM_function.delete(0, tk.END)

    def on_entry_focus_out_ROM(event):
        if entry_ROM_function.get() == "":
            entry_ROM_function.insert(0, "Enter ROM Function Here")

    entry_ROM_function = tk.Entry(frame_d, width=30)
    entry_ROM_function.insert(0, "Enter ROM Function Here")
    entry_ROM_function.configure(justify=tk.CENTER)
    entry_ROM_function.grid(row=2, column=1, sticky="e", padx=(65,0))

    entry_ROM_function.bind("<FocusIn>", on_entry_focus_in_ROM)
    entry_ROM_function.bind("<FocusOut>", on_entry_focus_out_ROM)

    label_loading = tk.Label(
        master=frame_d,
        text="Loading Function:",
        font=bold_font_small,
        width=20,
        height=2,
        bg="#ADD8E6",
    )

    def on_entry_focus_in_load(event):
        if entry_loading_function.get() == "Enter Loading Function Here":
            entry_loading_function.delete(0, tk.END)

    def on_entry_focus_out_load(event):
        if entry_loading_function.get() == "":
            entry_loading_function.insert(0, "Enter Loading Function Here")

    entry_loading_function = tk.Entry(frame_d, width=30)
    entry_loading_function.insert(0, "Enter Loading Function Here")
    entry_loading_function.configure(justify=tk.CENTER)
    entry_loading_function.grid(row=3, column=1, sticky="e", padx=(50,0))

    entry_loading_function.bind("<FocusIn>", on_entry_focus_in_load)
    entry_loading_function.bind("<FocusOut>", on_entry_focus_out_load)

    frame_d.pack()
    label_new_activity.grid(row=0, column=0, columnspan=2)
    label_new_activity_name.grid(row=1, column=0)
    label_ROM.grid(row=2, column=0)
    label_loading.grid(row=3, column=0)

def stop_application():
    window.destroy()

### Start of code

if __name__ == '__main__':
    window = create_main_window()
    create_title_label(window)
    create_buttons(window)
    create_name_entry(window)
    create_activity_selection(window)
    create_activity(window)

    window.mainloop()