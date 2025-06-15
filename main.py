
from settings import Settings
from settings_screen import SettingsScreen
from main_screen import MainScreen


def main():
    settings = Settings()
    main_screen = MainScreen(settings)
    settings_screen = SettingsScreen(settings, main_screen)
    main_screen.start_game()


if __name__ == "__main__":
    main()

