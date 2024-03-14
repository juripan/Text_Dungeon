from random import randint

import item_sheet as itm
from healthbar import Healthbar
from menu import BattleMenu

class Character():
    """
    base character class, any living thing inherits this class
    """
    def __init__(self, name: str, max_health: int, level: int=0, inventory: dict={}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.level = level
        self.stats: dict = {"strength": 1, "dexterity": 1, "agility": 1} #TODO: come up with other stats and add away to get more stats after level up

        self.weapon = itm.fists
        self.armor = itm.no_armor
        self.shield = itm.no_shield
        self.inventory = inventory

        self.shielded: bool = False
        self.vulnerable: bool = True

    def attack(self, other):
        if other.vulnerable:
            attack_damage = int(self.weapon.damage * ((100 - other.armor.resistance * 5) / 100)) # calculates damage based on armor
            if other.shielded:
                attack_damage = int(attack_damage * ((100 - other.shield.sturdiness * 15) / 100)) # if shield is up then lowers the damage
                print(f"{other.name} blocked the attack!")
                other.shielded = False # resets the shield
            
            other.health -= attack_damage
            other.health = max(other.health, 0) # a barrier so you dont go under 0
            other.healthbar.update()
            print(f"{self.name} attacked {other.name} with {self.weapon.name}, {other.name} took {attack_damage} damage!")
        else:
            print(f"{self.name}s attack missed!")
            other.vulnerable = True


class Player(Character):
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, experience_points: int=0, level: int=0, inventory: dict={}, money: int=0) -> None:
        super().__init__(name, max_health, level, inventory)
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
        roll = randint(0, 6) # placeholder odds
        if roll == 0:
            self.vulnerable = False
        print(f"{self.name} attempts to dodge the upcoming attack")
    
    def use_item(self, item, target): #self is the player, target is the who its used on (you or the enemy)
        if item in self.inventory and self.inventory.get(item) > 0:
            item.use(self, target)
        else:
            print(f"{self.name} ran out of {item.name}")
    
    def run_from_battle(self):
        roll = randint(0, int(12/self.stats["agility"])) #TODO: maybe change the odds in some way, maybe it could add to the rolled number and then check if its over a threshold in the if statement, or just lower the threshold, also make it scale with enemy level
        if roll == 0:
            self.run_success = True
            print(f"{self.name} ran away successfully!")
        else:
            print(f"{self.name} tried run away but failed!")
    
    def levelup_check(self):
        if self.experience_points >= self.experience_cap: # if you hit the amount of exp you need to level up
            self.experience_points -= self.experience_cap
            self.level += 1
            self.experience_cap = int(self.experience_cap * 9/8) # scales up the amout of exp you need to level up
            print(f"{self.name} reached level {self.level}!")


class Enemy(Character):
    """
    basic enemy class
    """
    def __init__(self, name: str, max_health: int, level: int=0, inventory: dict={}, money_dropped_on_kill: int=0, exp_dropped_on_kill: int=0) -> None:
        super().__init__(name, max_health, level, inventory)
        self.healthbar = Healthbar(self)
        self.money_dropped_on_kill = money_dropped_on_kill
        self.exp_dropped_on_kill = exp_dropped_on_kill
    
    def death(self, player, enemies):
        enemies.remove(self)
        player.money += self.money_dropped_on_kill
        player.experience_points += self.exp_dropped_on_kill
        print(f"{self.name} died, {player.name} earned {self.money_dropped_on_kill} gold and {self.exp_dropped_on_kill} experience!")
        player.levelup_check()


player = Player(name="Player", max_health=1000, 
                inventory={itm.small_health: 3, itm.bomb: 3, itm.dagger: 1, itm.iron_armor: 1, itm.iron_shield: 1})
enemy1 = Enemy(name="Ur mom", max_health=100, level=2, money_dropped_on_kill=20, exp_dropped_on_kill=20)
enemy2 = Enemy(name="Ur dad", max_health=300, level=4, money_dropped_on_kill=40, exp_dropped_on_kill=50)

enemies = [enemy1, enemy2] # all attackable enemies are here
