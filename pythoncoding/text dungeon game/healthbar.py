# class that draws and updates the healthbar of any Character

class Healthbar:
    symbol_remaining: str = "█"
    symbol_lost: str = "-"
    symbol_border: str = "│"

    def __init__(self, entity, length: int = 20) -> None:
        self.entity = entity
        self.length = length
        self.max_value = entity.max_health
        self.current_value = entity.health
    
    def update_health(self) -> None:
        self.current_value = self.entity.health
    
    def display_health(self, name_display=True, end=None) -> None:
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        if name_display:
            print(f"{self.entity.name}s ", end="")
        print(f"HP: {self.entity.health}/{self.entity.max_health}")
        print(f"{self.symbol_border}{self.symbol_remaining * remaining_bars}{self.symbol_lost * lost_bars}{self.symbol_border}")
