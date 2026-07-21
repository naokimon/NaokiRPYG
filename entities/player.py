import dataclasses
from dataclasses import dataclass
from pathlib import Path
import json
from utils import pinput, yn, cls, seperator, dia_input
from items.consumables import load_consum, Consumable
import os
from items.weapons import Weapon

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
        self.name: str = name
        self.rpg_class: str = rpg_class.lower()
        self.stats = Stats.from_class(rpg_class)
        self.level: int = 1
        self.exp = 0
        self.points: int = 0
        self._init_vitals()
        self._init_inventory()
        self.weapon: Weapon = Weapon.load(self.equipment_inv["equipment_inv"]["weapon"][0])

    def _init_vitals(self):
        base_exp = 100
        self.max_hp: int = 10 * self.stats.vitality
        self.hp: int = 10 * self.stats.vitality
        self.max_mp: int = 5 * self.stats.intelligence
        self.mp: int = 5 * self.stats.intelligence
        self.exp_needed: int = int(base_exp * (self.level ** 2.5))
        self.dead: bool = False

    def get_starter_weapon(self):
        match self.rpg_class:
            case "warrior":
                self.equipment_inv["equipment_inv"]["weapon"].append("wep_broadsword")

    def _init_inventory(self):
        self.key_inv: dict = {"key_inv": []}
        self.equipment_inv: dict = {"equipment_inv": {"weapon": [], "headwear": [], "armor": [], "greaves": [], "boots": []}}
        self.get_starter_weapon()
        self.consum_inv: dict = {"consum_inv": {"health_potion_1": 1, "mana_potion_1": 1}}
        self.inventory: dict = self.consum_inv | self.key_inv | self.equipment_inv


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

    def show_consum(self):
        showing_consum: bool = True
        message = "~ Type the corresponding number to select item"
        while showing_consum:
            cls()
            print(f"\n[ Consumable Inventory ]")
            consum_inv: dict = self.inventory["consum_inv"]
            if not consum_inv:
                print("  Your inventory is empty.")
                seperator()
                input("~ Press enter to leave.")
                return
            for i, (item_id, amount) in enumerate(consum_inv.items(), start=1):
                item = load_consum(item_id)
                print(f" {i}. {item.name} x{amount}")
                print(f"  {item.description}")
            print()
            seperator()
            print(message)

            player_input = pinput()
            if not player_input.strip():
                continue
            command: str = player_input.split()[0]
            args: list[str] = player_input.split(maxsplit=1)[1].split() if len(player_input.split()) > 1 else []

            match command:
                case "exit" | "e":
                    showing_consum = False
                case "use" | "u":
                    if not args or not args[0].isnumeric():
                        message = "~ Specify an item number. e.g. 'use 1'"
                        continue
                    item_number: int = int(args[0]) - 1
                    if item_number < 0 or item_number >= len(consum_inv):
                        message = f"~ {item_number} is invalid"
                        continue
                    item_id: str = list(consum_inv.keys())[item_number]
                    item: Consumable = load_consum(item_id)
                    if item.use(self):
                        consum_inv[item_id] -= 1
                        message = f"~ Healed {item.data['type']} by {item.data['amount']}"
                    else:
                        message = f"~ Already at max {item.data["type"]}!"
                    if consum_inv[item_id] <= 0:
                        del consum_inv[item_id]
                case "discard" | "d":
                    if not args or not args[0].isnumeric():
                        message = "~ Specify an item number. e.g. 'discard 1'"
                        continue
                    item_number: int = int(args[0]) -1
                    if item_number < 0 or item_number >= len(consum_inv):
                        message = f"~ {item_number} id invalid"
                        continue
                    item_id: str = list(consum_inv.keys())[item_number]
                    item: Consumable = load_consum(item_id)
                    if yn(f"~ Are you sure you want to discard {item.name}? Y/N:"):
                        consum_inv[item_id] -= 1
                        if consum_inv[item_id] <= 0:
                            del consum_inv[item_id]
                    else:
                        print(f"~ {item.name} was not discarded!")
                case _:
                    message = f"~ {player_input} is not a valid command"
                    continue

    def show_equip(self):
        showing_equip: bool = True
        message = "~ Type the corresponding number to select item"
        while showing_equip:
            cls()
            print(f"\n[ Equipment Inventory ]")
            equip_inv: dict = self.inventory["equipment_inv"]
            if not equip_inv:
                print("  Your inventory is empty.")
                seperator()
                input("~ Press enter to leave.")
                return
            equip_list: list = []
            i = 1
            for equip_type, equip_ids in equip_inv.items():
                for equip_id in equip_ids:
                    split_id: list[str] = equip_id.split("_", 1)
                    prefix = split_id[0]
                    match prefix:
                        case "wep":
                            weapon: Weapon = Weapon.load(equip_id)
                            print(f" {i}. {weapon.name}")
                            print(f"  Damage: {weapon.calc_damage(self)}")
                            equip_list.append(weapon)
                        case "hdw":
                            ...
                        case "arm":
                            ...
                        case "grv":
                            ...
                        case "bts":
                            ...
                i += 1
            print()
            seperator()
            print(message)

            player_input = pinput()
            if not player_input.strip():
                continue
            command: str = player_input.split()[0]
            args: list[str] = player_input.split(maxsplit=1)[1].split() if len(player_input.split()) > 1 else []

            match command:
                case "equip":
                    item_number: str = ""
                    if args:
                        item_number: str = args[0]
                    else:
                        while True:
                            print("~ What item would you like to equip? Type in the corresponding number:")
                            player_input = pinput()
                            if not player_input.isnumeric():
                                pass
                            else:
                                item_number: int = int(player_input)
                                break
                    item_number: int = int(item_number) - 1
                    if item_number < 0 or item_number >= len(equip_list):
                        print(f"~ {item_number + 1} is invalid")
                        continue
                    item = equip_list[item_number]
                    if isinstance(item, Weapon):
                        if item.id == self.weapon.id:
                            print(f"You already have {item.name} equipped.")
                            dia_input()
                        else:
                            self.weapon = item
                            print(f"~ {item.name} equipped!")
                            dia_input()
                    # add armor later when implemented
                case "info":
                    item_number: str = ""
                    if args:
                        item_number = args[0]
                    else:
                        print("What item would you like to see?")

                        while True:
                            player_input = pinput()

                            if not player_input.isnumeric():
                                print(f"{player_input} is not a number")
                                continue
                            else:
                                item_number: str = player_input
                                break
                    message = "~ Type exit to leave."
                    while True:
                        item_number: int = int(item_number) - 1
                        if item_number < 0 or item_number >= len(equip_list):
                            message = f"~ {item_number + 1} is invalid"
                            break
                        equip_list[item_number].show_info(self)
                        print(message)

                        player_input = pinput()

                        match player_input:
                            case "exit" | "e":
                                break
                            case _:
                                message = f"~ {player_input} is not a valid command."
                case "exit" | "e":
                    break
                case _:
                    message = f"~ {command} is not a valid command."

    def show_inventory(self):
        showing_inv: bool = True
        message = "~ Type 1, 2 or 3 to access different parts of your inventory"
        while showing_inv:
            cls()
            print(f"\n[ Inventory ]")
            for i, (k, v) in enumerate(self.inventory.items(), start=1):
                match k:
                    case "consum_inv":
                        print(f"{i}. Consumable Inventory")
                        if not v:
                            print(" Consumable inventory is empty...")
                        else:
                            print("")
                    case "key_inv":
                        print(f"{i}. Key Item Invetory")
                        if not v:
                            print(" Key Item inventory is empty...")
                        else:
                            print("")
                    case "equipment_inv":
                        print(f"{i}. Equipment Inventory")
                        if not v:
                            print(" Equipment Inventory is empty...")
                        else:
                            print("")
            seperator()
            print(message)

            player_input: str = pinput()
            if not player_input.strip():
                continue

            command: str = player_input.split()[0]
            if len(player_input.split()) > 1:
                args: list = player_input.split(maxsplit=1)[1].split()

            match command:
                case "e" | "exit":
                    showing_inv = False
                case "1" | "consumable":
                    self.show_consum()
                case "2" | "key":
                    print("TBA")
                    pass
                case "3" | "equipment":
                    self.show_equip()
                    pass
                case _:
                    message = f"~ {command} is invalid"


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
                        dia_input()
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
                case _:
                    message = f"{player_input} is not a valid command."

    def display_battle(self):
        print(f"[ {self.name} ]")
        width: int = 20
        pct = self.hp / self.max_hp
        filled = int(pct * width)
        empty = width - filled
        print(f"HP: [{'█' * filled}{'░' * empty}] {self.hp}/{self.max_hp}")

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)
        if self.hp is 0:
            self.dead = True

    def level_up(self):
        while True:
            if self.exp >= self.exp_needed:
                remaining_exp: int = self.exp - self.exp_needed
                self.exp = remaining_exp
                self.level += 1
                base_exp = 100
                self.exp_needed = int(base_exp * (self.level ** 2.5))
                self.points += 5
                cls()
                print(f"{self.name} has leveled up to {self.level}!")
                dia_input()
            else:
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