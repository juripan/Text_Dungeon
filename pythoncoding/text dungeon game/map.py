# map / the level display and generation file
from random import choice, randint


class Map:
    room_walls: list[str] = ["┌───┐", "│   │", "└───┘"]
    player_sprite: str = "P"
    directions: list[str] = ["up", "down", "left", "right"]

    def __init__(self, width, height, max_room_count) -> None:
        self.max_room_count: int = max_room_count
        self.max_width, self.max_height = width, height
        self.map_layout: list[list[int]] = [[0 for _ in range(self.max_width)] for _ in range(self.max_height)]
        self.player_pos: tuple[int, int] = ()
        self.current_pos: tuple[int, int] = ()

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
                if self.map_layout[y - i][x] in (1, 2):
                    return True
        elif direction == "down":
            if length >= self.max_height - y:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y + i][x] in (1, 2):
                    return True
        elif direction == "left":
            if length > x:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y][x - i] in (1, 2):
                    return True
        elif direction == "right":
            if length >= self.max_width - x:
                return True
            for i in range(1, length + 1):
                if self.map_layout[y][x + i] in (1, 2):
                    return True
        return False

    def move_player(self, direction: str) -> None:
        """
        moves the player,
        prints 'cant move there' if its out of the map or out of the room layout,
        returns: None
        """
        x, y = self.player_pos
        self.map_layout[y][x] = 1
        if direction == "up" and y - 1 > 0 and self.map_layout[y - 1][x] != 0:
            y -= 1
        elif direction == "down" and y + 1 < self.max_height and self.map_layout[y + 1][x] != 0:
            y += 1
        elif direction == "left" and x - 1 > 0 and self.map_layout[y][x - 1] != 0:
            x -= 1
        elif direction == "right" and x + 1 < self.max_width and self.map_layout[y][x + 1] != 0:
            x += 1
        else:
            print("cant move there!")
        self.map_layout[y][x] = 2
        self.player_pos = x, y

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
            self.map_layout[y][x] = 1
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
        origin = randint(1, self.max_width - 1), randint(1, self.max_height - 1)
        self.player_pos = origin
        self.map_layout[origin[1]][origin[0]] = 2

        for _ in range(4): # four branches stemming from the origin
            self.current_pos = origin
            init_branches = self.create_halls(self.current_pos, halls_count=density)
            new_branches = []
            for branch in init_branches:
                new_branches.extend(self.create_halls(branch, halls_count=density))
            
            for new_branch in new_branches:
                self.create_halls(new_branch, halls_count=density)
    
    def crop_map(self) -> None:
        """
        crops out the unnecessary whitespace,
        returns: None
        """
        to_remove_row: list = []
        to_remove_column = []
        for i, row in enumerate(self.map_layout):
            if sum(row) == 0:
                to_remove_row.append(i)
        
        for j in range(self.max_width):
            s = 0
            for i in range(self.max_height):
                s += self.map_layout[i][j]
            if s == 0:
                to_remove_column.append(j)
        
        # goes from the back because the indexing shifts when deleting items
        for index in to_remove_row[::-1]:
            self.map_layout.pop(index)
        for index in to_remove_column[::-1]:
            for i in range(len(self.map_layout)):
                self.map_layout[i].pop(index)

    def draw_map(self) -> None:
        """
        prints out the whole map based on the map_layout,
        returns None
        """
        for row in self.map_layout:
            for i in range(3):
                for column in row:
                    if column == 2: # room occupied by the player
                        self.room_walls[1] = f"│ {self.player_sprite} │"
                        print(self.room_walls[i], end="")
                        self.room_walls[1] = "│   │"
                    elif column == 1:
                        print(self.room_walls[i], end="") # normal room
                    else:
                        print("     ", end="") # no room
                print()


#note: most impactful parameters (in order) are: max_room_count, max_map_size, density
new_map = Map(30, 30, max_room_count = 20)
new_map.generate_map(density=10)
new_map.crop_map()
new_map.draw_map()
#TODO: make a function that makes a map object and generates, crops a map based on the in game 'floor', scales up as the game goes on
