from character_sheet import player
from saveandload import save
from map import new_map


def overworld_inv_menu(player):
    """
    displays every item in inventory,
    used in the overworld menu,
    passes the targets=None value to  player.use_item method to indicate where its being called from
    """
    print("─" * 50)
    for i, item in enumerate(player.inventory):
        print(f"{i + 1}. {item.name}: {player.inventory.get(item)}")
    print("─" * 50)

    print("Use or equip/unequip item: ")
    choice = input(">").lower()
    if choice == "back" or choice == "..":
        return display_overworld_menu()
    
    for i, item in enumerate(player.inventory):
        if choice == item.name.lower() or choice == str(i + 1):
            player.use_item(item, target=player, targets=None) # no targets here
            break
    else: # if not in the inv
        print("not in the item list")


def display_overworld_menu() -> int:
    """
    displays the map and the gui of the overworld,
    returns: player.health for the game loop in the main function,
    """
    new_map.draw_map()
    print("─" * 50)
    player.healthbar.display_health()
    print("what do you want to do?")
    print("('wasd' + enter to move, 'save' + enter to save the game, 'i' + enter to access inventory)")
    choice = input(">").lower()
    if choice == "save":
        save(player, new_map)
    elif choice in ("w", "a", "s", "d"):
        new_map.move_player(choice)
        return player.health
    elif choice == "i":
        overworld_inv_menu(player)
    else:
        print("not in the list of commands")
