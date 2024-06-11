#battle manager, contains and manages turns and events that occur during the battle and after it
from random import randint, choice

from character_sheet import player, all_enemies, all_bosses
from color_file import colors


def generate_encounter(all_enemies: tuple, boss: bool = False) -> None: #TODO: add enemy behavior here (AI)
    """
    generates a random encounter,
    1 to 3 enemies picked from the all_enemies list are added to the enemies list,
    if boss == True then generates 1 random boss
    """
    enemies: list[object] = []
    copy_count: int = 0
    if boss:
        encounter_amount = 1
    else:
        encounter_amount = randint(1, 3) # amount of enemies that will be "spawned"
    
    for _ in range(encounter_amount):
        random_enemy = choice(all_enemies)
        new_enemy = random_enemy.deepcopy() # creates a deep copy of an enemy object
        for ready_enemy in enemies:
            if ready_enemy.name == new_enemy.name: # detects if theres an enemy with the same name already
                copy_count += 1
                new_enemy.name = new_enemy.name + " " + str(copy_count)
        enemies.append(new_enemy) # adds the enemy to the encounter
    return enemies


def turn_resets() -> None:
    """
    resets blocking and dodging bools back to their original state
    """
    player.vulnerable = True
    player.shielded = False


def levelup_check() -> None:
    """
    triggers if the player hits the required experience cap
    keeps leveling up until the players exp is less than the experience cap
    """
    while player.experience_points >= player.experience_cap:
        player.experience_points -= player.experience_cap
        player.level += 1
        player.experience_cap = int(player.experience_cap * 9/8) # increases the amount of exp you need to level up
        print(f"{player.name} reached level {player.level}!")


def level_up(level_up_points) -> None:
    """
    gives the player a chance to add to your stats after the battle is over and if the player got some levels
    """
    for i in range(level_up_points):
        if sum(player.stats.values()) >= 20 * 5:
            print("All of your stats are maxed out, no leveling up can be done")
            break

        print("─" * 50)
        print("Choose a stat to level up:")
        for i, stat in enumerate(player.stats):
            print(f"{i + 1}. {stat}: {player.stats[stat]}")
        
        choice = input(">").lower()

        for i, stat in enumerate(player.stats):
            if choice == stat.lower() or choice == str(i + 1) and player.stats[stat] != 20: # max possible stat value should be 20
                player.stats[stat] += 1
                level_up_points -= 1
                print(f"You leveled up {colors["yellow"]}{stat}!{colors["default"]}")

                if stat == "vigor": # raises players hp for every vigor point the player added
                    player.max_health += int(player.max_health * (10/100))
                    player.healthbar.update_max_health() # updates max health so the healthbar is synced up
                break
        else:
            print("This stat doesn't exist / is too high")
            return level_up(level_up_points)


def battle_loop(boss: bool = False) -> None:
    """
    starts the battle and manages all of the battle events in its while loop
    """
    initial_player_level = player.level

    if not boss:
        enemies: list[object] = generate_encounter(all_enemies)
        print(f"{colors["yellow"]}YOU ENCOUNTERED A FOE!{colors["default"]}")
    else:
        enemies: list[object] = generate_encounter(all_bosses, boss = True)
        print(f"{colors["yellow"]}YOU ENCOUNTERED A BOSS!{colors["default"]}")
    
    while enemies and player.health > 0: # fight continues until enemies are dead or the player is dead
        player.menu.display_battle_menu(enemies) # players turn

        if player.run_success: # if player runs away then battle ends
            player.run_success = False # flips it for so the next battle doesn't have a 100% run chance
            break

        for enemy in enemies:
            if enemy.health == 0: # all enemies check for death
                enemy.death(player, enemies)
        

        for enemy in enemies: # all enemies have a turn (attack)
            enemy.attack(player)
        
        turn_resets()

        levelup_check() # checks if the player leveled up
    
    print("─" * 50)
    if player.health != 0:
        print("YOU WON!".center(50))
        level_up_points = player.level - initial_player_level # sets how many levels you leveled up by during the battle
        level_up(level_up_points)
        print(f"your current exp: {player.experience_points}/{player.experience_cap}, current level: {player.level}")
    else:
        print("YOU DIED!".center(50))
