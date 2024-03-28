# main file only used for testing features
from character_sheet import player, enemies

class Battle: #TODO: add enemy behavior here (AI)
    """
    battle manager
    manages turns and events that occur during the battle and after it
    """

    def __init__(self, player, enemies) -> None:
        self.player = player
        self.enemies = enemies
        self.initial_player_level = player.level
    
    def turn_resets(self):
        #resets blocking and dodging bools back to their original state
        self.player.vulnerable = True
        self.player.shielded = False

    def levelup_check(self):
        # if you hit the amount of exp you need to level up
        # keeps leveling up until your exp is less than the exp cap
        while self.player.experience_points >= self.player.experience_cap:
            self.player.experience_points -= self.player.experience_cap
            self.player.level += 1
            self.player.experience_cap = int(self.player.experience_cap * 9/8) # increases the amount of exp you need to level up
            print(f"{self.player.name} reached level {self.player.level}!")
    
    def level_up(self, level_up_points):
        # gives you a chance to add to your stats after the battle is over and if you got some levels
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

    
    def battle_loop(self):
        while self.enemies and self.player.health > 0: # fight continues until enemies are dead or the player is dead
            self.player.menu.display_battle_menu(enemies) # players turn

            if self.player.run_success: # if player runs away then battle ends
                break

            for enemy in self.enemies: 
                if enemy.health == 0: # all enemies check for death
                    enemy.death(self.player, self.enemies)
            

            for enemy in enemies: # all enemies have a turn (attack)
                enemy.attack(player)
            
            Battle.turn_resets(self)

            Battle.levelup_check(self) # checks if the player leveled up
        
        if self.player.health != 0:
            level_up_points = self.player.level - self.initial_player_level # sets how many levels you leveled up by durng the battle
            Battle.level_up(self,level_up_points)
        
        print(self.player.stats)
        print(f"your current exp: {player.experience_points}, current level: {player.level}, how much exp you need to get for new level: {player.experience_cap}")
        print("END OF BATTLE")


battle1 = Battle(player, enemies)


def main():
    battle1.battle_loop()

if __name__=="__main__":
    main()
