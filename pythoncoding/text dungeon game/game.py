# main file only used for testing features
from character_sheet import Enemy, Player
import item_sheet as itm

# not sure if the inventory should be defined here, maybe use names of items instead of the objects to lessen imports
player = Player(name="Player", max_health=1000, 
                inventory={itm.small_health: 3, itm.dagger: 1, itm.iron_armor: 1, itm.iron_shield: 1})
enemy = Enemy(name="Ur mom", max_health=500)


while True:
    enemy.attack(player)
    if player.health < 800:
        player.use_item(itm.small_health)
    if player.health < 500: 
        player.block_attack()
    player.equip(itm.dagger)
    player.equip(itm.iron_armor)
    player.equip(itm.iron_shield)
    player.attack(enemy)
    input()
