import tkinter as tk

bold_font_large = ('Helvetica', 12, 'bold')
bold_font_small = ('Helvetica', 10, 'bold')

window = tk.Tk()
window.configure(bg='#ADD8E6')

# window.geometry("625x500")
window.minsize(width=625, height=200)
window.maxsize(width=625, height=800)

window.title("Flight Mission Cycle Control Panel")

# scrollbar = tk.Scrollbar(window)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# canvas = tk.Canvas(window, yscrollcommand=scrollbar.set)
# canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# scrollbar.config(command=canvas.yview)

# main_frame = tk.Frame(canvas, bg="#ADD8E6")
# canvas.create_window((0, 0), window=main_frame, anchor='nw')


# def on_frame_configure(event):
#     canvas.config(scrollregion=canvas.bbox("all"))

# main_frame.bind("<Configure>", on_frame_configure)

# canvas.config(yscrollcommand=scrollbar.set)

# canvas.config(scrollregion=canvas.bbox(tk.ALL))

# Writing top line of text
label_title = tk.Label(
    text="Follow the steps below to complete the mission cycle setup.",
    font=bold_font_large,
    fg="black",
    bg="#ADD8E6",
    width=60,
    height=2,
)

label_title.pack()

## Creating buttons for save and open
frame_top_button = tk.Frame(bg="#ADD8E6")

button_open = tk.Button(
    master=frame_top_button,
    text="Open",
    width=10,
    height=2,
    bg="white",
    fg="black",
)

button_save_as = tk.Button(
    master=frame_top_button,
    text="Save As",
    width=10,
    height=2,
    bg="white",
    fg="black",
)

button_save_as.grid(row=0, column=0, padx=(0,5))
button_open.grid(row=0, column=5, padx=(5,0))
frame_top_button.pack()

## Create label and entry for flight mission name
frame_FMC_name = tk.Frame(bg="#ADD8E6")

label_define_FMC = tk.Label(
    master=frame_FMC_name,
    text="Define a New Flight Mission Cycle:",
    font=bold_font_large,
    width=40,
    height=2,
    bg="#ADD8E6",
)

label_FMC_name = tk.Label(
    master=frame_FMC_name,
    text="Flight Mission Cycle Name:",
    font=bold_font_small,
    width=40,
    height=2,
    bg="#ADD8E6",
    )

entry_FMC_name = tk.Entry(
    master=frame_FMC_name,
    width=30,
)

def on_entry_focus_in(event):
    if entry_FMC_name.get() == "Flight Mission Cycle Name Here":
        entry_FMC_name.delete(0, tk.END)

def on_entry_focus_out(event):
    if entry_FMC_name.get() == "":
        entry_FMC_name.insert(0, "Flight Mission Cycle Name Here")

entry_FMC_name.insert(0, "Flight Mission Cycle Name Here")
entry_FMC_name.configure(justify=tk.CENTER)
entry_FMC_name.bind("<FocusIn>", on_entry_focus_in)
entry_FMC_name.bind("<FocusOut>", on_entry_focus_out)

label_define_FMC.grid(row=0, column=0)
label_FMC_name.grid(row=1, column=0)
entry_FMC_name.grid(row=2, column=0)
frame_FMC_name.pack()

## Create label and space for entered activities
frame_show_activity = tk.Frame(bg="#ADD8E6")

label_active = tk.Label(
    master=frame_show_activity,
    text="Select Activities to Form a Flight Mission Cycle Batch:",
    font=bold_font_small,
    width=42,
    height=2,
    bg="#ADD8E6",
)

label_selected = tk.Label(
    master=frame_show_activity,
    text="Selected:",
    font=bold_font_small,
    width=8,
    height=1,
    bg="#ADD8E6",
)

label_activity = tk.Label(
    master=frame_show_activity,
    text="Activity:",
    font=bold_font_small,
    width=8,
    height=1,
    bg="#ADD8E6",
)

label_cycles = tk.Label(
    master=frame_show_activity,
    text="Cycles:",
    font=bold_font_small,
    width=8,
    height=1,
    bg="#ADD8E6",
)

listbox = tk.Listbox(frame_show_activity, width=25)
listbox.grid(row=3, column=0, columnspan=3, sticky="nsew")

# for i in range(8):
#     activity_frame = tk.Frame(listbox)
#     activity_frame.pack(fill=tk.X)

#     checkbox = tk.Checkbutton(activity_frame)
#     checkbox.grid(row=0, column=1, padx=(75,0))

#     activity_label = tk.Label(activity_frame, text="Activity" + str(i))
#     activity_label.grid(row=0, column=0, padx=(28,0))

