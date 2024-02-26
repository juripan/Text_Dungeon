from character_sheet import Enemy, Player

player = Player(name="Player", max_health=100, inventory={"health potion": 3})
enemy = Enemy(name="Ur mom", max_health=50)


while True:
    enemy.attack(player)
    if player.health < 50:
        player.heal()
    if player.health < 20:
        player.block_attack()
    player.attack(enemy)
    input()
