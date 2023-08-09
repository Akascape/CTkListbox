# CTkListbox
This is a **listbox widget** for customtkinter, works just like the tkinter listbox.

![Screenshot](https://github.com/Akascape/CTkListbox/assets/89206401/256c135f-3d6c-4daa-87a5-b4572a2c905f)

## Installation
```
pip install CTkListbox
```
### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/CTkListbox?&color=white&label=Download%20Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="400">](https://github.com/Akascape/CTkListbox/archive/refs/heads/main.zip)

## Usage
```python
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
```
## Arguments
| Parameter | Description |
|-----------| ------------|
| **master** | parent widget  |
| width | **optional**, set width of the listbox |
| height | **optional**, set height of the listbox |
| fg_color | foreground color of the listbox |
| border_color | border color of the listbox frame |
| border_width | width of the border frame |
| text_color | set the color of the option text |
| hover_color | set hover color of the options |
| highlight_color | set the selected color of the option |
| font | set font of the option text |
| command | calls a command when a option is selected |
| multiple_selection | select multiple options in the listbox, `default=False`|
| listvariable | use a tkinter variable to change the listbox content |
| *other_parameters | _all other parameters of ctk_scrollable frame can be passed_ |

## Methods
- **.insert(index, option)**
   add nwq option to the listbox
- **.get()**
   get the selected option(s)
- **.delete(index)**
   delete any option from the listbox
- **.size()**
   get the size of the listbox
- **.activate(index)**
  activate any option
- **.deactivae(index)**
  deactivate any option
- **.curselection()**
  returns indexes of selected options
- **.configure()**
   change some parameters for the listbox
  
### Thanks for visiting! Hope it will help :)
