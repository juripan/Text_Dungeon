# map / the level display and generation file

from random import randint, choice

class Map:
    def __init__(self, max_size: tuple) -> None:
        self.max_width, self.max_height = max_size
        self.rooms: list = [[0] * self.max_width] * self.max_height
        self.treasure_sprite: str = "T"
        self.enemy_sprite: str = "E"
        self.side_wall: str = "│"
        self.top_wall: str = "─"

    def generate_rooms(self):
        ... # TODO: replace this with the functional version that you wrote in class



    def random_special_rooms(self, encounter_count: int, treasure_count: int):
        raise NotImplementedError("Add a random generated distribution of enemy encounters and treasures")

    def draw_room_row(self, row_number: int, content: list=None) -> None:
        walls: list[str] = [f"┌─{self.top_wall}─┐", f"{self.side_wall}   {self.side_wall}", f"└─{self.top_wall}─┘"]
        
        if content == None:
            content = [" "] * self.max_width # if its not defined then it makes everything empty
        
        for i in range(len(walls)):
            for j in range(self.max_width):
                if self.rooms[row_number][i]:
                    print(walls[i], end="")
                else:
                    print(" " * len(walls[i]), end="")
            print()
    
    def draw_room_layout(self) -> None:
        Map.generate_rooms(self)
        for column in range(self.max_height):
            Map.draw_room_row(self, column)

newmap = Map((5, 5))

newmap.draw_room_layout()