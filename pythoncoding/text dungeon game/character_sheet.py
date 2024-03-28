from random import randint

import item_sheet as itm
from healthbar import Healthbar
from menu import BattleMenu

class Character():
    """
    base character class, any living thing inherits this class

    stats (max value is 20 for every stat)
    strength - makes meelee weapons do more damage TODO
    dexterity - makes long ranged weapons deal more damage TODO
    vigor - raises max hp of character
    agility - run and dodge chances
    luck - crit chances
    """
    def __init__(self, name: str, max_health: int, level: int=0, inventory: dict={}, 
                 stats: dict={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.level = level
        self.stats = stats

        for i in range(self.stats["vigor"] - 1): # initializes the max health and health based on the initial vigor stat
            self.max_health += int(self.max_health * (20/100))
            self.health = self.max_health

        self.weapon = itm.fists
        self.armor = itm.no_armor
        self.shield = itm.no_shield
        self.inventory = inventory

        self.shielded: bool = False
        self.vulnerable: bool = True

    def attack(self, other):
        if other.vulnerable:
            added_message = "!"
            roll = randint(1, 100 - 5 * self.stats["luck"] + 1) # max luck stat is 20, 21 throws an error
            if roll == 1: # critical hit, ignores armor and shielding
                attack_damage = self.weapon.damage * 3
                added_message = ", critical hit!"
            
            else:
                attack_damage = int(self.weapon.damage * ((100 - other.armor.resistance * 5) / 100)) # calculates damage based on armor
                if other.shielded:
                    attack_damage = int(attack_damage * ((100 - other.shield.sturdiness * 15) / 100)) # if shield is up then lowers the damage
                    print(f"{other.name} blocked the attack!")
                    other.shielded = False # resets the shield, TODO: should be reset at start of new turn not here, currently only blocks the first attack
            
            other.health -= attack_damage
            other.health = max(other.health, 0) # a barrier so you dont go under 0
            other.healthbar.update_health()
            print(f"{self.name} attacked {other.name} with {self.weapon.name}, {other.name} took {attack_damage} damage" + added_message)
        else:
            print(f"{self.name}s attack missed!")
            other.vulnerable = True


class Player(Character):
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, experience_points: int=0, level: int=0, inventory: dict={}, 
                 stats: dict={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}, money: int=0) -> None:
        super().__init__(name, max_health, level, inventory, stats)
        self.money: int = money
        self.experience_points = experience_points
        self.experience_cap = 10 # determies how much exp you need for a level up
        self.level = level
        self.run_success: bool = False
        self.healthbar = Healthbar(self)
        self.menu = BattleMenu(self)
    
    def block_attack(self):
        self.shielded = True
        print(f"{self.name} braces for the upcoming attack")
    
    def dodge(self):
        roll = randint(1, 40 - 2 * self.stats["agility"] + 1) #TODO: should probably dodge any attack in that turn
        if roll == 1:
            self.vulnerable = False
        print(f"{self.name} attempts to dodge the upcoming attack")
    
    def use_item(self, item, target): #self is the player, target is the who its used on (you or the enemy)
        if item in self.inventory and self.inventory.get(item) > 0:
            item.use(self, target)
        else:
            print(f"{self.name} ran out of {item.name}")
    
    def run_from_battle(self, targets):
        threshold: int = 25
        sum_target_level: int = 0
        for target in targets: sum_target_level += target.level
        roll = randint(0 - sum_target_level, 30) # makes it less likely to run depending on the enemy levels maybe make it into an average level not a sum
        if roll > (threshold - self.stats["agility"] + 1): # + 1 to make base agility not do anything (base is 1)
            self.run_success = True
            print(f"{self.name} ran away successfully!")
        else:
            print(f"{self.name} tried run away but failed!")


class Enemy(Character): #TODO: add magic / spells to the enemy and add more enemy variants (subclasses)
    """
    basic enemy class
    """
    def __init__(self, name: str, max_health: int, level: int=0, inventory: dict={}, 
                 stats: dict={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1},
                 money_dropped_on_kill: int=0, exp_dropped_on_kill: int=0) -> None:
        super().__init__(name, max_health, level, inventory, stats)
        self.healthbar = Healthbar(self)
        self.money_dropped_on_kill = money_dropped_on_kill
        self.exp_dropped_on_kill = exp_dropped_on_kill
    
    def death(self, player, enemies):
        enemies.remove(self)
        player.money += self.money_dropped_on_kill
        player.experience_points += self.exp_dropped_on_kill
        print(f"{self.name} died, {player.name} earned {self.money_dropped_on_kill} gold and {self.exp_dropped_on_kill} experience!")


player = Player(name="Player", max_health=1000, 
                inventory={itm.small_health: 3, itm.bomb: 3, itm.dagger: 1, itm.iron_armor: 1, itm.iron_shield: 1}, 
                stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1})
enemy1 = Enemy(name="Ur mom", max_health=100, level=2, money_dropped_on_kill=20, exp_dropped_on_kill=20, 
               stats = {"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1})
enemy2 = Enemy(name="Ur dad", max_health=300, level=4, money_dropped_on_kill=40, exp_dropped_on_kill=40,
               stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1})

enemies = [enemy1, enemy2] # all attackable enemies are here
