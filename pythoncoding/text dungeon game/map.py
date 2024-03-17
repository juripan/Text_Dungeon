# map / the level display and generation file
# TODO: make the rooms print look better, make it work with emojis

class Map:
    def __init__(self, max_size: tuple) -> None:
        self.max_size = max_size
        self.treasure_sprite: str = "🎁"
        self.enemy_sprite: str = "👿"
        self.side_wall: str = ":"
        self.top_wall: str = "."
    
    def draw_room(self) -> None:
        print("┌───┐")
        print("│   │")
        print("└───┘")

newmap = Map((30, 30))

newmap.draw_room()