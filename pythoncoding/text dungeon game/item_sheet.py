#TODO: add items other than heals, add damage clacs to armors in the attack method


class Item():
    def __init__(self, name: str, cost: int) -> None:
        self.name = name
        self.cost = cost


class HealingItem(Item):
    def __init__(self, name: str, cost: int, heal_amount: int):
        super().__init__(name, cost)
        self.heal_amount = heal_amount


small_health = HealingItem(name="Small potion of healing", cost=20, heal_amount=15)

medium_health = HealingItem(name="Potion of healing", cost=30, heal_amount=30)

big_health = HealingItem(name="Big potion of healing", cost=50, heal_amount=50)


class Armor(Item):
    def __init__(self, name: str, cost: int, resistance: int) -> None:
        super().__init__(name, cost)
        self.resistance = resistance

no_armor = Armor(name="No armor", cost=0, resistance=0)

leather_armor = Armor(name="Leather armor", cost=0, resistance=1)

chainmail_armor = Armor(name="Chainmail armor", cost=0, resistance=3)

iron_armor = Armor(name="Iron armor", cost=0, resistance=5)
