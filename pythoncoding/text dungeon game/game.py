# main file only used for testing features
from character_sheet import Enemy, Player
import item_sheet as item

player = Player(name="Player", max_health=100, inventory={item.small_health: 3}) # not sure if the inventory should be defined here
enemy = Enemy(name="Ur mom", max_health=50)


while True:
    enemy.attack(player)
    if player.health < 50:
        player.use_item(item.small_health)
    if player.health < 20:
        player.block_attack()
    player.attack(enemy)
    input()
