import dataclasses
from dataclasses import dataclass
from pathlib import Path
import json
from utils import pinput, yn, cls
from items.consumables import load_consum, Consumable
import os

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
        self.max_hp: int = 10 * self.stats.vitality
        self.hp: int = 10 * self.stats.vitality
        self.max_mp: int = 5 * self.stats.intelligence
        self.mp: int = 5 * self.stats.intelligence
        self.level: int = 1
        self.exp = 0
        self.exp_needed: int = int(base_exp * (self.level ** 2.5))
        self.points: int = 5
        self.inventory: dict    [str, int] = {"health_potion_1": 1, "mana_potion_1": 1}

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

    def display_info(self) -> None:
        name_line = f"  {self.name} — {self.rpg_class.capitalize()}  "
        width = max(len(name_line), 36)
        bar_filled = int((self.exp / self.exp_needed) * (width - 2))
        bar_empty = (width - 2) - bar_filled

        print(f"╔{'═' * width}╗")
        print(f"║{name_line.center(width)}║")
        print(f"╠{'═' * width}╣")
        print(f"║{" " * width}║")
        hp_str = f"{self.hp}/{self.max_hp}"
        mp_str = f"{self.mp}/{self.max_mp}"
        print(f"║    HP   : {hp_str:<{width - 11}}║")
        print(f"║    MP   : {mp_str:<{width - 11}}║")
        print(f"║    LVL  : {self.level:<{width - 11}}║")
        print(f"║{" " * width}║")
        print(f"╠{'═' * width}╣")
        print(f"║{" " * width}║")
        print(
            f"║  EXP: {self.exp}/{self.exp_needed}{' ' * (width - 8 - len(str(self.exp)) - len(str(self.exp_needed)))}║")
        print(f"║[{'█' * bar_filled}{'░' * bar_empty}]║")
        print(f"║{" " * width}║")
        print(f"╚{'═' * width}╝")

    def show_inventory(self):
        showing_inv: bool = True
        message = "~ Type the corresponding number in to select item"
        while showing_inv:
            cls()
            width: int = os.get_terminal_size().columns
            print(f"\n[ Inventory ]")
            if not self.inventory:
                print("  Your inventory is empty.")
                print(f"+{"-" * (width - 2)}+")
                print(message)
                pinput()
                return
            for i, (item_id, amount) in enumerate(self.inventory.items(), start=1):
                item = load_consum(item_id)
                print(f" {i}. {item.name} x{amount}")
                print(f"  {item.description}")
            print()
            print(f"+{"-" * (width - 2)}+")
            print(message)

            player_input = pinput()
            command: str = player_input.split()[0]
            args: list[str] = player_input.split(maxsplit=1)[1].split() if len(player_input.split()) > 1 else []

            match command:
                case "exit" | "e":
                    showing_inv = False
                case "use" | "u":
                    if not args or not args[0].isnumeric():
                        message = "~ Specify an item number. e.g. 'use 1'"
                        continue
                    item_number: int = int(args[0]) - 1
                    if item_number < 0 or item_number >= len(self.inventory):
                        message = f"~ {item_number} is invalid"
                        continue
                    item_id: str = list(self.inventory.keys())[item_number]
                    item: Consumable = load_consum(item_id)
                    if item.use(self):
                        self.inventory[item_id] -= 1
                        message = f"~ Healed {item.data["type"]} by {item.data["amount"]}"
                    else:
                        message = f"~ Already at max {item.data["type"]}!"
                    if self.inventory[item_id] <= 0:
                        del self.inventory[item_id]
                case "discard" | "d":
                    if not args or not args[0].isnumeric():
                        message = "~ Specify an item number. e.g. 'discard 1'"
                        continue
                    item_number: int = int(args[0]) -1
                    if item_number < 0 or item_number >= len(self.inventory):
                        message = f"~ {item_number} id invalid"
                        continue
                    item_id: str = list(self.inventory.keys())[item_number]
                    item: Consumable = load_consum(item_id)
                    if yn(f"~ Are you sure you want to discard {item.name}? Y/N:"):
                        self.inventory[item_id] -= 1
                        if self.inventory[item_id] <= 0:
                            del self.inventory[item_id]
                    else:
                        print(f"~ {item.name} was not discarded!")
                case _:
                    message = f"~ {player_input} is not a valid command"

    def recalc_stat(self):
        pct_hp: float = self.hp / self.max_hp
        self.max_hp = 10 * self.stats.vitality
        self.hp = int(self.max_hp * pct_hp)

        pct_mp: float = self.mp / self.max_mp
        self.max_mp = 5 * self.stats.intelligence
        self.mp = int(self.max_mp * pct_mp)


    def show_stats(self):
        message = "~ Type allocate to allocate points"
        while True:
            cls()
            print(f"[ {self.name}'s stats ]")
            stat_items = self.stats.__dict__.items()
            for k, v in stat_items:
                print(f"{k.capitalize()}: {v}")
            print(f"Stat points: {self.points}")
            width: int = os.get_terminal_size().columns
            print(f"+{"-" * (width - 2)}+")
            print(message)
            player_input = pinput()

            match player_input:
                case "allocate" | "alloc":
                    if self.points <= 0:
                        print("~ You have no points...")
                        continue
                    while True:
                        print("Enter amount of points you want to allocate:")
                        amount = pinput()

                        if not amount.isnumeric():
                            print(f"{amount} is not a number.")
                            continue
                        amount = int(amount)
                        print("What stat would you like to increase?")
                        for i, (k, v) in enumerate(stat_items, start=1):
                            print(f"{i}. {k.capitalize()}")
                        player_input = pinput()
                        match player_input:
                            case "strength" | "1":
                                if yn(f"Are you sure you want to increase strength by {amount}? Y/N:"):
                                    self.stats.strength += amount
                                    self.points -= amount
                                    message = f"Strength was increased by {amount}"
                                    break
                                else:
                                    print("Points were not allocated.")
                                    break
                            case "dexterity" | "2":
                                if yn(f"Are you sure you want to increase dexterity by {amount}? Y/N:"):
                                    self.stats.dexterity += amount
                                    self.points -= amount
                                    message = f"Dexterity was increased by {amount}"
                                    break
                                else:
                                    print("Points were not allocated.")
                                    break
                            case "intelligence" | "3":
                                if yn(f"Are you sure you want to increase intelligence by {amount}? Y/N:"):
                                    self.stats.intelligence += amount
                                    self.points -= amount
                                    self.recalc_stat()
                                    message = f"Intelligence was increased by {amount}"
                                    break
                                else:
                                    print("Points were not allocated.")
                                    break
                            case "vitality" | "4":
                                if yn(f"Are you sure you want to increase vitality by {amount}? Y/N:"):
                                    self.stats.vitality += amount
                                    self.points -= amount
                                    self.recalc_stat()
                                    message = f"Vitality was increased by {amount}"
                                    break
                                else:
                                    print("Points were not allocated.")
                                    break
                            case "luck" | "5":
                                if yn(f"Are you sure you want to increase luck by {amount}? Y/N:"):
                                    self.stats.luck += amount
                                    self.points -= amount
                                    message = f"Luck was increased by {amount}"
                                    break
                                else:
                                    print("Points were not allocated.")
                                    break
                case "exit" | "e":
                    break

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

    @classmethod
    def load_game(cls):
        save_path: Path = root / "save_data.json"
        with open(save_path) as file:
            save_data: dict = json.load(file)

        player: Player = cls(save_data["class"], save_data["name"])

        player.stats = Stats(**save_data["stats"])
        player.hp = save_data["hp"]
        player.mp = save_data["mp"]
        player.level = save_data["level"]
        player.exp = save_data["exp"]
        player.points = save_data["points"]
        player.inventory = save_data["inventory"]

        print("Game has been loaded!")

        return player