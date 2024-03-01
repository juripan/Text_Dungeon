# menu class, gives the player control of their character

class Menu(): #TODO: need to pass the enemy object into here also to know what the target is
    symbol_border: str = "-" 
    width: int = 30

    def __init__(self, entity) -> None: # entity is the player
        self.entity = entity
    
    def mini_attack_menu(self, targets): # only add attack method
        print("put the attack function here")

    def mini_defend_menu(self): # add dodge and shield functionality here
        print("put defend or dodge function here")

    def mini_item_menu(self, targets): # add equip and use item functionality here
        print("put a new menu function for opening the inventory here")

    def run(self): # add run mechanics here
        print("add a run function here")
    
    def action(self, targets, choice):
        if choice == "attack" or choice == "1":
            Menu.mini_attack_menu(self, targets)
        elif choice == "defend" or choice == "2":
            Menu.mini_defend_menu(self)
        elif choice == "item" or choice == "3":
            Menu.mini_item_menu(self, targets)
        elif choice == "run" or choice == "4":
            Menu.run(self)
    
    def display_battle_menu(self, targets): # figure out what to do with the entity bs and that it doesnt need to pass it as an argument
        print(targets)
        print("What would you like to do?")
        choices_display = "| Attack | Defend | Item | Run |"
        print(self.symbol_border * len(choices_display))
        print(f"| {self.entity.name.ljust(len(choices_display)-3)}|") # string formatting to add spaces
        print(self.symbol_border * len(choices_display))
        print(choices_display)
        print(self.symbol_border * len(choices_display))
        choice = input(">").lower()
        Menu.action(self, targets, choice)

