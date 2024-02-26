# main file only used for testing features
from character_sheet import Enemy, Player
import item_sheet as itm
import weapon_sheet as ws

# not sure if the inventory should be defined here, maybe use names of items insteado of the objects to lessen imports
player = Player(name="Player", max_health=100, inventory={itm.small_health: 3, ws.dagger: 1, itm.chainmail_armor: 1})
enemy = Enemy(name="Ur mom", max_health=50)


while True:
    enemy.attack(player)
    if player.health < 50:
        player.use_item(itm.small_health)
    if player.health < 20:
        player.block_attack()
    player.equip(ws.dagger)
    player.equip(itm.chainmail_armor)
    player.attack(enemy)
    input()
