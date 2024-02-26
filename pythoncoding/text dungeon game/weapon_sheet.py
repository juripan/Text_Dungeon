
class Weapon():
    # base weapon class
    def __init__(self, name: str, damage: int, damage_type: str, weapon_range: str, weight: int = 10) -> None:
        self.name = name
        self.damage = damage
        self.damage_type = damage_type
        self.weapon_range = weapon_range


iron_sword = Weapon(name="Iron sword", damage=5, damage_type="slashing", weapon_range="close")

short_bow = Weapon(name="Short bow", damage=3, damage_type="piercing", weapon_range="mid")

fists = Weapon(name="Fists", damage=2, damage_type="bludgeoning", weapon_range="close")

bow = Weapon(name="Bow", damage=5, damage_type="piercing", weapon_range="long")
