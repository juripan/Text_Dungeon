from color_file import colors
from character_sheet import Character, Player, Enemy

class Item():
    """
    base item class
    any item inherits this class
    """
    def __init__(self, name: str, cost: int) -> None:
        self.name = name
        self.cost = cost


class Weapon(Item):
    def __init__(self, name: str, damage: int, damage_type: str, cost: int) -> None:
        super().__init__(name, cost)
        self.damage = damage
        self.damage_type = damage_type
    
    def use(self, user: Character, target: Character): # target isn't used cuz the user is the target automatically, still defined so it doesn't raise an error
        if user.weapon == self: # if you already have it equipped it unequips the item
            print(f"{user.name} unequipped {user.weapon.name}")
            user.inventory[user.weapon] += 1
            user.weapon = fists
            return
        
        if user.weapon in user.inventory:
            user.inventory[user.weapon] += 1 # puts the weapon back into the inventory
        user.weapon = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class RangedWeapon(Weapon):
    def __init__(self, name: str, damage: int, damage_type: str, weapon_range: str, cost: int) -> None:
        super().__init__(name, damage, damage_type, cost)
        self.weapon_range = weapon_range
        self.loaded: Ammo | bool = False # default False, saves the type of ammo that is loaded into the weapon
    
    def use(self, user, target): # target isn't used cuz the user is the target automatically, still defined so it doesn't raise an error
        if user.weapon == self: # if you already have it equipped it unequips the item
            print(f"{user.name} unequipped {user.weapon.name}")
            user.inventory[user.weapon] += 1
            user.weapon = fists
            return

        if user.weapon in user.inventory:
            user.inventory[user.weapon] += 1 # puts the weapon back into the inventory
        user.weapon = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class Armor(Item):
    def __init__(self, name: str, cost: int, resistance: int) -> None:
        super().__init__(name, cost)
        self.resistance = resistance
    
    def use(self, user: Character, _target): # target isn't used cuz the user is the target automatically, still defined so it doesn't raise an error
        if user.armor == self: # if you already have it equipped it unequips the item
            print(f"{user.name} unequipped {user.armor.name}")
            user.inventory[user.armor] += 1
            user.armor = no_armor
            return

        if user.armor in user.inventory:
            user.inventory[user.armor] += 1 # puts the item back into the inventory
        user.armor = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class Shield(Item):
    def __init__(self, name: str, cost: int, sturdiness: int) -> None:
        super().__init__(name, cost)
        self.sturdiness = sturdiness
    
    def use(self, user: Character, _target): # target isn't used cuz the user is the target automatically, still defined so it doesn't raise an error
        if user.shield == self: # if you already have it equipped it unequips the item
            print(f"{user.name} unequipped {user.shield.name}")
            user.inventory[user.shield] += 1
            user.shield = no_shield
            return

        if user.shield in user.inventory:
            user.inventory[user.shield] += 1 # puts the weapon back into the inventory
        user.shield = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class HealingItem(Item):
    """
    heal_amount: int - a percentage of target health that gets healed
    """
    def __init__(self, name: str, cost: int, heal_amount: int) -> None:
        super().__init__(name, cost)
        self.heal_amount = heal_amount
    
    def use(self, user: Character, target: Player | Enemy): # note: you can heal anyone and I mean ANYONE, even an enemy
        if user.inventory.get(self) > 0:
            healed = target.max_health * self.heal_amount // 100
            target.health += healed
            target.health = min(target.health, target.max_health) # a barrier so you dont go over max health
            user.inventory[self] -= 1
            if user.inventory[self] == 0:
                user.inventory.pop(self)
            target.healthbar.update_health()
            print(f"{user.name} used {self.name}, and healed {target.name} by {colors["green"]}{healed} health{colors["default"]}")
        else:
            print(f"{user.name} ran out of {self.name}")


