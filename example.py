import customtkinter
from CTkListbox import *

def show_value(selected_option):
    print(selected_option)
    
root = customtkinter.CTk()

listbox = CTkListbox(root, command=show_value)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

listbox.insert(0, "Option 0")
listbox.insert(1, "Option 1")
listbox.insert(2, "Option 2")
listbox.insert(3, "Option 3")
listbox.insert(4, "Option 4")
listbox.insert(5, "Option 5")
listbox.insert(6, "Option 6")
listbox.insert(7, "Option 7")
listbox.insert("END", "Option 8")

root.mainloop()
