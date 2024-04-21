# add more items like potions

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


class RangedWeapon(Weapon):
    def __init__(self, name: str, damage: int, damage_type: str, weapon_range: str, cost: int) -> None:
        super().__init__(name, damage, damage_type, cost)
        self.weapon_range = weapon_range
        self.loaded = False # default False, saves the type of ammo that is loaded into the weapon
    
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
    
    def use(self, user, target): # target isn't used cuz the user is the target automatically
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
    
    def use(self, user, target): # target isn't used cuz the user is the target automatically
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
    
    def use(self, user, target): # note: you can heal anyone and I mean ANYONE, even an enemy
        if user.inventory.get(self) > 0:
            healed = target.max_health * self.heal_amount // 100
            target.health += healed
            target.health = min(target.health, target.max_health) # a barrier so you dont go over max health
            user.inventory[self] -= 1
            target.healthbar.update_health()
            print(f"{user.name} used {self.name}, and healed {target.name} by {healed} health")
        else:
            print(f"{user.name} ran out of {self.name}")


class Ammo(Item):
    def __init__(self, name: str, cost: int, piercing: int) -> None:
        super().__init__(name, cost)
        self.piercing = piercing
    
    def load_weapon(self, user, weapon) -> int:
        if weapon.loaded != self:
            weapon.damage += int(weapon.damage * ((self.piercing * 5) / 100))
            user.inventory[self] -= 1
            weapon.loaded = self
        elif weapon.loaded:
            user.inventory[self] -= 1


class OffensiveItem(Item): # goes through armor on purpose, TODO: maybe make it deal damage to all enemies at once instead
    def __init__(self, name: str, cost: int, damage: int) -> None:
        super().__init__(name, cost)
        self.damage = damage
    
    def use(self, user, target):
        if user.inventory.get(self) > 0:
            target.health -= self.damage
            target.health = max(target.health, 0) # a barrier so you dont go under 0
            user.inventory[self] -= 1
            target.healthbar.update_health()
            print(f"{user.name} used {self.name}, and dealt {self.damage} damage to {target.name}")
        else:
            print(f"{user.name} ran out of {self.name}")


fists = Weapon(name="Fists", damage=10, damage_type="bludgeoning", cost=None)

iron_sword = Weapon(name="Iron sword", damage=50, damage_type="slashing", cost=None)

dagger = Weapon(name="Dagger", damage=35, damage_type="piercing", cost=None)


bow = RangedWeapon(name="Bow", damage=40, damage_type="piercing", weapon_range="long", cost=None)

short_bow = RangedWeapon(name="Short bow", damage=30, damage_type="piercing", weapon_range="mid", cost=None)


no_armor = Armor(name="No armor", resistance=0, cost=None)

leather_armor = Armor(name="Leather armor", resistance=1, cost=None)

chainmail_armor = Armor(name="Chainmail armor", resistance=2, cost=None)

iron_armor = Armor(name="Iron armor", resistance=6, cost=None)


no_shield = Shield(name="No shield", sturdiness=0, cost=None)

wooden_shield = Shield(name="Wooden shield", sturdiness=2, cost=None)

iron_shield = Shield(name="Iron shield", sturdiness=4, cost=None)


wooden_arrow = Ammo(name="Wooden arrow", piercing=1, cost=None)

flit_arrow = Ammo(name="Flint arrow", piercing=3, cost=None)


small_health = HealingItem(name="Small potion of healing", heal_amount=20, cost=None)

medium_health = HealingItem(name="Potion of healing", heal_amount=50, cost=None)

big_health = HealingItem(name="Big potion of healing", heal_amount=70, cost=None)

bomb = OffensiveItem(name="Bomb", damage=80, cost=None)

dynamite = OffensiveItem(name="Stick of dynamite", damage=50, cost=None)


every_item = [fists, iron_sword, dagger, 
              bow, short_bow, 
              no_armor, leather_armor, chainmail_armor, iron_armor, 
              no_shield, wooden_shield, iron_shield, 
              wooden_arrow, flit_arrow,
              small_health, medium_health, big_health,
              bomb, dynamite]
