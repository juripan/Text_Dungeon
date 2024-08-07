from random import randint, choice

import item_sheet as itm
from healthbar import Healthbar
from battlemenu import BattleMenu
from color_file import colors


class Character():
    """
    base character class, any living thing inherits this class

    stats (max value is 20 for every stat)
    strength - makes melee weapons do more damage,
    dexterity - makes long ranged weapons deal more damage,
    vigor - raises max hp of character,
    agility - run and dodge chances,
    luck - crit chances
    """
    def __init__(self, name: str, max_health: int, stats: dict[str, int], level: int=0, inventory: dict[itm.Item, int]={}) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.level = level
        self.stats = stats

        for _ in range(self.stats["vigor"] - 1): # initializes the max health and health based on the initial vigor stat
            self.max_health += int(self.max_health * (10/100))
            self.health = self.max_health

        self.weapon = itm.fists
        self.armor = itm.no_armor
        self.shield = itm.no_shield
        self.inventory = inventory

        self.shielded: bool = False
        self.vulnerable: bool = True
    
    def attack_calc(self, other, modifier):
        added_message: str = "!"
        roll = randint(1, 100 - 5 * self.stats["luck"] + 1) # max luck stat is 20, 21 throws an error
        if roll == 1: # critical hit, ignores armor and shielding
            attack_damage = int((self.weapon.damage + self.weapon.damage * (modifier * 5 / 100)) * 3)
            added_message = f", {colors["yellow"]}critical hit!{colors["default"]}"
        else:
            attack_damage = int((self.weapon.damage + self.weapon.damage * (modifier * 5 / 100)) * ((100 - other.armor.resistance * 5) / 100)) # calculates damage based on armor
            if other.shielded:
                attack_damage = int(attack_damage * ((100 - other.shield.sturdiness * 15) / 100)) # if shield is up then lowers the damage
                print(f"{other.name} blocked the attack!")
                 
        other.health -= attack_damage
        other.health = max(other.health, 0) # a barrier so you dont go under 0
        other.healthbar.update_health()
        print(f"{self.name} attacked {other.name} with {self.weapon.name}, {other.name} took {colors["red"]}{attack_damage} damage" + added_message + colors["default"])
    
    def attack(self, other):
        if not other.vulnerable:
            print(f"{self.name}s attack missed!")
        elif not isinstance(self.weapon, itm.RangedWeapon):
            # close range attack, strength buffs by 5 percent for each level (ignores base level)
            Character.attack_calc(self, other, self.stats["strength"] - 1)
        else:
            # ranged attack, dexterity buffs by 5 percent for each level (ignores base level)
            for item in self.inventory: # attempts to find the ammo for the weapon
                if isinstance(item, itm.Ammo) and self.inventory[item] > 0:
                    item.load_weapon(self, self.weapon) # loads the weapon
                    Character.attack_calc(self, other, self.stats["dexterity"] - 1)
                    break
            else:
                print(f"{self.name} ran out of ammo!")
                self.weapon.loaded = False


class Player(Character):
    """
    main player of the game
    """
    def __init__(self, name: str, max_health: int, stats: dict, experience_points: int=0, level: int=0, inventory: dict={}, money: int=0) -> None:
        super().__init__(name, max_health, stats, level, inventory)
        self.money: int = money
        self.experience_points = experience_points
        self.experience_cap = 10 # determines how much exp you need for a level up
        self.level = level
        self.run_success: bool = False
        self.healthbar = Healthbar(self, color="light_blue")
        self.menu = BattleMenu(self)
    
    def block_attack(self):
        self.shielded = True
        print(f"{self.name} braces for the upcoming attack")
    
    def dodge(self):
        roll = randint(1, 40 - 2 * self.stats["agility"] + 1)
        if roll == 1:
            self.vulnerable = False
        print(f"{self.name} attempts to dodge the upcoming attack")
    
    def use_item(self, item, target, targets): 
        """
        self is the player, 
        target is the who its used on (you or the enemy), 
        targets is the whole encounter,
        if targets is None then its triggered from the overworld menu
        """
        if targets is None: # checks of its triggered from the overworld menu
            if not isinstance(item, itm.OffensiveItem):
                item.use(self, target) # target is the player
            else:
                print("Please don't do that to yourself :(")
        elif not isinstance(item, itm.Ammo): # checks of the item is usable
            if hasattr(item, "splash_damage") and item.splash_damage:
                item.use(self, targets)
            else:
                item.use(self, target)
        else:
            print("You cannot use/equip this item")

    def run_from_battle(self, targets: list[object]): # maybe re-balance the running, its too unlikely
        if isinstance(targets[0], Boss):
            print(f"{self.name} tried run away but failed!")
            print("can't run away from the boss!")
            return
        
        threshold: int = 25
        sum_target_level: int = 0
        
        for target in targets: 
            sum_target_level += target.level
        
        roll = randint(0 - sum_target_level, 30) # maybe make it into an average level not a sum
        
        if roll > (threshold - self.stats["agility"] + 1): # + 1 to make base agility not do anything (base is 1)
            self.run_success = True
            print(f"{self.name} ran away successfully!")
        else:
            print(f"{self.name} tried run away but failed!")


