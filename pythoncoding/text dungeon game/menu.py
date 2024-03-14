# menu class, gives the player control of their character

class BattleMenu():
    symbol_border: str = "-"
    default_width: int = 50

    def __init__(self, entity) -> None: # entity is the player
        self.entity = entity
    
    def help(self, targets):
        print(self.symbol_border * self.default_width)
        print("""All possible commands:
        (yes you can also use numbers instead of commands)
        (they go by order from left to right)
        
        Battle menu:
        'attack' or '1' - brings up the attack menu
        'defend' or '2' - brings up the defend menu
        'item' or '3' - brings up the item use menu / inventory
        'run' or '4' - attempts to run from the battle
        
        Atttack menu:
        *name of enemy or their order number* - attack that enemy with your weapon
        'back' or '..' - goes back to the previous menu

        Defend menu:
        'shield' - uses your shield to block the next attack
        'dodge' - attempts to dodge the next attack
        'back' or '..' - goes back to the previous menu
        
        Item menu:
        1st input:
        *name of the item or its order number* - determines the item you equip/use
        'back' or '..' - goes back to the previous menu
        2nd input(use on who?):
        *name of the enemy or their order number* - determines the target you use the item on (equip or heasl items automatically target you)
        'back' or '..' - goes back to the previous menu
        any other input will use the item on you""")
        print(self.symbol_border * self.default_width)
        BattleMenu.display_battle_menu(self, targets)

    def mini_attack_menu(self, targets):
        print(self.symbol_border * self.default_width)
        print("who do you want to attack?")
        print(self.symbol_border * self.default_width)
        choice = input(">").lower() # you can either use the name of the enemy or their number in the listed thext to them in console

        if choice == "back" or choice == "..": # if you want to go back to the original menu
            BattleMenu.display_battle_menu(self, targets)
            return # halts the current function 

        for i, target in enumerate(targets):
            if choice == target.name.lower() or choice == str(i + 1):
                self.entity.attack(target)
                break
        else: # if misspelled (not in the enemies list)
            print("not in the list of enemies")
            BattleMenu.mini_attack_menu(self, targets)
    
    def mini_defend_menu(self, targets):
        print(self.symbol_border * self.default_width)
        print(f"1. Shield with {self.entity.shield.name}")
        print("2. Dodge")
        print(self.symbol_border * self.default_width)
        choice = input(">").lower()

        if choice == "shield" or choice == "1":
            self.entity.block_attack()
        elif choice == "dodge" or choice == "2":
            self.entity.dodge()
        elif choice == "back" or choice == "..": # goes back to the original menu
            BattleMenu.display_battle_menu(self, targets)
            return # halts the current function
        else: # if misspelled
            print("not in the commands list")
            BattleMenu.mini_defend_menu(self)

    def mini_item_menu(self, targets):
        print(self.symbol_border * self.default_width)
        print("Use or equip item: ")
        for i, item in enumerate(self.entity.inventory):
            print(f"{i + 1}. {item.name}: {self.entity.inventory.get(item)}")
        print(self.symbol_border * self.default_width)
        choice = input(">").lower()
        print("use on who?")
        choice2 = input(">").lower()

        if choice == "back" or choice == ".." or choice2 == "back" or choice2 == "..": # if you want to go back to the original menu
            BattleMenu.display_battle_menu(self, targets)
            return # halts the current function 

        for i, target in enumerate(targets):
            if target.name.lower() == choice2 or choice2 == str(i + 1):
                aimed_at = target
                break
        else:
            aimed_at = self.entity # if its not in the list of enemies it gets used on the player

        for i, item in enumerate(self.entity.inventory):
            if choice == item.name.lower() or choice == str(i + 1):
                self.entity.use_item(item, target=aimed_at)
                break
        else: # if not in the inv
            print("not in the item list")
            BattleMenu.mini_item_menu(self, targets)

    def run(self):
        self.entity.run_from_battle()
    
    def action(self, targets):
        choice = input(">").lower()
        if choice == "attack" or choice == "1":
            BattleMenu.mini_attack_menu(self, targets)
        elif choice == "defend" or choice == "2":
            BattleMenu.mini_defend_menu(self, targets)
        elif choice == "item" or choice == "3":
            BattleMenu.mini_item_menu(self, targets)
        elif choice == "run" or choice == "4":
            BattleMenu.run(self)
        elif choice == "help":
            BattleMenu.help(self, targets)
        else: # if wrong command
            print("not in the commands list")
            BattleMenu.action(self, targets)
    
    def display_battle_menu(self, targets):
        print(self.symbol_border * self.default_width)
        print("write 'help' if you need a list of commands")
        print(self.symbol_border * self.default_width)
        self.entity.healthbar.display_health() # player health
        
        choices_display = "| Attack | Defend | Item | Run |"

        print("Enemies:")
        for i, target in enumerate(targets): # prints out every enemy thats in the fight
            print(f"| {i+1}. {target.name} (level {target.level})", end=" ")
            target.healthbar.display_health(name_display=False, end=" ")
        
        print("What would you like to do?")
        print(f"+{self.symbol_border * (len(choices_display) - 2)}+")
        print(f"| {self.entity.name.ljust(len(choices_display)-3)}|") # string formatting to add spaces
        print(f"+{self.symbol_border * (len(choices_display) - 2)}+")
        print(choices_display)
        print(f"+{self.symbol_border * (len(choices_display) - 2)}+")
        BattleMenu.action(self, targets)
