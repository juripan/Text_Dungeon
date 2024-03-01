from random import randint

import item_sheet as itm
from healthbar import Healthbar
from menu import Menu

class Character(): #TODO: add a stats attribute to Character class
    """
    base character class, any living thing inherits this class
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.weapon = itm.fists
        self.armor = itm.no_armor
        self.shield = itm.no_shield
        self.shielded: bool = False
        self.vulnerable: bool = True
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
            print(f"{self.name}s attack missed")
            other.vulnerable = True


class Player(Character):
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}, money: int=0) -> None:
        super().__init__(name, max_health, inventory)
        self.money = money
        self.healthbar = Healthbar(self)
        self.menu = Menu(self)
    
    def block_attack(self):
        self.shielded = True
        print(f"{self.name} braces for the upcoming attack")
    
    def dodge(self):
        print(f"{self.name} attempts to dodge the upcoming attack")
        roll = randint(0 ,6)
        if roll == 6:
            self.vulnerable = False
    
    def use_item(self, item, target): #self is the player, target is the who its used on (you or the enemy)
        if item in self.inventory and self.inventory.get(item) > 0:
            item.use(self, target)
        else:
            print(f"{self.name} ran out of {item.name}")       


class Enemy(Character):
    """
    basic enemy class
    """
    def __init__(self, name: str, max_health: int, inventory: dict={}, money_dropped_on_kill: int=0) -> None:
        super().__init__(name, max_health, inventory)
        self.healthbar = Healthbar(self)
        self.money_dropped_on_kill = money_dropped_on_kill


player = Player(name="Player", max_health=1000, 
                inventory={itm.small_health: 3, itm.bomb: 3, itm.dagger: 1, itm.iron_armor: 1, itm.iron_shield: 1})
enemy1 = Enemy(name="Ur mom", max_health=500)
enemy2 = Enemy(name="Ur dad", max_health=700)

enemies = [enemy1, enemy2] # all attackable enemies are here
