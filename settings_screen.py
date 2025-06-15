
from tkinter import BooleanVar, Toplevel, Checkbutton


class SettingsScreen:
    def __init__(self, settings, main_screen):
        self.settings = settings
        self.settings_screen = None
        self.settings_screen_is_active = False
        main_screen.link_to_mainmenu(self)


    def show(self):
        if self.settings_screen_is_active:
            return

        self.settings_screen = Toplevel()
        self.settings_screen.title("Settings")
        self.settings_screen.resizable(False, False)
        self.settings_screen.protocol("WM_DELETE_WINDOW", self.close)
        self.settings_screen_is_active = True

        self.remove_all_siblings_var = BooleanVar()
        self.remove_all_siblings_var.set(self.settings.remove_all_siblings)
        self.add_multiple_blocks_var = BooleanVar()
        self.add_multiple_blocks_var.set(self.settings.add_multiple_blocks)

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
        self.settings_screen_is_active = False