class Ammo(Item):
    def __init__(self, name: str, cost: int, piercing: int) -> None:
        super().__init__(name, cost)
        self.piercing = piercing
    
    def load_weapon(self, user: Character, weapon: RangedWeapon):
        if weapon.loaded != self:
            weapon.damage += int(weapon.damage * ((self.piercing * 5) / 100))
            user.inventory[self] -= 1
            weapon.loaded = self
        elif weapon.loaded:
            user.inventory[self] -= 1
        
        if user.inventory[self] == 0:
            user.inventory.pop(self)


class OffensiveItem(Item): #note: ignores armor
    def __init__(self, name: str, cost: int, damage: int, splash_damage: bool) -> None:
        super().__init__(name, cost)
        self.damage = damage
        self.splash_damage = splash_damage
    
    def use(self, user: Character, target):
        if user.inventory.get(self) > 0:
            if self.splash_damage:
                for enemy in target:
                    enemy.health -= self.damage
                    enemy.health = max(enemy.health, 0) # a barrier so you dont go under 0
                    enemy.healthbar.update_health()
                    print(f"{user.name} used {self.name}, and dealt {colors["red"]}{self.damage} damage{colors["default"]} to {enemy.name}!")
            else:
                target.health -= self.damage
                target.health = max(target.health, 0) # a barrier so you dont go under 0
                target.healthbar.update_health()
                print(f"{user.name} used {self.name}, and dealt {colors["red"]}{self.damage} damage{colors["default"]} to {target.name}!")
            
            user.inventory[self] -= 1
            if user.inventory[self] == 0:
                user.inventory.pop(self)
        else:
            print(f"{user.name} ran out of {self.name}")


fists = Weapon(name="Fists", damage=10, damage_type="bludgeoning", cost=0)

iron_sword = Weapon(name="Iron sword", damage=50, damage_type="slashing", cost=20)

dagger = Weapon(name="Dagger", damage=35, damage_type="piercing", cost=10)


bow = RangedWeapon(name="Bow", damage=40, damage_type="piercing", weapon_range="long", cost=30)

short_bow = RangedWeapon(name="Short bow", damage=30, damage_type="piercing", weapon_range="mid", cost=15)


no_armor = Armor(name="No armor", resistance=0, cost=0)

leather_armor = Armor(name="Leather armor", resistance=1, cost=10)

chainmail_armor = Armor(name="Chainmail armor", resistance=2, cost=15)

iron_armor = Armor(name="Iron armor", resistance=6, cost=25)


no_shield = Shield(name="No shield", sturdiness=0, cost=0)

wooden_shield = Shield(name="Wooden shield", sturdiness=2, cost=10)

iron_shield = Shield(name="Iron shield", sturdiness=4, cost=15)


wooden_arrow = Ammo(name="Wooden arrow", piercing=1, cost=1)

flint_arrow = Ammo(name="Flint arrow", piercing=3, cost=3)


small_health = HealingItem(name="Small potion of healing", heal_amount=20, cost=10)

medium_health = HealingItem(name="Potion of healing", heal_amount=50, cost=20)

big_health = HealingItem(name="Big potion of healing", heal_amount=70, cost=30)


dynamite = OffensiveItem(name="Stick of dynamite", damage=50, splash_damage=True, cost=15)

bomb = OffensiveItem(name="Bomb", damage=80, splash_damage=True, cost=20)

throwing_knives = OffensiveItem(name="Throwing knives", damage=50, splash_damage=False, cost=5)


every_item: tuple = (
    fists, iron_sword, dagger, 
    bow, short_bow, 
    no_armor, leather_armor, chainmail_armor, iron_armor, 
    no_shield, wooden_shield, iron_shield, 
    wooden_arrow, flint_arrow,
    small_health, medium_health, big_health,
    bomb, dynamite, throwing_knives
)

consumables: tuple = (
    wooden_arrow, flint_arrow,
    small_health, medium_health, big_health,
    bomb, dynamite, throwing_knives
)

equipables: tuple = (
    iron_sword, dagger, 
    bow, short_bow, 
    leather_armor, chainmail_armor, iron_armor, 
    wooden_shield, iron_shield
)