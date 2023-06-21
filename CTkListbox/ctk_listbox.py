"""
Custom ListBox for customtkinter
Author: Akash Bora
"""

import customtkinter

class CTkListbox(customtkinter.CTkScrollableFrame):

    def __init__(self,
                 master: any,
                 height: int = 100,
                 width: int = 200,
                 hightlight_color: str = "default",
                 fg_color: str = "transparent",
                 bg_color: str = None,
                 text_color: str = "default",
                 select_color: str = "default",
                 hover_color: str = "default",
                 border_width: int = 3,
                 font: tuple = "default",
                 command = None,
                 **kwargs):
        
        super().__init__(master, width=width, height=height, fg_color=fg_color, border_width=border_width, **kwargs)
        self._scrollbar.grid_configure(padx=(0,border_width))
        self._scrollbar.configure(width=12)
        
        if bg_color:
            super().configure(bg_color=bg_color)

        self.select_color = customtkinter.ThemeManager.theme["CTkButton"]["fg_color"] if select_color=="default" else select_color
        self.text_color = customtkinter.ThemeManager.theme["CTkButton"]["text_color"] if text_color=="default" else text_color
        self.hover_color = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"] if hover_color=="default" else hover_color
        self.font = (customtkinter.ThemeManager.theme["CTkFont"]["family"],13) if font=="default" else font
        self.buttons = {}
        self.command = command
        self.selected = None
    
    def select(self, index):
        """ select the option """
        for options in self.buttons.values():
            options.configure(fg_color="transparent")
        self.buttons[index].configure(fg_color=self.select_color)
        self.selected = self.buttons[index]
        if self.command:
            self.command(self.get())
        
    def insert(self, index, option, justify="left", **args):
        """ select new value in the listbox """
        if justify=="left":
            justify = "w"
        elif justify=="right":
            justify = "e"
        else:
            justify = "c"
            
        if index in self.buttons:
            if index!="END":
                self.delete(index)
            
        self.buttons[index] = customtkinter.CTkButton(self, text=option, fg_color="transparent", anchor=justify,
                                                      text_color=self.text_color, font=self.font,
                                                      hover_color=self.hover_color, **args)
        self.buttons[index].configure(command=lambda num=index: self.select(num))
        self.buttons[index].pack(padx=0, pady=(0,5), fill="x", expand=True)

    def delete(self, index):
        """ delete a value from the listbox """
        self.buttons[index].destroy()
        del self.buttons[index]
        
    def size(self):
        """ return total number of items in the listbox """
        return len(self.buttons.values())

    def get(self, index=None):
        """ get the selected value """
        if index:
            if index=="ALL":
                return self.buttons[index].cget("text")
            else:
                return list(item.cget("text") for item in self.buttons.values())
        else:
            return self.selected.cget("text") if self.selected is not None else None
        
    def configure(self, **kwargs):
        """ configurable options of the listbox """
        
        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
            for i in self.buttons.values():
                i.configure(hover_color=self.hover_color)
        if "highlight_color" in kwargs:
            self.select_color = kwargs.pop("highlight_color")
            if self.selected: self.selected.configure(fg_color=self.select_color)
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            for i in self.buttons.values():
                i.configure(text=self.text_color)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
            for i in self.buttons.values():
                i.configure(font=self.font)

        super().configure(**kwargs)
