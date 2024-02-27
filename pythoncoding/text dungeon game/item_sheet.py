#TODO: add more items like potions, or shields to be used with the block_attack method

class Item():
    """
    base item class
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


class HealingItem(Item): #TODO: add use attributes to all item consumable classes
    def __init__(self, name: str, cost: int, heal_amount: int):
        super().__init__(name, cost)
        self.heal_amount = heal_amount
    
    def use(self, other):
        other.health += self.heal_amount
        other.health = min(other.health, other.max_health) # a barrier so you dont go over max health
        other.inventory[self] -= 1
        other.healthbar.update()
        print(f"{other.name} used {self.name}, +{self.heal_amount} health")


iron_sword = Weapon(name="Iron sword", damage=50, damage_type="slashing", weapon_range="close", cost=None)

short_bow = Weapon(name="Short bow", damage=30, damage_type="piercing", weapon_range="mid", cost=None)

fists = Weapon(name="Fists", damage=10, damage_type="bludgeoning", weapon_range="close", cost=None)

bow = Weapon(name="Bow", damage=50, damage_type="piercing", weapon_range="long", cost=None)

dagger = Weapon(name="Dagger", damage=40, damage_type="piercing", weapon_range="close", cost=None)


small_health = HealingItem(name="Small potion of healing", cost=20, heal_amount=150)

medium_health = HealingItem(name="Potion of healing", cost=30, heal_amount=300)

big_health = HealingItem(name="Big potion of healing", cost=50, heal_amount=500)


no_armor = Armor(name="No armor", cost=0, resistance=0)

leather_armor = Armor(name="Leather armor", cost=0, resistance=1)

chainmail_armor = Armor(name="Chainmail armor", cost=0, resistance=2)

iron_armor = Armor(name="Iron armor", cost=0, resistance=6)
