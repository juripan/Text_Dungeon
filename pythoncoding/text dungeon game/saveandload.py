#TODO: add map saving and loading
import json
from datetime import datetime

from character_sheet import player
from item_sheet import every_item


def save(player: object, map: object):
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


def load(file_name: str):
    held_item_objects = []
    inventory_objects = []

    with open(r"saves/" + file_name, "r") as f:
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
    
    # fills all of the player held item slots
    player.name = data["name"]
    player.max_health = data["max_health"]
    player.health = data["health"]
    player.level = data["level"]
    player.stats = data["stats"]

    player.weapon = held_item_objects[0]
    player.armor = held_item_objects[1]
    player.shield = held_item_objects[2]
    
    # fills all of the inventory item slots
    player.inventory = dict(zip(inventory_objects, saved_inventory.values()))
    
    player.shielded = data["shielded"]
    player.vulnerable = data["vulnerable"]
    player.money = data["money"]
    player.experience_points = data["experience_points"]
    player.experience_cap = data["experience_cap"]
    player.run_success = data["run_success"]
    
    """
    for i in range(player.stats["vigor"]): # might not be needed here if the max hp gets saved correctly and it doesn't need to be reinitialized
        player.max_health += int(player.max_health * (10/100))
        player.healthbar.update_max_health() # updates max health so the healthbar is synced up
    """
    #TODO: make this read the data and change the default attributes of the map

