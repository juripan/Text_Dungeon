import item_sheet as itm
from healthbar import Healthbar


class Character(): #TODO: implement dying, cuz everyone is invincible now
    """
    base character class, any living thing inherits this calss
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.weapon = itm.fists
        self.armor = itm.no_armor
        self.vulnerable: bool = True
        self.inventory = inventory
    
    def attack(self, other):
        if other.vulnerable:
            attack_damage = int(self.weapon.damage * ((100 - other.armor.resistance * 5) / 100)) # calculates damage based on armor
            other.health -= attack_damage
            other.health = max(other.health, 0) # a barrier so you dont go under 0
            other.healthbar.update()
            print(f"{self.name} attacked {other.name} with {self.weapon.name}, {other.name} took {attack_damage} damage!")
        else:
            print(f"{self.name}s attack does nothing")
        other.healthbar.display_health()


class Player(Character):
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        super().__init__(name, max_health, inventory)
        self.healthbar = Healthbar(self)
    
    def block_attack(self): # maybe make it block a percentage of damage but not the whole blow, maybe repurpose the vulnerable bool for dodging
        self.vulnerable = False
        print(f"{self.name} braces for the upcoming attack")
    
    def use_item(self, item): # using consumables like potions
        if item in self.inventory and self.inventory.get(item) > 0:
            item.use(self)
        else:
            print(f"{self.name} ran out of {item.name}")
        self.healthbar.display_health()
    
    def equip(self, item): # used for equiping weapons and armor
        if item in self.inventory:
            if isinstance(item, itm.Weapon):
                self.weapon = item
            elif isinstance(item, itm.Armor):
                self.armor = item
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
