# main file used for running the whole project
import battle_manager as bm
import mainmenu as mm
from overworld_menu import display_overworld_menu


def main():
    if not mm.display_main_menu(): # if this returns 0 (player chooses quit) then the program ends else it returns 1
        return
    bm.battle_loop()
    bm.battle_loop() # works with multiple battles, player stats and items carry over, enemies get reset


if __name__=="__main__":
    main()
