# main file only used for testing features
from character_sheet import player, enemies


while True:
    player.menu.display_battle_menu(enemies)
    #enemies[0].attack(player)
    #player.dodge()
    #player.attack(enemies[0])
    #input()

    for enemy in enemies:
        enemy.healthbar.display_health()
    player.healthbar.display_health()
