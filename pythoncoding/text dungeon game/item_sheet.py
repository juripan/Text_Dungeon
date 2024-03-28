# add more items like potions

class Item():
    """
    base item class
    any item iherits this class
    """
    def __init__(self, name: str, cost: int) -> None:
        self.name = name
        self.cost = cost


class Weapon(Item):
    def __init__(self, name: str, damage: int, damage_type: str, cost: int) -> None:
        super().__init__(name, cost)
        self.damage = damage
        self.damage_type = damage_type
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically, still defined so it doesnt raise an error
        if user.weapon in user.inventory:
            user.inventory[user.weapon] += 1 # puts the weapon back into the inventory
        user.weapon = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class RangedWeapon(Weapon):
    def __init__(self, name: str, damage: int, damage_type: str, weapon_range: str, cost: int) -> None:
        super().__init__(name, damage, damage_type, cost)
        self.weapon_range = weapon_range
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically, still defined so it doesnt raise an error
        if user.weapon in user.inventory:
            user.inventory[user.weapon] += 1 # puts the weapon back into the inventory
        user.weapon = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class Armor(Item):
    def __init__(self, name: str, cost: int, resistance: int) -> None:
        super().__init__(name, cost)
        self.resistance = resistance
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically
        if user.armor in user.inventory:
            user.inventory[user.armor] += 1 # puts the item back into the inventory
        user.armor = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class Shield(Item):
    def __init__(self, name: str, cost: int, sturdiness: int) -> None:
        super().__init__(name, cost)
        self.sturdiness = sturdiness
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically
        if user.shield in user.inventory:
            user.inventory[user.shield] += 1 # puts the weapon back into the inventory
        user.shield = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class HealingItem(Item):
    def __init__(self, name: str, cost: int, heal_amount: int) -> None:
        super().__init__(name, cost)
        self.heal_amount = heal_amount
    
    def use(self, user, target): # you can heal anyone and I mean ANYONE, even an enemy
        target.health += self.heal_amount
        target.health = min(target.health, target.max_health) # a barrier so you dont go over max health
        user.inventory[self] -= 1
        target.healthbar.update_health()
        print(f"{user.name} used {self.name}, and healed {target.name} by {self.heal_amount} health")


class Ammo(Item):
    def __init__(self, name: str, cost: int, piercing: int) -> None:
        super().__init__(name, cost)
        self.piercing = piercing
    
    def use(self, user, weapon) -> int: #TODO: if used from the inv creates an error
        weapon.damage += int(weapon.damage * ((self.piercing * 5) / 100))
        user.inventory[self] -= 1
        return int(weapon.damage * ((self.piercing * 5) / 100)) # returns it so the attack method can subtract it after firing


class OffensiveItem(Item): # goes through armor on purpose, TODO: maybe make it deal damage to all enemies at once instead
    def __init__(self, name: str, cost: int, damage: int) -> None:
        super().__init__(name, cost)
        self.damage = damage
    
    def use(self, user, target):
        target.health -= self.damage
        target.health = max(target.health, 0) # a barrier so you dont go under 0
        user.inventory[self] -= 1
        target.healthbar.update_health()
        print(f"{user.name} used {self.name}, and dealt {self.damage} damage to {target.name}")

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

flit_arrow = Ammo(name="Flint arrow", piercing=2, cost=None)


small_health = HealingItem(name="Small potion of healing", heal_amount=150, cost=None)

medium_health = HealingItem(name="Potion of healing", heal_amount=300, cost=None)

big_health = HealingItem(name="Big potion of healing", heal_amount=500, cost=None)

bomb = OffensiveItem(name="Bomb", damage=80, cost=None)

dynamite = OffensiveItem(name="Stick of dynamite", damage=50, cost=None)
