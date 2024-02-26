#TODO: add items other than heals, maybe armor but that needs to be added to the characters and damage calcs frist


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
