# menu class, gives the player control of their character
# TODO: add a back out option and add a way of mitigating misspellings like a retry option

class Menu():
    symbol_border: str = "-" 
    width: int = 30

    def __init__(self, entity) -> None: # entity is the player
        self.entity = entity
    
    def mini_attack_menu(self, targets):
        print("who do you want to attack?")
        choice = input(">").lower() # you can either use the name of the enemy or their number in the listed thext to them in console

        for i, target in enumerate(targets):
            if choice == target.name.lower() or choice == str(i + 1):
                self.entity.attack(target)
                break
    
    def mini_defend_menu(self):
        print(f"1. Shield with {self.entity.shield.name}")
        print("2. Dodge")
        choice = input(">").lower()

        if choice == "shield" or choice == "1":
            self.entity.block_attack()
        elif choice == "dodge" or choice == "2":
            self.entity.dodge()

    def mini_item_menu(self, targets):
        print("Use or equip item: ")
        for i, item in enumerate(self.entity.inventory):
            print(f"{i + 1}. {item.name}: {self.entity.inventory.get(item)}")
        choice = input(">").lower()
        print("on who?")
        choice2 = input(">").lower()

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

    def run(self):
        self.entity.run_from_battle()
    
    def action(self, targets, choice):
        if choice == "attack" or choice == "1":
            Menu.mini_attack_menu(self, targets)
        elif choice == "defend" or choice == "2":
            Menu.mini_defend_menu(self)
        elif choice == "item" or choice == "3":
            Menu.mini_item_menu(self, targets)
        elif choice == "run" or choice == "4":
            Menu.run(self)
    
    def display_battle_menu(self, targets):
        print("Enemies:")
        for i, target in enumerate(targets): # prints out every enemy thats in the fight
            print(f"| {i+1}. {target.name} (level {target.level})", end=" ")
        print("|") # just so it ends the list and adds a newline
        
        print("What would you like to do?")
        choices_display = "| Attack | Defend | Item | Run |"
        print(self.symbol_border * len(choices_display))
        print(f"| {self.entity.name.ljust(len(choices_display)-3)}|") # string formatting to add spaces
        print(self.symbol_border * len(choices_display))
        print(choices_display)
        print(self.symbol_border * len(choices_display))
        choice = input(">").lower()
        Menu.action(self, targets, choice)
