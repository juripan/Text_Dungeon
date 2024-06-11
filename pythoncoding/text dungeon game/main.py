# main file used for running the whole project
import mainmenu as mm
from overworld_menu import display_main_gui


def main():
    player_health: int = -1 # initial value just so the game starts

    if not mm.display_main_menu(): # if this returns 0 (player chooses quit) then the program ends else it returns 1
        return
    
    while player_health != 0:
        player_health = display_main_gui() # main game loop

if __name__=="__main__":
    main()
