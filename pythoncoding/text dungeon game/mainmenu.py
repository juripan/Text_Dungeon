import os

from saveandload import load


class MainMenu:
    """
    main menu class, appears at the booting up of the game
    """
    symbol_border: str = "─"
    default_width: int = 50
    logo_width = 114

    def saved_progress_menu(self) -> None:
        saves = os.listdir(r"saves")
        saves = [save for save in saves if save.endswith(".json")]
        for i, save in enumerate(saves):
            print(f"{i + 1}. {save}")
        choice = input("Which one do you want to load: ")

        for i, save in enumerate(saves):
            if choice.lower() == save or choice == str(i + 1):
                file_name = save
                break
            else:
                print(f"No file named or numbered {choice} in the saves directory")
                MainMenu.saved_progress_menu(self)
        
        load(file_name)


    def display_main_menu(self) -> int:
        LOGO = r"""
==================================================================================================================
 ________                      __                  __                                                             
|        \                    |  \                |  \                                                            
 \$$$$$$$$______   __    __  _| $$_           ____| $$ __    __  _______    ______    ______    ______   _______  
   | $$  /      \ |  \  /  \|   $$ \         /      $$|  \  |  \|       \  /      \  /      \  /      \ |       \ 
   | $$ |  $$$$$$\ \$$\/  $$ \$$$$$$        |  $$$$$$$| $$  | $$| $$$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$\| $$$$$$$\
   | $$ | $$    $$  >$$  $$   | $$ __       | $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$    $$| $$  | $$| $$  | $$
   | $$ | $$$$$$$$ /  $$$$\   | $$|  \      | $$__| $$| $$__/ $$| $$  | $$| $$__| $$| $$$$$$$$| $$__/ $$| $$  | $$
   | $$  \$$     \|  $$ \$$\   \$$  $$       \$$    $$ \$$    $$| $$  | $$ \$$    $$ \$$     \ \$$    $$| $$  | $$
    \$$   \$$$$$$$ \$$   \$$    \$$$$         \$$$$$$$  \$$$$$$  \$$   \$$ _\$$$$$$$  \$$$$$$$  \$$$$$$  \$$   \$$
                                                                          |  \__| $$                              
                                                                           \$$    $$                              
                                                                            \$$$$$$                               
=================================================================================================================="""
        print(LOGO)
        print(">NEW GAME (ENTER)<".center(self.logo_width))
        print(">CONTINUE (C)<".center(self.logo_width))
        print(">QUIT (Q)<".center(self.logo_width))
        choice = input(">".rjust(self.logo_width//2))
        if not choice: # if the player presses enter the it runs the game
            return 1
        elif choice.lower() == "c":
            MainMenu.saved_progress_menu(self)
            return 1
        elif choice.lower() == "q":
            print("Are you sure?(y/n)")
            choice = input(">")
            if choice.lower == "y":
                return 0
            else:
                return MainMenu.display_main_menu(self)