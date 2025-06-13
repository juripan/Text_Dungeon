# this file manages the overworld map gui and shop gui and functions like buying and selling and the generation of the next floor
from random import randint, choices
import os

from character_sheet import player, Player
from saveandload import save
from map import Map, current_map, floor_counter
import battle_manager as bm
import item_sheet as itm


def next_floor():
    """
    asks the player if they want to leave,
    triggered when entering the bossroom after defeating the boss,
    """
    global current_map, shop_content, floor_counter
    #TODO: refactor this mess (refactor the map and shop content being global and make it nicer in general)
    print("Do you want to move to the next floor?(y/n)")
    print("(note: you cant come back here if you leave)")
    choice = input(">").lower()
    if choice == "y":
        current_map, shop_content, floor_counter = generate_floor()


def generate_floor():
    """
    generates the floor (based on the number of floors played in a run) and its shop content
    """
    current_map = Map(30 * floor_counter, 30 * floor_counter, max_room_count = 10 * floor_counter)
    current_map.generate_map(density=5 * floor_counter)
    current_map.crop_map()
    current_map.create_special_rooms()

    shop_content = generate_shop_stock()
    return (current_map, shop_content, floor_counter + 1)


def generate_shop_stock() -> dict[itm.Item, int]:
    """
    generates the shops stock,
    should be ran only at the start of the floor,
    returns a dictionary containing the shop stock
    """
    keys_equipable: list[itm.Item] = choices(itm.equipables, k=2)
    keys_consumable: list[itm.Item] = choices(itm.consumables, k=4)

    shop_content: dict[itm.Item, int] = {key: randint(1, 2) for key in keys_equipable}
    shop_content.update({key: randint(1, 10) for key in keys_consumable})
    return shop_content


def buy_item(item: itm.Item, shop_content: dict) -> None:
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


def buy_menu(shop_content: dict) -> None:
    while shop_content:
        print("Which item would you like to buy? (back or ..)")
        print(f"Your money: {player.money} gold")

        longest_item_len: int = len(max(shop_content.keys(), key=lambda x: len(x.name)).name)
        formatting_string: str = "{:<2} {:<" + str(longest_item_len) + "} {:>6} {:>10}"

        print("─" * 50)
        print(formatting_string.format("id", 'Name', 'Amount', 'Value(g)'))
        for i, key_value in enumerate(shop_content.items()):
            print(formatting_string.format(i + 1, key_value[0].name, key_value[1], str(key_value[0].cost) + " gold"))
        print("─" * 50)
        choice = input(">").lower()

        if choice == "back" or choice == "..":
            os.system("cls")
            break

        for i, key in enumerate(shop_content.keys()):
            if choice == key.name.lower() or choice == str(i + 1):
                os.system("cls")
                buy_item(key, shop_content)
                break
        else:
            os.system("cls")
            print("Item not in inventory")
    shop_menu()


def sell_item(item: itm.Item, sell_percentage_value: int) -> None:
        if player.inventory[item] == 0:
            print("you dont have that item")
            return
        money_earned = int(item.cost * (sell_percentage_value / 100))
        player.inventory[item] -= 1
        if player.inventory[item] == 0:
            player.inventory.pop(item)
        player.money += money_earned


def sell_menu() -> None:
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
            os.system("cls")
            break

        for i, key in enumerate(player.inventory.keys()):
            if choice == key.name.lower() or choice == str(i + 1):
                os.system("cls")
                sell_item(key, sell_percentage_value)
                break
        else:
            os.system("cls")
            print("Item not in inventory")
    shop_menu()


def shop_menu() -> None:
    """
    shows the shop menu and handles the inputs,
    returns: None
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
    if choice == "buy" or choice == "1":
        os.system("cls")
        buy_menu(shop_content)
    elif choice == "sell" or choice == "2":
        os.system("cls")
        sell_menu()
    elif choice == "back" or choice == "..":
        os.system("cls")
        print("Goodbye!")
    else:
        os.system("cls")
        print("Not included in the list of commands")
        shop_menu()


def move_player(map_object: Map, direction: str) -> None:
        """
        moves the player,
        prints 'cant move there' if its out of the map or out of the room layout,
        returns: None
        """
        os.system("cls")
        x, y = map_object.player_pos
        if map_object.map_layout[y][x][0] in (map_object.NORMAL_ROOM, map_object.BOSS_ROOM):
            map_object.map_layout[y][x] = map_object.map_layout[y][x][0] + map_object.EXPLORED_ROOM
        else:
            map_object.map_layout[y][x] = map_object.map_layout[y][x][:2]
        
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

        #events that trigger after entering a room
        if map_object.map_layout[y][x][:2] == map_object.NORMAL_ROOM + map_object.UNEXPLORED_ROOM:
            roll = randint(1, 3)
            if roll == 1:
                bm.battle_loop(boss=False)
            map_object.map_layout[y][x] = map_object.NORMAL_ROOM + map_object.EXPLORED_ROOM + map_object.PLAYER_IN_ROOM
        elif map_object.map_layout[y][x][0] == map_object.BOSS_ROOM:
            if map_object.map_layout[y][x][1] == map_object.UNEXPLORED_ROOM:
                bm.battle_loop(boss=True)
            else:
                next_floor()
        elif map_object.map_layout[y][x][0] == map_object.SHOP_ROOM:
            shop_menu()


def overworld_inv_menu(player: Player):
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
        return display_main_gui()
    
    for i, item in enumerate(player.inventory):
        if choice == item.name.lower() or choice == str(i + 1):
            player.use_item(item, target=player, targets=None) # no targets here
            break
    else: # if not in the inv
        print("not in the item list")


def display_main_gui() -> int | None:
    """
    displays the map and the gui of the overworld,
    returns: player.health for the game loop in the main function,
    """
    current_map.draw_map()
    print("─" * 50)
    player.healthbar.display_health()
    print("what do you want to do?")
    print("('wasd' + enter to move, 'save' to save the game,'quit' to exit the game(dont forget to save),  'i' to access inventory)")
    choice = input(">").lower()
    if choice == "save":
        save(player, current_map)
    elif choice in ("w", "a", "s", "d"):
        move_player(map_object=current_map, direction=choice)
        return player.health
    elif choice == "i":
        overworld_inv_menu(player)
    elif choice == "quit":
        print("Goodbye!")
        exit()
    else:
        os.system("cls")
        print("not in the list of commands")


current_map, shop_content, floor_counter =  generate_floor() #triggered after starting the game to generate the floor and shop
