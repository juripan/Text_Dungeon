import item_sheet as itm
from healthbar import Healthbar
from menu import Menu

class Character():
    """
    base character class, any living thing inherits this calss
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.weapon = itm.fists
        self.armor = itm.no_armor
        self.shield = itm.no_shield
        self.shielded: bool = False
        self.vulnerable: bool = True # maybe repurpose the vulnerable bool for dodging
        self.inventory = inventory
    
    def death(self): #TODO: implement dying, cuz everyone is invincible now
        pass

    def attack(self, other):
        if other.vulnerable:
            if other.shielded:
                attack_damage = int(self.weapon.damage * ((100 - other.shield.sturdiness * 15) / 100)) # if shield is up then lowers the damage
                print(f"{other.name} blocked the attack!")
                other.shielded = False # resets the shield
            else:
                attack_damage = int(self.weapon.damage * ((100 - other.armor.resistance * 5) / 100)) # calculates damage based on armor
            
            other.health -= attack_damage
            other.health = max(other.health, 0) # a barrier so you dont go under 0
            other.healthbar.update()
            print(f"{self.name} attacked {other.name} with {self.weapon.name}, {other.name} took {attack_damage} damage!")
        else:
            print(f"{self.name}s attack does nothing")


class Player(Character):
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        super().__init__(name, max_health, inventory)
        self.healthbar = Healthbar(self)
        self.menu = Menu(self)
    
    def block_attack(self):
        self.shielded = True
        print(f"{self.name} braces for the upcoming attack")
    
    def use_item(self, item, target): #self is the player, other is the attacker
        if item in self.inventory and self.inventory.get(item) > 0:
            if isinstance(item, itm.HealingItem):
                item.use(self)
            elif isinstance(item, itm.OffensiveItem):
                item.use(self, target)
        else:
            print(f"{self.name} ran out of {item.name}")
    
    def equip(self, item): # used for equiping weapons and armor
        if item in self.inventory:
            if isinstance(item, itm.Weapon):
                self.weapon = item
            elif isinstance(item, itm.Armor):
                self.armor = item
            elif isinstance(item, itm.Shield):
                self.shield = item
            print(f"{self.name} equipped {item.name}")
        else:
            print(f"{self.name} doesnt have {item.name}")


class Enemy(Character):
    """
    basic enemy class
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        super().__init__(name, max_health, inventory)
        self.healthbar = Healthbar(self)
