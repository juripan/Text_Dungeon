# class that draws and updates the healthbar of any Character
from color_file import colors


class Healthbar:
    symbol_remaining: str = "█"
    symbol_lost: str = "-"
    symbol_border: str = "│"

    def __init__(self, entity, length: int = 20, color: str="default") -> None:
        self.entity = entity
        self.length = length
        self.max_value = entity.max_health
        self.current_value = entity.health
        self.color = color
    
    def update_health(self) -> None:
        """
        updates the health of healthbar,
        used after the health changes in any way
        """
        self.current_value = self.entity.health
    
    def update_max_health(self) -> None:
        """
        updates the max health of healthbar,
        used when leveling up vigor
        """
        self.max_value = self.entity.max_health

    def display_health(self, name_display=True) -> None:
        """
        prints out the health + healthbar of the entity,
        name_display: default true, prints out the name of the entity
        """
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        if name_display:
            print(colors[self.color], f"{self.entity.name} (level {self.entity.level}) ", end="")
        print(colors[self.color], f"HP: {self.entity.health}/{self.entity.max_health}")
        print(f"{self.symbol_border}{self.symbol_remaining * remaining_bars}{self.symbol_lost * lost_bars}{self.symbol_border}", colors["default"])
