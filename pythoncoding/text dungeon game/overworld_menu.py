from character_sheet import player
from saveandload import save
from map import Map, new_map
from random import randint, choices
import battle_manager as bm
import item_sheet as itm


def buy_item(item, shop_content):
    if item.cost <= player.money:
        if player.inventory.get(item) is None:
            player.inventory[item] = 0
        
        player.inventory[item] += 1
        shop_content[item] -= 1

        if shop_content[item] == 0:
            shop_content.pop(item)
        
        player.money -= item.cost
    else:
        print("You dont have enough money to buy this item")


def buy_menu():
    #TODO: generate this before the function gets called, one shop stock per floor
    NUMBER_OF_ITEMS: int = 6
    sellable_items: list = [item for item in itm.every_item if item.cost != 0]
    keys: list[object] = choices(sellable_items, k=NUMBER_OF_ITEMS)

    shop_content: dict[object, int] = {key: randint(1, 6) for key in keys}

    while shop_content:
        print("Which item would you like to buy? (back or ..)")
        print(f"Your money: {player.money} gold")

        longest_item_len = len(max(shop_content.keys(), key=lambda x: len(x.name)).name)
        formatting_string = "{:<2} {:<" + str(longest_item_len) + "} {:>6} {:>10}"

        print("─" * 50)
        print(formatting_string.format("id", 'Name', 'Amount', 'Value(g)'))
        for i, key_value in enumerate(shop_content.items()):
            print(formatting_string.format(i + 1, key_value[0].name, key_value[1], str(key_value[0].cost) + " gold"))
        print("─" * 50)
        choice = input(">").lower()

        if choice == "back" or choice == "..":
            break

        for i, key in enumerate(shop_content.keys()):
            if choice == key.name.lower() or choice == str(i + 1):
                buy_item(key, shop_content)
                break
        else:
            print("Item not in inventory")
    shop_menu()


def sell_item(item: object, sell_percentage_value: int):
        if player.inventory[item] == 0:
            print("you dont have that item")
            return
        money_earned = int(item.cost * (sell_percentage_value / 100))
        player.inventory[item] -= 1
        if player.inventory[item] == 0:
            player.inventory.pop(item)
        player.money += money_earned


def sell_menu():
    sell_percentage_value: int = 80
    while player.inventory:
        print("Which item would you like to sell? (exit or ..)")
        print(f"Your money: {player.money} gold")
        longest_item_len = len(max(player.inventory.keys(), key=lambda x: len(x.name)).name)
        formatting_string = "{:<2} {:<" + str(longest_item_len) + "} {:^10} {:>2}"

        print("─" * 50)
        print(formatting_string.format("id", 'Name', 'Amount', 'Value(g)'))
        for i, key_value in enumerate(player.inventory.items()):
            print(formatting_string.format(i + 1, key_value[0].name, key_value[1], str(int(key_value[0].cost * (sell_percentage_value / 100))) + " gold"))
        print("─" * 50)
        choice = input(">").lower()

        if choice == "exit" or choice == "..":
            break

        for i, key in enumerate(player.inventory.keys()):
            if choice == key.name.lower() or choice == str(i + 1):
                sell_item(key, sell_percentage_value)
                break
        else:
            print("Item not in inventory")
    shop_menu()


def shop_menu() -> None:
    """
    shows the shop menu nad handles the inputs,
    returns None
    """
    MESSAGE = "Welcome to the shop! How may I help you?"
    SHOPKEEPER_SPRITE = "(*-*)│"
    SIGN_WIDTH = len(MESSAGE)

    print("┌────────────────────────────────────────┐")
    print("│Welcome to the shop! How may I help you?│")
    print("└────────────────────────────────────────┘")
    print(SHOPKEEPER_SPRITE.center(SIGN_WIDTH))
    print(">BUY    >SELL    >BACK")
    choice = input(">").lower()
    if choice == "buy":
        buy_menu()
    elif choice == "sell":
        sell_menu()
    elif choice == "back" or choice == "..":
        print("Goodbye!")
    else:
        print("Not included in the list of commands")
        shop_menu()


def move_player(map_object: Map, direction: str) -> int | None:
        """
        moves the player,
        prints 'cant move there' if its out of the map or out of the room layout,
        returns: None
        """
        x, y = map_object.player_pos
        if map_object.map_layout[y][x][0] in (map_object.NORMAL_ROOM, map_object.BOSS_ROOM):
            map_object.map_layout[y][x] = map_object.EXPLORED_ROOM
        else:
            map_object.map_layout[y][x] = map_object.map_layout[y][x][0]
        
        if direction == "w" and y > 0 and map_object.map_layout[y - 1][x] != map_object.NO_ROOM:
            y -= 1
        elif direction == "s" and y + 1 < map_object.max_height and map_object.map_layout[y + 1][x] != map_object.NO_ROOM:
            y += 1
        elif direction == "a" and x > 0 and map_object.map_layout[y][x - 1] != map_object.NO_ROOM:
            x -= 1
        elif direction == "d" and x + 1 < map_object.max_width and map_object.map_layout[y][x + 1] != map_object.NO_ROOM:
            x += 1
        else:
            print("cant move there!")
        
        map_object.map_layout[y][x] += map_object.PLAYER_IN_ROOM
        map_object.player_pos = x, y

        if map_object.map_layout[y][x][0] == map_object.NORMAL_ROOM: # player goes to an unexplored room
            roll = randint(1, 3)
            if roll == 1:
                bm.battle_loop(boss=False)
        elif map_object.map_layout[y][x][0] == map_object.BOSS_ROOM:
            bm.battle_loop(boss=True)
        elif map_object.map_layout[y][x][0] == map_object.SHOP_ROOM:
            shop_menu()


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


def display_overworld_menu() -> int | None:
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
        move_player(map_object=new_map, direction=choice)
        return player.health
    elif choice == "i":
        overworld_inv_menu(player)
    else:
        print("not in the list of commands")
