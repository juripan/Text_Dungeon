# map / the level display and generation file
from random import choice, randint
import color_file as cf
import battle_manager as bm

class Map:
    room_walls: list[str] = ["┌───┐", "│   │", "└───┘"]
    player_sprite: str = "■"
    boss_sprite: str = "☠"  #note: the skull sprite doesn't want to cooperate (offset to the side)
    player_color: str = "light_blue"
    current_color: str = "default"

    no_room: str = "0"
    normal_room: str = "1"
    explored_room: str = "2"
    boss_room: str = "3"
    player_in_room: str = "9" 

    def __init__(self, width, height, max_room_count) -> None:
        self.max_room_count: int = max_room_count
        self.max_width, self.max_height = width, height
        self.map_layout: list[list[str]] = [["0" for _ in range(self.max_width)] for _ in range(self.max_height)]
        self.player_pos: tuple[int, int] = ()
        self.current_pos: tuple[int, int] = ()
    
    def move_player(self, direction: str) -> None:
        """
        moves the player,
        prints 'cant move there' if its out of the map or out of the room layout,
        returns: None
        """
        x, y = self.player_pos
        self.map_layout[y][x] = self.explored_room
        if direction == "w" and y > 0 and self.map_layout[y - 1][x] != self.no_room:
            y -= 1
        elif direction == "s" and y + 1 < self.max_height and self.map_layout[y + 1][x] != self.no_room:
            y += 1
        elif direction == "a" and x > 0 and self.map_layout[y][x - 1] != self.no_room:
            x -= 1
        elif direction == "d" and x + 1 < self.max_width and self.map_layout[y][x + 1] != self.no_room:
            x += 1
        else:
            print("cant move there!")
        
        if self.map_layout[y][x] == self.normal_room: # player goes to an unexplored room
            roll = randint(1, 3)
            if roll == 1:
                bm.battle_loop()
        elif self.map_layout[y][x] == self.boss_room:
            raise NotImplementedError("Implement bossfights") #TODO: add bossfights to the game

        self.map_layout[y][x] += self.player_in_room
        self.player_pos = x, y
    
    def create_boss_room(self):
        """
        finds the farthest room from the start and makes it into a boss room
        """
        player_x, player_y = self.player_pos
        distances = []
        distance_metric = lambda coords: (coords[0] - player_x)**2 + (coords[1] - player_y)**2
        for y in range(len(self.map_layout)):
            for x in range(len(self.map_layout[0])):
                if self.map_layout[y][x] != self.no_room:
                    distances.append((x, y))
        
        boss_loc = max(distances, key=distance_metric)
        self.map_layout[boss_loc[1]][boss_loc[0]] = "3"

    def will_collide(self, pos: tuple[int, int], length: int, direction: str) -> bool:
        """
        checks for going out of bounds and room overlap,
        used when generating hallways,
        returns: boolean (True if collision, False if otherwise)
        """
        x, y = pos
        if direction == "up":
            if length > y:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y - i][x] != self.no_room:
                    return True
        elif direction == "down":
            if length >= self.max_height - y:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y + i][x] != self.no_room:
                    return True
        elif direction == "left":
            if length > x:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y][x - i] != self.no_room:
                    return True
        elif direction == "right":
            if length >= self.max_width - x:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y][x + i] != self.no_room:
                    return True
        return False

    def create_hall(self, pos: tuple[int, int], length: int, direction: str) -> None:
        """
        creates a hall with using the initial position, length and direction given as parameters,
        returns: None
        """
        x, y = pos
        for _ in range(length):
            if self.max_room_count == 0:
                return
            match direction:
                case "up":
                    y -= 1
                case "down":
                    y += 1
                case "left":
                    x -= 1
                case "right":
                    x += 1
            self.map_layout[y][x] = self.normal_room
            self.max_room_count -= 1
        self.current_pos = (x, y)
    
    def create_halls(self, pos: tuple[int, int], halls_count: int) -> list[tuple[int, int]]:
        """
        creates halls from a branchpoint,
        pos: initial position from witch the branches start,
        returns: a list of tuples with 2 integers (branchpoints)
        """
        directions: list[str] = ["up", "down", "left", "right"]
        hall_lens: list[int] = [2, 4]
        branch_points: list[tuple[int, int]] = []

        for _ in range(halls_count):
            hall_len = choice(hall_lens)
            direction = choice(directions)

            while self.will_collide(pos, hall_len, direction):
                if len(directions) > 1:
                    directions.remove(direction)
                    direction = choice(directions)
                elif len(hall_lens) > 1:
                    hall_lens.remove(hall_len)
                    hall_len = choice(hall_lens)
                    directions = ["up", "down", "left", "right"]
                else: 
                    # breaks the infinite loop that happens if theres nowhere to go
                    return branch_points
            
            self.create_hall(pos, hall_len, direction)
            branch_points.append(self.current_pos)
            directions = ["up", "down", "left", "right"]
        return branch_points

    def generate_map(self, density: int) -> None:
        """
        density: determines how many new branchpoints get created after the initial branches are generated,
        it also determines the amount of halls generated from a branch, is limited by the chance of collision which ends the generation of halls prematurely,
        Note: larger "density" tends to slow down the generation of the map,
        returns: None
        """
        self.origin = randint(1, self.max_width - 1), randint(1, self.max_height - 1)
        self.player_pos = self.origin
        self.map_layout[self.origin[1]][self.origin[0]] = self.normal_room + self.player_in_room

        for _ in range(4): # four branches stemming from the origin
            self.current_pos = self.origin
            init_branches = self.create_halls(self.current_pos, halls_count=density)
            new_branches = []
            for branch in init_branches:
                new_branches.extend(self.create_halls(branch, halls_count=density))
            
            for new_branch in new_branches:
                self.create_halls(new_branch, halls_count=density)
        self.create_boss_room()
    
    def crop_map(self) -> None:
        """
        crops out the unnecessary whitespace,
        updates the map width and height and the position for the player,
        returns: None
        """
        to_remove_row: list = []
        to_remove_column = []
        for i, row in enumerate(self.map_layout):
            if sum(map(int, row)) == 0:
                to_remove_row.append(i)
        
        # goes from the back because the indexing shifts when deleting items
        for index in to_remove_row[::-1]:
            self.map_layout.pop(index)
        self.max_height = len(self.map_layout)

        for j in range(self.max_width):
            s = 0
            for i in range(self.max_height):
                s += int(self.map_layout[i][j])
            if s == 0:
                to_remove_column.append(j)
        
        # see previous comment
        for index in to_remove_column[::-1]:
            for i in range(len(self.map_layout)):
                self.map_layout[i].pop(index)
        self.max_width = len(self.map_layout[0])
        
        player_room_indicator = self.normal_room + self.player_in_room
        for i, row in enumerate(self.map_layout): # finds the players initial position
            if player_room_indicator in row:
                column_index = row.index(player_room_indicator)
                row_index = i
        self.player_pos = (column_index, row_index)

    def draw_map(self) -> None:
        """
        prints out the whole map based on the map_layout,
        returns None
        """
        for row in self.map_layout:
            for i in range(3):
                for column in row:
                    if column[0] == self.normal_room:
                        self.current_color = "default"
                    elif column[0] == self.explored_room:
                        self.current_color = "dark_grey"
                    elif column[0] == self.boss_room:
                        self.current_color = "red"
                        self.room_walls[1] = f"│ {self.boss_sprite} │"
                    
                    if column.endswith(self.player_in_room):
                        self.room_walls[1] = f"│ {self.player_sprite} │"
                        self.player_sprite = f"{cf.colors[self.player_color]}{self.player_sprite}{cf.colors[self.current_color]}"

                    if column[0] == self.no_room:
                        print("     ", end="")
                    else:
                        print(f"{cf.colors[self.current_color]}{self.room_walls[i]}{cf.colors["default"]}", end="")
                    
                    self.room_walls[1] = "│   │" # resets the content of the room (empty)
                print()
        print("-" * self.max_width * 5)


#note: most impactful parameters (in order) are: max_room_count, max_map_size, density
#TODO: make a function that makes a map object and generates, crops a map based on the in game 'floor', scales up as the game goes on
new_map = Map(30, 30, max_room_count = 20)
new_map.generate_map(density=10)
new_map.crop_map()
