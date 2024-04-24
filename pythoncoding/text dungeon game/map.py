# map / the level display and generation file
from random import choice


def remove_all(array: list, item) -> list:
    return [j for _,j in enumerate(array) if j!=item]


class Map:
    room_walls: list[str] = ["┌───┐", "│   │", "└───┘"]
    player_sprite: str = "P"

    def __init__(self, size: tuple[int, int]):
        self.max_width, self.max_height = size
        self.map_layout: list[list[int]] = [[0 for _ in range(self.max_width)] for _ in range(self.max_height)]

    def generate_branch(self, x: int, y: int, room_count: int) -> list[tuple[int]]: 
        #TODO: make it generate better maps, less bunched up now but still too gobbed up, main problem is that it bunches itself up in one direction
        """
        generates a branch of rooms in a 2d array from its starting point,
        x and y are the starting room coordinates
        room_count is the amount of rooms it will generate (might generate less because it could crash into itself)
        returns a list of points where more branches can sprout if needed
        """

        moves: list[str] = ["up", "down", "left", "right"]
        branch_points: list[tuple[int]] = []

        for i in range(room_count):
            # disables movement if it goes out or the map or if it goes over a generated room
            if y == 0:
                moves = remove_all(moves, "up")
            elif self.map_layout[y - 1][x]:
                moves = remove_all(moves, "up")
            if y == self.max_height - 1:
                moves = remove_all(moves, "down")
            elif self.map_layout[y + 1][x]:
                moves = remove_all(moves, "down")
            if x == 0:
                moves = remove_all(moves, "left")
            elif self.map_layout[y][x - 1]:
                moves = remove_all(moves, "left")
            if x == self.max_width - 1:
                moves = remove_all(moves, "right")
            elif self.map_layout[y][x + 1]:
                moves = remove_all(moves, "right")
            
            if not moves:
                print("it cornered itself") # temporary print
                break

            direction = choice(moves)
            print(direction) # temporary print
            
            if direction == "up":
                y -= 1
            elif direction == "down":
                y += 1
            elif direction == "left":
                x -= 1
            elif direction == "right":
                x += 1

            self.map_layout[y][x] = 1  # sets the room

            if i % 3 == 0: # every even room can sprout a new branch
                branch_points.append((x, y))
            
            for row in self.map_layout: # temporary way or printing the array (for debugging only)
                print(row)
            print("===============================")

            moves = ["up", "down", "left", "right"] # resets the possible moves
            moves.append(direction) # adds the recent direction to make it more likely to go that way
        return branch_points #returns all possible points where the new branches can start
    
    def generate_layout(self, main_branch_length: int, extra_branch_length: int): #TODO: make the branch lengths scale off of the map size
        """
        generates a 2d array that determines the room layout,
        2 is the player in a room,
        1 is a room,
        0 is an empty space,
        """

        # starting room, set in the middle
        x, y = self.max_width // 2, self.max_height // 2
        self.map_layout[y][x] = 2 # player is set here

        #main branch
        branch_points = Map.generate_branch(self, x, y, main_branch_length)

        #extra branches
        for possible_branch in branch_points:
            print("new branch being generated") # temporary print
            Map.generate_branch(self, possible_branch[0], possible_branch[1], extra_branch_length)
    
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


new_map = Map((10, 10))

new_map.generate_layout(6, 5)

new_map.draw_map()
