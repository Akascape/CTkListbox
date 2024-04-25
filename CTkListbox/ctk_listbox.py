"""
Custom ListBox for customtkinter
Author: Akash Bora
"""

import customtkinter

class CTkListbox(customtkinter.CTkScrollableFrame):
    def __init__(
        self,
        master: any,
        height: int = 100,
        width: int = 150,
        highlight_color: str = "default",
        fg_color: str = "transparent",
        bg_color: str = None,
        text_color: str = "default",
        hover_color: str = "default",
        button_color: str = "default",
        border_width: int = 3,
        font: tuple = None,
        multiple_selection: bool = False,
        listvariable=None,
        hover: bool = True,
        command=None,
        justify="left",
        **kwargs,
        ):
        super().__init__(
            master,
            width=width,
            height=height,
            fg_color=fg_color,
            border_width=border_width,
            **kwargs,
        )
        self._scrollbar.grid_configure(padx=(0, border_width + 4))
        self._scrollbar.configure(width=12)

        if bg_color:
            super().configure(bg_color=bg_color)

        self.select_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]
            if highlight_color == "default"
            else highlight_color
        )
        self.text_color = (
            customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
            if text_color == "default"
            else text_color
        )
        self.hover_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]
            if hover_color == "default"
            else hover_color
        )
        
        if not font:
            self.font = customtkinter.CTkFont(customtkinter.ThemeManager.theme["CTkFont"]["family"],13)
        else:
            if isinstance(font, customtkinter.CTkFont):
                self.font = font
            else:
                self.font = customtkinter.CTkFont(font)
                
        self.button_fg_color = (
            "transparent" if button_color == "default" else button_color
        )

        if justify == "left":
            self.justify = "w"
        elif justify == "right":
            self.justify = "e"
        else:
            self.justify = "c"
        self.buttons = {}
        self.command = command
        self.multiple = multiple_selection
        self.selected = None
        self.hover = hover
        self.end_num = 0
        self.selections = []
        self.selected_index = 0
        self._scrollbar.configure(height=height)
        self.columnconfigure(0, weight=1)
        
        if listvariable:
            self.listvariable = listvariable
            self.listvariable.trace_add("write", lambda a, b, c: self.update_listvar())
            self.update_listvar()

    def update_listvar(self):
        values = list(eval(self.listvariable.get()))
        self.delete("all")
        for i in values:
            self.insert("END", option=i)

    def select(self, index):
        """select the option"""
        for options in self.buttons.values():
            options.configure(fg_color=self.button_fg_color)
        
        if isinstance(index, int):
            if index in self.buttons:
                selected_button = self.buttons[index]
            else:
                selected_button = list(self.buttons.values())[index]
        else:
            selected_button = self.buttons[index]
  
        if self.multiple:
            if selected_button in self.selections:
                self.selections.remove(selected_button)
                selected_button.configure(fg_color=self.button_fg_color, hover=False)
                self.after(100, lambda: selected_button.configure(hover=self.hover))
            else:
                self.selections.append(selected_button)
            for i in self.selections:
                i.configure(fg_color=self.select_color, hover=False)
                self.after(100, lambda button=i: button.configure(hover=self.hover))
        else:
            self.selected = selected_button
            selected_button.configure(fg_color=self.select_color, hover=False)
            self.after(100, lambda: selected_button.configure(hover=self.hover))

        if self.command:
            self.command(self.get())

        self.event_generate("<<ListboxSelect>>")

    def activate(self, index):
        if str(index).lower() == "all":
            if self.multiple:
                for i in self.buttons:
                    self.select(i)
            return

        if str(index).lower() == "end":
            index = -1

        selected = list(self.buttons.keys())[index]
        self.select(selected)

    def curselection(self):
        index = 0
        if self.multiple:
            indexes = []
            for i in self.buttons.values():
                if i in self.selections:
                    indexes.append(index)
                index += 1
            return tuple(indexes)

        else:
            for i in self.buttons.values():
                if i == self.selected:
                    return index
                else:
                    index += 1

    def bind(self, key, func, add="+"):
        super().bind(key, lambda e: func(e), add=add)
        self._parent_frame.bind(key, lambda e: func(e), add=add)
        self._parent_canvas.bind(key, lambda e: func(e), add=add)
        
    def unbind(self, key):
        super().unbind(key)
        self._parent_frame.unbind(key)
        self._parent_canvas.unbind(key)
        
    def deselect(self, index):
        if not self.multiple:
            if self.selected:
                self.selected.configure(fg_color=self.button_fg_color)
                self.selected = None
                return
        if self.buttons[index] in self.selections:
            self.selections.remove(self.buttons[index])
            self.buttons[index].configure(fg_color=self.button_fg_color)

    def deactivate(self, index):
        if str(index).lower() == "all":
            if self.multiple:
                for i in self.buttons:
                    self.deselect(i)
            else:
                self.deselect(0)
            return
        
        if str(index).lower() == "end":
            index = -1

        selected = list(self.buttons.keys())[index]
        self.deselect(selected)

    def insert(self, index, option, update=True, **args):
        """add new option in the listbox"""

        if str(index).lower() == "end":
            index = f"END{self.end_num}"
            self.end_num += 1

        if index in self.buttons:
            self.buttons[index].destroy()

        self.buttons[index] = customtkinter.CTkButton(
            self,
            text=option,
            fg_color=self.button_fg_color,
            anchor=self.justify,
            text_color=self.text_color,
            font=self.font,
            hover_color=self.hover_color,
            **args,
        )
        self.buttons[index].configure(command=lambda num=index: self.select(num))
        
        if type(index) is int:
            self.buttons[index].grid(padx=0, pady=(0, 5), sticky="nsew", column=0, row=index)
        else:
            self.buttons[index].grid(padx=0, pady=(0, 5), sticky="nsew", column=0)
            
        if update:
            self.update()

        if self.multiple:
            self.buttons[index].bind(
                "<Shift-1>", lambda e: self.select_multiple(self.buttons[index])
            )

        return self.buttons[index]
        
    def select_multiple(self, button):
        selections = list(self.buttons.values())
        if len(self.selections) > 0:
            last = selections.index(self.selections[-1])
            to = selections.index(button)

            if last < to:
                for i in range(last + 1, to + 1):
                    if list(self.buttons.values())[i] not in self.selections:
                        self.select(i)
            else:
                for i in range(to, last):
                    if list(self.buttons.values())[i] not in self.selections:
                        self.select(i)
    def destroy(self):
        for i in self.buttons:
            self.buttons[i].destroy()
        self._scrollbar.destroy()
        super().destroy()
        
        self._parent_frame.destroy()
        self._parent_canvas.destroy()
        
    def delete(self, index, last=None):
        """delete options from the listbox"""
        if str(index).lower() == "all":
            self.deactivate("all")
            for i in self.buttons:
                self.buttons[i].destroy()
                self.update()
            self.buttons = {}
            self.end_num = 0
            return

        if str(index).lower() == "end":
            self.end_num -= 1
            if len(self.buttons.keys())>0:
                index = list(self.buttons.keys())[-1]
            if index not in self.buttons:
                return
        else:
            if int(index) >= len(self.buttons):
                return
            if not last:
                index = list(self.buttons.keys())[int(index)]

        if last:
            if str(last).lower() == "end":
                last = len(self.buttons) - 1
            elif int(last) >= len(self.buttons):
                last = len(self.buttons) - 1

            deleted_list = []
            for i in range(int(index), int(last) + 1):
                list(self.buttons.values())[i].destroy()
                deleted_list.append(list(self.buttons.keys())[i])
                self.update()
            for i in deleted_list:
                del self.buttons[i]
        else:
            self.buttons[index].destroy()
            if self.multiple:
                if self.buttons[index] in self.selections:
                    self.selections.remove(self.buttons[index])
            del self.buttons[index]
        
    def size(self):
        """return total number of items in the listbox"""
        return len(self.buttons.keys())

    def get(self, index=None):
        """get the selected value"""
        if index is not None:
            if str(index).lower() == "all":
                return list(item.cget("text") for item in self.buttons.values())
            else:
                index = list(self.buttons.keys())[int(index)]
                return self.buttons[index].cget("text")
        else:
            if self.multiple:
                return (
                    [x.cget("text") for x in self.selections]
                    if len(self.selections) > 0
                    else None
                )
            else:
                return self.selected.cget("text") if self.selected is not None else None

    def configure(self, **kwargs):
        """configurable options of the listbox"""

        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
            for i in self.buttons.values():
                i.configure(hover_color=self.hover_color)
        if "button_color" in kwargs:
            self.button_fg_color = kwargs.pop("button_color")
            for i in self.buttons.values():
                i.configure(fg_color=self.button_fg_color)
        if "highlight_color" in kwargs:
            self.select_color = kwargs.pop("highlight_color")
            if self.selected:
                self.selected.configure(fg_color=self.select_color)
            if len(self.selections) > 0:
                for i in self.selections:
                    i.configure(fg_color=self.select_color)
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            for i in self.buttons.values():
                i.configure(text_color=self.text_color)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
            for i in self.buttons.values():
                i.configure(font=self.font)
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "hover" in kwargs:
            self.hover = kwargs.pop("hover")
            for i in self.buttons.values():
                i.configure(hover=self.hover)
        if "justify" in kwargs:
            self.justify = kwargs.pop("justify")
            if self.justify == "left":
                self.justify = "w"
            elif self.justify == "right":
                self.justify = "e"
            else:
                self.justify = "c"
            for i in self.buttons.values():
                i.configure(anchor=self.justify) 
        if "height" in kwargs:
            self._scrollbar.configure(height=kwargs["height"])
        if "multiple_selection" in kwargs:
            self.multiple = kwargs.pop("multiple_selection")
        
        super().configure(**kwargs)

    def cget(self, param):
        if param=="hover_color":
            return self.hover_color
        if param=="button_color":
            return self.button_fg_color
        if param=="highlight_color":
            return self.select_color
        if param=="text_color":
            return self.text_color
        if param=="font":
            return self.font
        if param=="hover":
            return self.hover
        if param=="justify":
            return self.justify
        return super().cget(param)
    
    def move_up(self, index):
        """Move the option up in the listbox"""
        if index > 0:
            current_key = list(self.buttons.keys())[index]
            previous_key = list(self.buttons.keys())[index - 1]

            # Store the text of the button to be moved
            current_text = self.buttons[current_key].cget("text")

            # Update the text of the buttons
            self.buttons[current_key].configure(
                text=self.buttons[previous_key].cget("text")
            )
            self.buttons[previous_key].configure(text=current_text)

            # Clear the selection from the current option
            self.deselect(current_key)

            # Update the selection
            self.select(previous_key)

            # Update the scrollbar position
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview("scroll", -int(100 / 6), "units")

    def move_down(self, index):
        """Move the option down in the listbox"""
        if index < len(self.buttons) - 1:
            current_key = list(self.buttons.keys())[index]
            next_key = list(self.buttons.keys())[index + 1]

            # Store the text of the button to be moved
            current_text = self.buttons[current_key].cget("text")

            # Update the text of the buttons
            self.buttons[current_key].configure(
                text=self.buttons[next_key].cget("text")
            )
            self.buttons[next_key].configure(text=current_text)

            # Clear the selection from the current option
            self.deselect(current_key)

            # Update the selection
            self.select(next_key)

            # Update the scrollbar position
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview("scroll", int(100 / 6), "units")
