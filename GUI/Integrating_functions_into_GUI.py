from functions_for_GUI import *
from Functions_for_Mission_Cycle_Graphs import *

### Initialize the GUI
window = create_main_window()
create_title_label(window)
create_buttons(window)
create_name_entry(window)
create_activity_selection(window)
create_activity(window)

window.mainloop()