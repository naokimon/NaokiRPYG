from dataclasses import dataclass
import json

with open("data/classes.json") as f:
    BASE_STATS: dict = json.load(f)

@dataclass
class Stats:
    strength: int
    dexterity: int
    intelligence: int
    vitality: int
    luck: int

    @classmethod
    def from_class(cls, rpg_class: str):
        base = BASE_STATS[rpg_class]
        return cls(
            **{k: v for k, v in base.items()}
        )

class Player:
    def __init__(self, rpg_class: str, name: str):
        rpg_class = rpg_class.lower()
        base_exp = 100
        self.name: str = name
        self.rpg_class: str = rpg_class
        self.stats = Stats.from_class(rpg_class)
        self.hp: int = 10 * self.stats.vitality
        self.mp: int = 5 * self.stats.intelligence
        self.level: int = 1
        self.exp = 0
        self.exp_needed: int = int(base_exp * (self.level ** 2.5))
        self.points: int = 0
        self.inventory: list = []

    def display_stats(self):
        name_line = f"  {self.name} — {self.rpg_class.capitalize()}  "
        width = max(len(name_line), 36)
        bar_filled = int((self.exp / self.exp_needed) * (width - 2))
        bar_empty = (width - 2) - bar_filled

        print(f"╔{'═' * width}╗")
        print(f"║{name_line.center(width)}║")
        print(f"╠{'═' * width}╣")
        print(f"║    HP   : {self.hp:<{width - 11}}║")
        print(f"║    MP   : {self.mp:<{width - 11}}║")
        print(f"║    LVL  : {self.level:<{width - 11}}║")
        print(f"╠{'═' * width}╣")
        print(
            f"║  EXP: {self.exp}/{self.exp_needed}{' ' * (width - 8 - len(str(self.exp)) - len(str(self.exp_needed)))}║")
        print(f"║[{'█' * bar_filled}{'░' * bar_empty}]║")
        print(f"╚{'═' * width}╝")

