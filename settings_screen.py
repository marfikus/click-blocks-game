
from tkinter import BooleanVar, Toplevel, Checkbutton


class SettingsScreen:
    def __init__(self, settings, main_screen):
        self.settings = settings
        self.screen = None
        self.screen_is_active = False
        self.main_screen = main_screen
        self.main_screen.settings_screen = self


    def show(self):
        if self.screen_is_active:
            return

        self.screen = Toplevel()
        x = self.main_screen.root.winfo_x()
        y = self.main_screen.root.winfo_y()
        self.screen.geometry(f"+{x}+{y}")
        self.screen.title("Settings")
        self.screen.resizable(False, False)
        self.screen.protocol("WM_DELETE_WINDOW", self.close)
        self.screen_is_active = True

        self.remove_all_siblings_var = BooleanVar()
        self.remove_all_siblings_var.set(self.settings.remove_all_siblings)
        self.add_multiple_blocks_var = BooleanVar()
        self.add_multiple_blocks_var.set(self.settings.add_multiple_blocks)

        Checkbutton(self.screen, 
            text="remove_all_siblings",
            variable=self.remove_all_siblings_var,
            onvalue=1,
            offvalue=0,
            command=self.update_settings
        ).pack()

        Checkbutton(self.screen, 
            text="add_multiple_blocks",
            variable=self.add_multiple_blocks_var,
            onvalue=1,
            offvalue=0,
            command=self.update_settings
        ).pack()


    def update_settings(self):
        self.settings.remove_all_siblings = self.remove_all_siblings_var.get()
        self.settings.add_multiple_blocks = self.add_multiple_blocks_var.get()


    def close(self):
        self.screen.destroy()
        self.screen_is_active = False