#     entry_cycles = tk.Entry(activity_frame, width=8)
#     entry_cycles.insert(0, "0")
#     entry_cycles.configure(justify=tk.CENTER)
#     entry_cycles.grid(row=0, column=2, sticky="e", padx=(75,0))
    
scrollbar = tk.Scrollbar(frame_show_activity, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.grid(row=3, column=3, sticky="ns")
listbox.config(yscrollcommand=scrollbar.set)

label_active.grid(row=0, column=0, columnspan=3)
label_activity.grid(row=2, column=0)
label_selected.grid(row=2, column=1)
label_cycles.grid(row=2, column=2)

frame_show_activity.pack()

# Create input for batch cycles
frame_batch_cycles = tk.Frame(bg="#ADD8E6")

label_batch_cycles = tk.Label(
    master=frame_batch_cycles,
    text="Cycles of Activity Batch:",
    font=bold_font_small,
    width=20,
    height=1,
    bg="#ADD8E6",
)

entry_batch_cycles = tk.Entry(frame_batch_cycles, width=8)
entry_batch_cycles.insert(0, "0")
entry_batch_cycles.configure(justify=tk.CENTER)

label_batch_cycles.grid(row=0, column=0)
entry_batch_cycles.grid(row=0, column=1)

frame_batch_cycles.pack()

# Create inputs for new activity
frame_input_activity = tk.Frame(bg="#ADD8E6")

label_new_activity = tk.Label(
    master=frame_input_activity,
    text="Define a New Activity:",
    font=bold_font_large,
    width=40,
    height=2,
    bg="#ADD8E6",
)

label_new_activity_name = tk.Label(
    master=frame_input_activity,
    text="New Activity Name:",
    font=bold_font_small,
    width=20,
    height=2,
    bg="#ADD8E6",
)

def on_entry_focus_in_activity(event):
    if entry_activity_name.get() == "New Activity Name Here":
        entry_activity_name.delete(0, tk.END)

def on_entry_focus_out_activity(event):
    if entry_activity_name.get() == "":
        entry_activity_name.insert(0, "New Activity Name Here")

entry_activity_name = tk.Entry(frame_input_activity, width=30)
entry_activity_name.insert(0, "New Activity Name Here")
entry_activity_name.configure(justify=tk.CENTER)
entry_activity_name.grid(row=1, column=1, columnspan=5, sticky="w", padx=(15,0))

entry_activity_name.bind("<FocusIn>", on_entry_focus_in_activity)
entry_activity_name.bind("<FocusOut>", on_entry_focus_out_activity)

label_min = tk.Label(
    master=frame_input_activity,
    text="Min:",
    font=bold_font_small,
    width=16,
    height=2,
    bg="#ADD8E6",
)

label_max = tk.Label(
    master=frame_input_activity,
    text="Max:",
    font=bold_font_small,
    width=16,
    height=2,
    bg="#ADD8E6",
)

label_period = tk.Label(
    master=frame_input_activity,
    text="Period:",
    font=bold_font_small,
    width=16,
    height=2,
    bg="#ADD8E6",
)

label_ROM = tk.Label(
    master=frame_input_activity,
    text="Range of Motion Function:",
    font=bold_font_small,
    width=20,
    height=2,
    bg="#ADD8E6",
)

def on_entry_focus_in_ROM(event):
    if entry_ROM_min.get() == "ROM Min Here":
        entry_ROM_min.delete(0, tk.END)

def on_entry_focus_out_ROM(event):
    if entry_ROM_min.get() == "":
        entry_ROM_min.insert(0, "ROM Min Here")

entry_ROM_min = tk.Entry(frame_input_activity, width=16)
entry_ROM_min.insert(0, "ROM Min Here")
entry_ROM_min.configure(justify=tk.CENTER)
entry_ROM_min.grid(row=2, column=1, sticky="w", padx=(15,0))

entry_ROM_min.bind("<FocusIn>", on_entry_focus_in_ROM)
entry_ROM_min.bind("<FocusOut>", on_entry_focus_out_ROM)


def on_entry_focus_in_ROM(event):
    if entry_ROM_max.get() == "ROM Max Here":
        entry_ROM_max.delete(0, tk.END)

def on_entry_focus_out_ROM(event):
    if entry_ROM_max.get() == "":
        entry_ROM_max.insert(0, "ROM Max Here")

entry_ROM_max = tk.Entry(frame_input_activity, width=16)
entry_ROM_max.insert(0, "ROM Max Here")
entry_ROM_max.configure(justify=tk.CENTER)
entry_ROM_max.grid(row=2, column=2, sticky="w", padx=(15,0))

entry_ROM_max.bind("<FocusIn>", on_entry_focus_in_ROM)
entry_ROM_max.bind("<FocusOut>", on_entry_focus_out_ROM)


def on_entry_focus_in_ROM(event):
    if entry_ROM_period.get() == "ROM Period Here":
        entry_ROM_period.delete(0, tk.END)

def on_entry_focus_out_ROM(event):
    if entry_ROM_period.get() == "":
        entry_ROM_period.insert(0, "ROM Period Here")

entry_ROM_period = tk.Entry(frame_input_activity, width=16)
entry_ROM_period.insert(0, "ROM Period Here")
entry_ROM_period.configure(justify=tk.CENTER)
entry_ROM_period.grid(row=2, column=3, sticky="w", padx=(15,0))

entry_ROM_period.bind("<FocusIn>", on_entry_focus_in_ROM)
entry_ROM_period.bind("<FocusOut>", on_entry_focus_out_ROM)

label_loading = tk.Label(
    master=frame_input_activity,
    text="Loading Function:",
    font=bold_font_small,
    width=20,
    height=2,
    bg="#ADD8E6",
)

def on_entry_focus_in_load(event):
    if entry_loading_min.get() == "Load Min Here":
        entry_loading_min.delete(0, tk.END)

def on_entry_focus_out_load(event):
    if entry_loading_min.get() == "":
        entry_loading_min.insert(0, "Load Min Here")

entry_loading_min = tk.Entry(frame_input_activity, width=16)
entry_loading_min.insert(0, "Load Min Here")
entry_loading_min.configure(justify=tk.CENTER)
entry_loading_min.grid(row=3, column=1, sticky="w", padx=(15,0))

entry_loading_min.bind("<FocusIn>", on_entry_focus_in_load)
entry_loading_min.bind("<FocusOut>", on_entry_focus_out_load)


def on_entry_focus_in_load(event):
    if entry_loading_max.get() == "Load Max Here":
        entry_loading_max.delete(0, tk.END)

def on_entry_focus_out_load(event):
    if entry_loading_max.get() == "":
        entry_loading_max.insert(0, "Load Max Here")

entry_loading_max = tk.Entry(frame_input_activity, width=16)
entry_loading_max.insert(0, "Load Max Here")
entry_loading_max.configure(justify=tk.CENTER)
entry_loading_max.grid(row=3, column=2, sticky="w", padx=(15,0))

entry_loading_max.bind("<FocusIn>", on_entry_focus_in_load)
entry_loading_max.bind("<FocusOut>", on_entry_focus_out_load)

def on_entry_focus_in_load(event):
    if entry_loading_period.get() == "Load Period Here":
        entry_loading_period.delete(0, tk.END)

def on_entry_focus_out_load(event):
    if entry_loading_period.get() == "":
        entry_loading_period.insert(0, "Load Period Here")

entry_loading_period = tk.Entry(frame_input_activity, width=16)
entry_loading_period.insert(0, "Load Period Here")
entry_loading_period.configure(justify=tk.CENTER)
entry_loading_period.grid(row=3, column=3, sticky="w", padx=(15,0))

entry_loading_period.bind("<FocusIn>", on_entry_focus_in_load)
entry_loading_period.bind("<FocusOut>", on_entry_focus_out_load)

label_new_activity.grid(row=0, column=0, columnspan=8, sticky="ew", pady=(15,0))
label_new_activity_name.grid(row=1, column=0)
label_min.grid(row=1, column=1)
label_max.grid(row=1, column=2)
label_period.grid(row=1, column=3)
label_ROM.grid(row=2, column=0)
label_loading.grid(row=3, column=0)

frame_input_activity.pack()

# Add or import new activity
frame_add_activity = tk.Frame(bg="#ADD8E6")

button_add_active = tk.Button(
    master=frame_add_activity,
    text="Add Actvity",
    width=12,
    height=2,
    bg="white",
    fg="black",
)

button_import_active = tk.Button(
    master=frame_add_activity,
    text="Import Activity",
    width=12,
    height=2,
    bg="white",
    fg="black",
)

label_add_active = tk.Label(
    master=frame_add_activity,
    text="Select 'Add Activity' when above fields have been completed:",
    font=bold_font_small,
    width=50,
    height=2,
    bg="#ADD8E6",
)

label_import_active = tk.Label(
    master=frame_add_activity,
    text="Select 'Import Activity' to add an existing activity to the list:",
    font=bold_font_small,
    width=50,
    height=2,
    bg="#ADD8E6",
)

label_add_active.grid(row=0, column=0)
label_import_active.grid(row=1, column=0)
button_add_active.grid(row=0, column=1, padx=(0,0))
button_import_active.grid(row=1, column=1, padx=(0,0))

frame_add_activity.pack()

window.mainloop()