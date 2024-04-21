import json
from datetime import datetime
from character_sheet import player
from item_sheet import every_item


def save(player: object, map: object): #TODO: add map saving
    """
    saves content to a .json file
    creates a new one every time and names it automatically based on system time
    """
    player_info = player.__dict__
    player_info["weapon"] ="obj_" + player.weapon.name
    player_info["armor"] = "obj_" + player.armor.name
    player_info["shield"] = "obj_" + player.shield.name
    # creates a new dictionary with class names instead of classes(python classes cannot be saved into the json file)
    keynames = ["obj_" + key.name for key in player_info["inventory"].keys()]
    player_info["inventory"] = dict(zip(keynames, list(player_info["inventory"].values())))
    del player_info["menu"]
    del player_info["healthbar"]

    with open(r"saves/" + str(datetime.now()).replace(":", "-") + ".json", "w") as f:
        json_string = json.dumps(player_info, indent=4)
        f.write(json_string) # writing it as a string cuz the formatting is prettier :)
        #json.dump(player_info, f), could also use this


def load(file_path: str):
    held_item_objects = []
    inventory_objects = []

    with open(r"saves/" + file_path, "r") as f:
        data: dict = json.load(f)
    
    for key, value in data.items():
        if isinstance(value, str) and value.startswith("obj_"): # adds all of the items in the weapon, armor, shield slots to a list
            value = value.lstrip("obj_")
            for item in every_item:
                if item.name == value:
                    held_item_objects.append(item)
                    break
            else:
                print("Error: Item not found")
        if isinstance(value, dict) and list(value.keys())[0].startswith("obj_"): # adds all of the items in the inventory to a list
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
    
    #TODO: make all of the other attributes transfer like level, name, money, bools etc.

    # fills all of the player held item slots
    player.weapon = held_item_objects[0]
    player.armor = held_item_objects[1]
    player.shield = held_item_objects[2]
    
    # fills all of the inventory item slots
    player.inventory = dict(zip(inventory_objects, saved_inventory.values()))
    
    #TODO: make this read the data and change the default attributes of the map

