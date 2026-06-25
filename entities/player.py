import dataclasses
from dataclasses import dataclass
from pathlib import Path
import json
from utils import pinput, yn

root = Path(__file__).parent.parent
classes_path = root / "data" / "classes.json"

with open(classes_path) as f:
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

    @classmethod
    def charactercreation(cls):
        print("What is your name..?")

        while True:
            name = pinput()

            if yn(f"Are you sure your name is {name}? Y/N"):
                break

        rpg_class: str = ""
        while True:
            print("Choose your class...")
            classes: list[str] = ["warrior", "mage", "rogue", "cleric", "archer"]
            for index, rclass in enumerate(classes, start=1):
                print(f"{index}. {rclass.capitalize()}")

            choice: str = pinput().lower().strip()

            if choice in classes:
                rpg_class = choice
            elif choice.isdigit() and 1 <= int(choice) <= len(classes):
                rpg_class = classes[int(choice) - 1]
            else:
                print("Enter a valid number or class.")
                continue

            if yn(f"Are you sure you want to start as a {rpg_class}? Y/N"):
                break

        print(f"You are now {name}, the {rpg_class.capitalize()}!")
        return cls(rpg_class, name)

    def display_stats(self) -> None:
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

    def save_game(self) -> None:
        save_data: dict = {
            "name": self.name,
            "class": self.rpg_class,
            "stats": dataclasses.asdict(self.stats),
            "hp": self.hp,
            "mp": self.mp,
            "level": self.level,
            "exp": self.exp,
            "points": self.points,
            "inventory": self.inventory,
        }

        save_path: Path = root / "save_data.json"

        with open(save_path, "w") as file:
            json.dump(save_data, file, indent=2)

    def load_game(self):
        save_path: Path = root / "save_data.json"
        with open(save_path) as file:
            save_data: dict = json.load(file)

        self.name = save_data["name"]
        self.rpg_class = save_data["class"]
        self.stats = Stats(**save_data["stats"])
        self.hp = save_data["hp"]
        self.mp = save_data["mp"]
        self.level = save_data["level"]
        self.exp = save_data["exp"]
        self.points = save_data["points"]
        self.inventory = save_data["inventory"]

        print("Game has been loaded!")