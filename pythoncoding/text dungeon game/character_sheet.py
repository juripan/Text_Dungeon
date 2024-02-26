import weapon_sheet as ws
from healthbar import Healthbar


class Character(): #TODO: implement dying, cuz everyone is invincible now
    """
    base character class, any living thing inherits this calss
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.weapon = ws.fists
        self.vulnerable = True
        self.inventory = inventory
    
    def attack(self, other):
        if other.vulnerable:
            other.health -= self.weapon.damage
            other.health = max(other.health, 0) # a barrier so you dont go under 0
            other.healthbar.update()
            print(f"{self.name} attacked {other.name} with {self.weapon.name}, {other.name} took {self.weapon.damage} damage!")
        else:
            print(f"{self.name}s attack does nothing")
        other.healthbar.display_health()


class Player(Character): #TODO: add swapping weapons, like an equip function that takes from the inventory
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        super().__init__(name, max_health, inventory)
        self.healthbar = Healthbar(self)
    
    def block_attack(self):
        self.vulnerable = False
        print(f"{self.name} blocks the upcoming attack")
    
    def use_item(self, item): #TODO: make this method universal for all items that are in the inv, like equipping weapons
        if item in self.inventory and self.inventory.get(item) > 0:
            self.health += item.heal_amount
            self.health = min(self.health, self.max_health) # a barrier so you dont go over max health
            self.inventory[item] -= 1
            self.healthbar.update()
            print(f"{self.name} used {item.name}, +{item.heal_amount} health")
        else:
            print(f"{self.name} ran out of {item.name}")
        self.healthbar.display_health()


class Enemy(Character):
    """
    basic enemy class
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        super().__init__(name, max_health, inventory)
        self.healthbar = Healthbar(self)
