# used for the main menu display and functionality
import os

from saveandload import load
from color_file import colors


def saved_progress_menu() -> None:
    saves = os.listdir(r"saves\\")
    saves = [save for save in saves if save.endswith(".json")]
    print("─" * 50)
    for i, save in enumerate(saves):
        print(f"{i + 1}. {save}")
    print("─" * 50)
    choice = input("Which one do you want to load: ")

    for i, save in enumerate(saves):
        if choice.lower() == save or choice == str(i + 1):
            file_name = save
            load(file_name)
            break
    else:
        print(f"No file named or numbered {choice} in the saves directory")
        saved_progress_menu()


def display_main_menu() -> int:
    LOGO = r"""
{}==================================================================================================================
{} ________                      __                  __                                                             
{}|        \                    |  \                |  \                                                            
{} \$$$$$$$$______   __    __  _| $$_           ____| $$ __    __  _______    ______    ______    ______   _______  
{}   | $$  /      \ |  \  /  \|   $$ \         /      $$|  \  |  \|       \  /      \  /      \  /      \ |       \ 
{}   | $$ |  $$$$$$\ \$$\/  $$ \$$$$$$        |  $$$$$$$| $$  | $$| $$$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$\| $$$$$$$\
{}   | $$ | $$    $$  >$$  $$   | $$ __       | $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$    $$| $$  | $$| $$  | $$
{}   | $$ | $$$$$$$$ /  $$$$\   | $$|  \      | $$__| $$| $$__/ $$| $$  | $$| $$__| $$| $$$$$$$$| $$__/ $$| $$  | $$
{}   | $$  \$$     \|  $$ \$$\   \$$  $$       \$$    $$ \$$    $$| $$  | $$ \$$    $$ \$$     \ \$$    $$| $$  | $$
{}    \$$   \$$$$$$$ \$$   \$$    \$$$$         \$$$$$$$  \$$$$$$  \$$   \$$ _\$$$$$$$  \$$$$$$$  \$$$$$$  \$$   \$$
{}                                                                          |  \__| $$                              
{}                                                                           \$$    $$                              
{}                                                                            \$$$$$$                               
{}=================================================================================================================={}""".format(colors["red"], colors["blue"], colors["purple"],
                                                                                                                               colors["red"], colors["blue"], colors["purple"],
                                                                                                                               colors["red"], colors["blue"], colors["purple"],
                                                                                                                               colors["red"], colors["blue"], colors["purple"],
                                                                                                                               colors["red"], colors["blue"], colors["default"])
    print(LOGO)
    logo_width: int = 114
    print(">NEW GAME (ENTER)<".center(logo_width))
    print(">CONTINUE (C)<".center(logo_width))
    print(">QUIT (Q)<".center(logo_width))
    choice = input(">".rjust(logo_width//2))
    if not choice: # if the player presses enter the it runs the game
        return 1
    elif choice.lower() == "c":
        saved_progress_menu()
        return 1
    elif choice.lower() == "q":
        print("Are you sure?(y/n)")
        choice = input(">")
        if choice.lower() == "y":
            return 0
        else:
            return display_main_menu()
    else:
        print("invalid command")
        return display_main_menu()