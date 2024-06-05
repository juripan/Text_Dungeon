# file containing functions that save and load game state (player and map data) into a JSON file
import json
from datetime import datetime

from character_sheet import player
from item_sheet import every_item
from healthbar import Healthbar
from map import new_map
from battlemenu import BattleMenu


def save(player: object, map: object):
    """
    saves content to a .json file
    creates a new one every time and names it automatically based on system time
    """

    player_info = player.__dict__
    player_info["weapon"] ="obj_" + player.weapon.name
    player_info["armor"] = "obj_" + player.armor.name
    player_info["shield"] = "obj_" + player.shield.name
    # creates a new dictionary with class names instead of classes(python classes cannot be saved into the JSON file)
    keynames = ["obj_" + key.name for key in player_info["inventory"].keys()]
    player_info["inventory"] = dict(zip(keynames, list(player_info["inventory"].values())))
    menu_buffer =  player_info["menu"]
    healthbar_buffer = player_info["healthbar"]

    del player_info["menu"]
    del player_info["healthbar"]

    map_info = map.__dict__

    with open(r"pythoncoding\text dungeon game\saves\\" + str(datetime.now()).replace(":", "-") + ".json", "w") as f:
        json_string = json.dumps([player_info, map_info], indent=4)
        f.write(json_string) # writing it as a string cuz the formatting is prettier :)
    
    # gives the attributes back to the player, has to be deleted because the save doesn't work otherwise (JSON and objects dont mix)
    player_info["menu"] = menu_buffer
    player_info["healthbar"] = healthbar_buffer


def load(file_name: str):
    held_item_objects = []
    inventory_objects = []

    with open(r"pythoncoding\text dungeon game\saves\\" + file_name, "r") as f:
        data: list[dict, dict] = json.load(f)
    
    player.__dict__ = data[0]
    player.healthbar = Healthbar(player, color="light_blue")
    player.menu = BattleMenu(player)

    for key, value in data[0].items():
        if isinstance(value, str) and value.startswith("obj_"): # adds all of the items in the weapon, armor, shield slots to a list
            value = value.lstrip("obj_")
            for item in every_item:
                if item.name == value:
                    held_item_objects.append(item)
                    break
            else:
                print("Error: Item not found")
        elif isinstance(value, dict) and list(value.keys())[0].startswith("obj_"): # adds all of the items in the inventory to a list
            saved_inventory = value
            for key in saved_inventory.keys():
                key: str = key.lstrip("obj_")
                for item in every_item:
                    if item.name == key:
                        print("found", item.name)
                        inventory_objects.append(item)
                        break
                else:
                    print("Error: Item not found")
    
    player.inventory = dict(zip(inventory_objects, saved_inventory.values()))

    player.weapon = held_item_objects[0]
    player.armor = held_item_objects[1]
    player.shield = held_item_objects[2]

    new_map.__dict__ = data[1]
