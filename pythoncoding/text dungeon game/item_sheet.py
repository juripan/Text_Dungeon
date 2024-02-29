# add more items like potions
# in the future add use attributes to all item consumable classes

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


class Armor(Item):
    def __init__(self, name: str, cost: int, resistance: int) -> None:
        super().__init__(name, cost)
        self.resistance = resistance


class Shield(Item):
    def __init__(self, name: str, cost: int, sturdiness: int) -> None:
        super().__init__(name, cost)
        self.sturdiness = sturdiness


class HealingItem(Item):
    def __init__(self, name: str, cost: int, heal_amount: int) -> None:
        super().__init__(name, cost)
        self.heal_amount = heal_amount
    
    def use(self, user):
        user.health += self.heal_amount
        user.health = min(user.health, user.max_health) # a barrier so you dont go over max health
        user.inventory[self] -= 1
        user.healthbar.update()
        print(f"{user.name} used {self.name}, +{self.heal_amount} health")


class OffensiveItem(Item): #note: goes through armor on purpose
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

dynamite = OffensiveItem(name="stick of dynamite", damage=50, cost=None)
