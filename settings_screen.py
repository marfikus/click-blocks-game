
from tkinter import BooleanVar, Toplevel, Checkbutton


class SettingsScreen:
    def __init__(self, settings):
        self.settings = settings
        self.settings_screen = None
        self.settings_screen_is_active = False

        self.remove_all_siblings_var = BooleanVar()
        self.remove_all_siblings_var.set(1)
        self.add_multiple_blocks_var = BooleanVar()
        self.add_multiple_blocks_var.set(1)


    def show(self):
        if self.settings_screen_is_active:
            return

        self.settings_screen = Toplevel()
        self.settings_screen.title("Settings")
        self.settings_screen.resizable(False, False)
        self.settings_screen.protocol("WM_DELETE_WINDOW", self.close)
        self.settings_screen_is_active = True

        Checkbutton(self.settings_screen, 
            text="remove_all_siblings",
            variable=self.remove_all_siblings_var,
            onvalue=1,
            offvalue=0,
            command=self.update_settings
        ).pack()

        Checkbutton(self.settings_screen, 
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
        self.settings_screen.destroy()
        print(self.settings_screen)
        self.settings_screen_is_active = False


