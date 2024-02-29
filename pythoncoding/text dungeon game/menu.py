# menu class, gives the player control of their character

class Menu(): #TODO: need to pass the enemy object into here also to know what the target is
    symbol_border: str = "-" 
    width: int = 30

    def __init__(self, entity) -> None:
        self.entity = entity
    
    def action(self, entity, choice):
        if choice == "fight" or choice == "1":
            print("put the fight function here")
        elif choice == "defend"or choice == "2":
            print("put defend function here")
        elif choice == "item" or choice == "3":
            print("put a new menu function for opening the inventory here")
        else:
            print("???") #TODO: think of a new action for the player to do

    def display_menu(self, entity):
        print("What would you like to do?")
        choices_display = "| Fight | Defend | Item | ??? |"
        print(self.symbol_border * len(choices_display))
        print(f"| {self.entity.name.ljust(len(choices_display)-3)}|") # string formatting to add spaces
        print(self.symbol_border * len(choices_display))
        print(choices_display)
        print(self.symbol_border * len(choices_display))
        choice = input().lower()
        Menu.action(self, entity, choice)

