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
        width: int = 200,
        hightlight_color: str = "default",
        fg_color: str = "transparent",
        bg_color: str = None,
        text_color: str = "default",
        select_color: str = "default",
        hover_color: str = "default",
        button_fg_color: str = "default",
        border_width: int = 3,
        font: tuple = "default",
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
            if select_color == "default"
            else select_color
        )
        self.text_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["text_color"]
            if text_color == "default"
            else text_color
        )
        self.hover_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]
            if hover_color == "default"
            else hover_color
        )
        self.font = (
            (customtkinter.ThemeManager.theme["CTkFont"]["family"], 13)
            if font == "default"
            else font
        )
        self.button_fg_color = (
            "transparent" if button_fg_color == "default" else button_fg_color
        )

        if justify == "left":
            self.justify = "w"
        elif justify == "right":
            self.justify = "e"
        else:
            self.justify = "c"
        self.buttons = []
        self.command = command
        self.multiple = multiple_selection
        self.selected = None
        self.hover = hover
        self.selections = []
        self.selected_index = 0

        if listvariable:
            self.listvariable = listvariable
            self.listvariable.trace_add("write", lambda a, b, c: self.update_listvar())
            self.update_listvar()

        super().bind("<Destroy>", lambda e: self.unbind_all("<Configure>"))

    def update_listvar(self):
        values = list(eval(self.listvariable.get()))
        self.delete("all")
        for i in values:
            self.insert(option=i)

    def select(self, index):
        """select the option"""
        for option in self.buttons:
            option.configure(fg_color=self.button_fg_color)

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

        selected = self.buttons[index]
        self.select(selected)

    def curselection(self):
        index = 0
        if self.multiple:
            indexes = []
            for i in self.buttons:
                if i in self.selections:
                    indexes.append(index)
                index += 1
            return tuple(indexes)

        else:
            for i in self.buttons:
                if i == self.selected:
                    return index
                else:
                    index += 1

    def bind(self, key, func):
        super().bind_all(key, lambda e: func(self.get()), add="+")

    def deselect(self, index):
        if not self.multiple:
            self.selected.configure(fg_color=self.button_fg_color)
            self.selected = None
            return
        if self.buttons[index] in self.selections:
            self.selections.remove(self.buttons[index])
            self.buttons[index].configure(fg_color=self.button_fg_color)

    def deactivate(self, index):
        if str(index).lower() == "all":
            for i in self.buttons:
                self.deselect(i)
            return

        selected = self.buttons[index]
        self.deselect(selected)

    def insert(self, option, index: int = -1, order: bool = False, **args):
        """add new option in the listbox"""

        if 0 <= index < len(self.buttons):
            self.buttons[index].configure(text=option, **args)
        else:
            button = customtkinter.CTkButton(
                self,
                text=option,
                fg_color=self.button_fg_color,
                anchor=self.justify,
                text_color=self.text_color,
                font=self.font,
                hover_color=self.hover_color,
                **args,
            )

            if index < 0:
                self.buttons.append(button)
                index = self.buttons.index(button)
            else:
                self.buttons.insert(index, button)

            self.buttons[index].configure(command=lambda num=index: self.select(num))
            self.buttons[index].pack(padx=0, pady=(0, 5), fill="x", expand=True)
            self.update()

        if self.multiple:
            self.buttons[index].bind(
                "<Shift-1>", lambda e: self.select_multiple(self.buttons[index])
            )

        return self.buttons[index]

    def select_multiple(self, button):
        selections = self.buttons
        if len(self.selections) > 0:
            last = selections.index(self.selections[-1])
            to = selections.index(button)

            if last < to:
                for i in range(last + 1, to + 1):
                    if self.buttons[i] not in self.selections:
                        self.select(i)
            else:
                for i in range(to, last):
                    if self.buttons[i] not in self.selections:
                        self.select(i)

    def delete(self, index, last=None):
        """delete options from the listbox"""

        def recalculate_index(i):
            for new_index in range(i, len(self.buttons)):
                self.buttons[new_index].configure(
                    command=lambda num=new_index: self.select(num)
                )

        if str(index).lower() == "all":
            for i in self.buttons:
                self.buttons[i].destroy()
            self.buttons = []
            return

        if int(index) < 0 or int(index) >= len(self.buttons):
            return

        if last:
            if str(last).lower() == "end":
                last = len(self.buttons) - 1
            elif (
                int(last) <= int(index)
                or int(last) < 0
                or int(last) >= len(self.buttons)
            ):
                return

            deleted_list = []
            for i in range(int(index), int(last) + 1):
                self.buttons[i].destroy()
                deleted_list.append(i)
                self.update()

            deleted_list.sort(reverse=True)
            for i in deleted_list:
                del self.buttons[i]

            recalculate_index(index)
        else:
            self.buttons[index].destroy()
            del self.buttons[index]

            recalculate_index(index)

    def size(self):
        """return total number of items in the listbox"""
        return len(self.buttons)

    def get(self, index=None):
        """get the selected value"""
        if index is not None:
            if str(index).lower() == "all":
                return list(item.cget("text") for item in self.buttons)
            else:
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
        if "button_fg_color" in kwargs:
            self.button_fg_color = kwargs.pop("button_fg_color")
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
                i.configure(text=self.text_color)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
            for i in self.buttons.values():
                i.configure(font=self.font)
        if "command" in kwargs:
            self.command = kwargs.pop("command")

        super().configure(**kwargs)

    def move_up(self, index):
        """Move the option up in the listbox"""
        if index > 0:
            previous_index = index - 1

            # Store the text of the button to be moved
            current_text = self.buttons[index].cget("text")

            # Update the text of the buttons
            self.buttons[index].configure(
                text=self.buttons[previous_index].cget("text")
            )
            self.buttons[previous_index].configure(text=current_text)

            # Clear the selection from the current option
            self.deselect(index)

            # Update the selection
            self.select(previous_index)

            # Update the scrollbar position
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview("scroll", -int(100 / 6), "units")

    def move_down(self, index):
        """Move the option down in the listbox"""
        if index < len(self.buttons) - 1:
            next_index = index + 1

            # Store the text of the button to be moved
            current_text = self.buttons[index].cget("text")

            # Update the text of the buttons
            self.buttons[index].configure(text=self.buttons[next_index].cget("text"))
            self.buttons[next_index].configure(text=current_text)

            # Clear the selection from the current option
            self.deselect(index)

            # Update the selection
            self.select(next_index)

            # Update the scrollbar position
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview("scroll", int(100 / 6), "units")
