# main file only used for testing features
#TODO: make a proper battle manager not this bs, also make the death of player a seperate thing
from character_sheet import player, enemies


while enemies and player.health > 0: # fight continues until enemies are dead or the player is dead
    player.menu.display_battle_menu(enemies) # players turn

    if player.run_success: # if player runs away then battle ends
        break

    for enemy in enemies: # all enemies check for death
        if enemy.health == 0:
            enemy.death(player, enemies)
    
    for enemy in enemies: # all enemies have a turn (attack)
        enemy.attack(player)
    
    for enemy in enemies: # shows healthbars of every enemy
        enemy.healthbar.display_health()
    player.healthbar.display_health() # shows healthbar of the player

print("END OF BATTLE")