import customtkinter

from CTkListbox import *


def show_value(selected_option):
    print(selected_option)


root = customtkinter.CTk()

listbox = CTkListbox(root, command=show_value, multiple_selection=False)
listbox.pack(fill="both", expand=True, padx=10, pady=10)

listbox.insert("Option 0", index=0)
listbox.insert("Option 1", index=1)
listbox.insert("Option 2", index=2)
listbox.insert("Option 3", index=3)
listbox.insert("Option 4", index=4)
listbox.insert("Option 5", index=5)
listbox.insert("Option 6", index=6)
listbox.insert("Option 7", index=7)
listbox.insert("Option 8")


def delete4ToEnd():
    listbox.delete(index=4, last="end")


def delete3():
    listbox.delete(index=3)


def delete4():
    listbox.delete(index=4)


def add0():
    listbox.insert(option="New Option 0", index=0)


def delete4To5():
    listbox.delete(index=4, last=5)


def move_up_current():
    index = listbox.curselection()
    print(index)
    listbox.move_up(index)


def move_down_current():
    index = listbox.curselection()
    print(index)
    listbox.move_down(index)


button = customtkinter.CTkButton(root, text="Delete Index 3", command=delete3)
button.pack(fill="both", expand=True, padx=10, pady=10)

button2 = customtkinter.CTkButton(root, text="Delete Index 4", command=delete4)
button2.pack(fill="both", expand=True, padx=10, pady=10)

button3 = customtkinter.CTkButton(
    root, text="Delete Index 4 to the End", command=delete4ToEnd
)
button3.pack(fill="both", expand=True, padx=10, pady=10)

button4 = customtkinter.CTkButton(root, text="Add at Index 0", command=add0)
button4.pack(fill="both", expand=True, padx=10, pady=10)

button5 = customtkinter.CTkButton(
    root, text="Delete Index 4 to Index 5", command=delete4To5
)
button5.pack(fill="both", expand=True, padx=10, pady=10)

button6 = customtkinter.CTkButton(root, text="Move Up Current", command=move_up_current)
button6.pack(fill="both", expand=True, padx=10, pady=10)

button7 = customtkinter.CTkButton(
    root, text="Move Down Current", command=move_down_current
)
button7.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
