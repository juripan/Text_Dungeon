from character_sheet import player
from saveandload import save
from map import new_map


def display_overworld_menu():
    new_map.draw_map()
    print("─" * 50)
    player.healthbar.display_health()
    print("what do you want to do?")
    print("('wasd' + enter to move, 'save' + enter to save the game)")
    choice = input(">").lower()
    if choice == "save":
        save(player, new_map)
    elif choice in ("w", "a", "s", "d"):
        new_map.move_player(choice)
    else:
        print("not in the list of commands")
    display_overworld_menu() #TODO: remove the recursion, replace with a while loop (to avoid recursion errors)