class Enemy(Character): #TODO: add magic / spells to the enemy and add more enemy variants (subclasses)
    """
    basic enemy class
    when initialized checks its level and randomly distributes its stats based on its level
    """
    def __init__(self, name: str, max_health: int, stats: dict, level: int=0, inventory: dict={}, money_dropped_on_kill: int=0, exp_dropped_on_kill: int=0) -> None:
        super().__init__(name, max_health, stats, level, inventory)
        self.exp_dropped_on_kill = exp_dropped_on_kill
        self.money_dropped_on_kill = money_dropped_on_kill
        self.healthbar = Healthbar(self, color="red")
    
    def death(self, player, enemies):
        enemies.remove(self)
        player.money += self.money_dropped_on_kill
        player.experience_points += self.exp_dropped_on_kill
        print(f"{self.name} died, {player.name} earned {self.money_dropped_on_kill} gold and {self.exp_dropped_on_kill} experience!")
    
    def deepcopy(self):
        """
        returns a unique object based on itself, used to create a different instance of the same enemy type
        randomizes its stats and returns a new objects with the new stats based on player level
        """
        new_stats = {"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}
        new_level = max(player.level + randint(-1, 2), 0)
        new_exp_dropped_on_kill = int(self.exp_dropped_on_kill + (self.exp_dropped_on_kill * self.level) / 10)
        new_money_dropped_on_kill = int(self.money_dropped_on_kill + (self.money_dropped_on_kill * self.level) / 20)

        for _ in range(new_level):
            random_stat = choice(list(new_stats.keys()))
            new_stats[random_stat] += 1
        
        return self.__class__(name=self.name, max_health=self.max_health, level=new_level, money_dropped_on_kill=new_money_dropped_on_kill, 
                     exp_dropped_on_kill=new_exp_dropped_on_kill, stats = new_stats) # uses self.__class__ so it works with objects that inherit it (doesn't retype them to Enemy class)


class Boss(Enemy):
    def __init__(self, name: str, max_health: int, stats: dict, level: int = 0, inventory: dict = {}, 
                 money_dropped_on_kill: int = 0, exp_dropped_on_kill: int = 0, special_attack_cooldown: int = 10) -> None:
        super().__init__(name, max_health, stats, level, inventory, money_dropped_on_kill, exp_dropped_on_kill)
        self.special_attack_cooldown: int = special_attack_cooldown # number of turns
    
    def special_attack(): # TODO: add special attacks
        pass


player = Player(name="Player", max_health=1000, stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1},  level=0,
                inventory={itm.small_health: 3, itm.bomb: 3, itm.dagger: 1, itm.iron_armor: 1, itm.iron_shield: 1, itm.bow: 1, itm.wooden_arrow: 5, itm.leather_armor: 1, itm.flint_arrow: 3, itm.throwing_knives: 5})

bat = Enemy(name="Bat", max_health=100, stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}, 
            level=0, money_dropped_on_kill=20, exp_dropped_on_kill=20)
skeleton = Enemy(name="Skeleton", max_health=300, stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}, 
                 level=0, money_dropped_on_kill=40, exp_dropped_on_kill=40)
slime = Enemy(name="Slime", max_health=200, stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1},
              level=0, money_dropped_on_kill=30, exp_dropped_on_kill=30)

slime_king = Boss(name="Slime King", max_health=500, stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}, 
                  level=0, money_dropped_on_kill=60, exp_dropped_on_kill=60, special_attack_cooldown=15)

skeleton_king = Boss(name="Skeleton King", max_health=500, stats={"strength": 1, "dexterity": 1, "vigor": 1, "agility": 1, "luck": 1}, 
                  level=0, money_dropped_on_kill=60, exp_dropped_on_kill=60, special_attack_cooldown=15)


all_enemies: tuple = (bat, skeleton, slime) # all implemented enemies are here

all_bosses: tuple = (slime_king, skeleton_king) # all implemented bosses are here
