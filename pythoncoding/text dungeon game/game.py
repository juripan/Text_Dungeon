# main file only used for testing features
from random import randint

from character_sheet import player, all_enemies

class Battle: #TODO: add enemy behavior here (AI)
    """
    battle manager
    manages turns and events that occur during the battle and after it
    """

    def __init__(self, player) -> None:
        self.player = player
        self.enemies: list = []
        self.initial_player_level = player.level
    
    def generate_encounter(self, all_enemies: list) -> None: # TODO: make level and the stats of the enemies scaleable based on player level
        """
        generates a random encounter
        1 to 3 enemies picked from the all_enemies list are added to the self.enemies list
        """
        copy_count = 0
        encounter_amount = randint(1, 3) # amount of enemies that will be "spawned"
        for i in range(encounter_amount):
            random_enemy_index = randint(0, len(all_enemies) - 1)
            new_enemy = all_enemies[random_enemy_index].deepcopy() # creates a deep copy of an enemy object
            for ready_enemy in self.enemies:
                if ready_enemy.name == new_enemy.name: # detects if theres an enemy with the same name already
                    copy_count += 1
                    new_enemy.name = new_enemy.name + " " + str(copy_count)
            self.enemies.append(new_enemy) # adds the enemy to the encounter

    def turn_resets(self) -> None:
        #resets blocking and dodging bools back to their original state
        self.player.vulnerable = True
        self.player.shielded = False

    def levelup_check(self) -> None:
        # if you hit the amount of exp you need to level up
        # keeps leveling up until your exp is less than the exp cap
        while self.player.experience_points >= self.player.experience_cap:
            self.player.experience_points -= self.player.experience_cap
            self.player.level += 1
            self.player.experience_cap = int(self.player.experience_cap * 9/8) # increases the amount of exp you need to level up
            print(f"{self.player.name} reached level {self.player.level}!")
    
    def level_up(self, level_up_points) -> None:
        # gives the player a chance to add to your stats after the battle is over and if you got some levels
        for i in range(level_up_points):
            print("--------------------------------------")
            print("choose a stat to level up")
            for i, stat in enumerate(self.player.stats):
                print(f"{i + 1}. {stat} {self.player.stats[stat]}")
            
            choice = input(">").lower()

            for i, stat in enumerate(self.player.stats):
                if choice == stat.lower() or choice == str(i + 1) and self.player.stats[stat] != 20: # max possible stat value should be 20
                    self.player.stats[stat] += 1
                    level_up_points -= 1
                    print(f"You leveled up {stat}!")

                    if stat == "vigor": # raises your hp for every vigor point you added
                        self.player.max_health += int(self.player.max_health * (20/100))
                    break
            else:
                print("this stat doesnt exist / is too high")
                return Battle.level_up(self, level_up_points)

    
    def battle_loop(self) -> None:
        Battle.generate_encounter(self, all_enemies)
        while self.enemies and self.player.health > 0: # fight continues until enemies are dead or the player is dead
            self.player.menu.display_battle_menu(self.enemies) # players turn

            if self.player.run_success: # if player runs away then battle ends
                break

            for enemy in self.enemies:
                if enemy.health == 0: # all enemies check for death
                    enemy.death(self.player, self.enemies)
            

            for enemy in self.enemies: # all enemies have a turn (attack)
                enemy.attack(player)
            
            Battle.turn_resets(self)

            Battle.levelup_check(self) # checks if the player leveled up
        
        if self.player.health != 0:
            level_up_points = self.player.level - self.initial_player_level # sets how many levels you leveled up by durng the battle
            Battle.level_up(self,level_up_points)
        
        print(self.player.stats)
        print(f"your current exp: {player.experience_points}, current level: {player.level}, how much exp you need to get for new level: {player.experience_cap}")
        print("END OF BATTLE")


battle1 = Battle(player)


def main():
    battle1.battle_loop()

if __name__=="__main__":
    main()
