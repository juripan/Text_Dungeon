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
    def __init__(self, name: str, damage: int, damage_type: str, weapon_range: str, cost: int) -> None:
        super().__init__(name, cost)
        self.damage = damage
        self.damage_type = damage_type
        self.weapon_range = weapon_range
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically, still defined so it doesnt raise an error
        user.weapon = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class Armor(Item):
    def __init__(self, name: str, cost: int, resistance: int) -> None:
        super().__init__(name, cost)
        self.resistance = resistance
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically
        user.armor = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class Shield(Item):
    def __init__(self, name: str, cost: int, sturdiness: int) -> None:
        super().__init__(name, cost)
        self.sturdiness = sturdiness
    
    def use(self, user, target): # target isnt used cuz the user is the target automatically
        user.shield = self
        user.inventory[self] -= 1
        print(f"{user.name} equipped {self.name}")


class HealingItem(Item):
    def __init__(self, name: str, cost: int, heal_amount: int) -> None:
        super().__init__(name, cost)
        self.heal_amount = heal_amount
    
    def use(self, user, target):
        target.health += self.heal_amount
        target.health = min(target.health, target.max_health) # a barrier so you dont go over max health
        user.inventory[self] -= 1
        target.healthbar.update()
        print(f"{user.name} used {self.name}, and healed {target.name} by {self.heal_amount} health")


class OffensiveItem(Item): #note: goes through armor on purpose,TODO: maybe make it deal damage to all enemies at once instead
    def __init__(self, name: str, cost: int, damage: int) -> None:
        super().__init__(name, cost)
        self.damage = damage
    
    def use(self, user, target):
        target.health -= self.damage
        target.health = max(target.health, 0) # a barrier so you dont go under 0
        user.inventory[self] -= 1
        target.healthbar.update()
        print(f"{user.name} used {self.name}, and dealt {self.damage} damage to {target.name}")


iron_sword = Weapon(name="Iron sword", damage=50, damage_type="slashing", weapon_range="close", cost=None)

short_bow = Weapon(name="Short bow", damage=30, damage_type="piercing", weapon_range="mid", cost=None)

fists = Weapon(name="Fists", damage=10, damage_type="bludgeoning", weapon_range="close", cost=None)

bow = Weapon(name="Bow", damage=40, damage_type="piercing", weapon_range="long", cost=None)

dagger = Weapon(name="Dagger", damage=35, damage_type="piercing", weapon_range="close", cost=None)


no_armor = Armor(name="No armor", resistance=0, cost=None)

leather_armor = Armor(name="Leather armor", resistance=1, cost=None)

chainmail_armor = Armor(name="Chainmail armor", resistance=2, cost=None)

iron_armor = Armor(name="Iron armor", resistance=6, cost=None)


no_shield = Shield(name="No shield", sturdiness=0, cost=None)

wooden_shield = Shield(name="Wooden shield", sturdiness=2, cost=None)

iron_shield = Shield(name="Iron shield", sturdiness=4, cost=None)


small_health = HealingItem(name="Small potion of healing", heal_amount=150, cost=None)

medium_health = HealingItem(name="Potion of healing", heal_amount=300, cost=None)

big_health = HealingItem(name="Big potion of healing", heal_amount=500, cost=None)

bomb = OffensiveItem(name="Bomb", damage=80, cost=None)

dynamite = OffensiveItem(name="Stick of dynamite", damage=50, cost=None)
