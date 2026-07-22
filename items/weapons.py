from __future__ import annotations
from typing import TYPE_CHECKING
import json
from pathlib import Path

from PyInstaller.compat import check_requirements

from utils import cls, seperator

if TYPE_CHECKING:
    from entities.player import Player

root: Path = Path(__file__).parent.parent

class Weapon:
    def __init__(self, wep_data: dict):
        self.name: str = wep_data["name"]
        self.id: str = wep_data["id"]
        self.base_atk: int = wep_data["atk"]
        self.requirement: dict = wep_data["requirements"]
        self.scaling: dict = wep_data["scaling"]

    def calc_damage(self, player: Player) -> int:
        stat_amount: int = player.get_stat(self.scaling["stat"])
        scale: float = self.scaling["scale"]
        return int(self.base_atk + (stat_amount * scale))

    def check_requirements(self, print_falses: bool, player: Player) -> bool:
        bool_list: list[bool] = []
        for requirement in self.requirement:
            requirement_stat: int = self.requirement[requirement]
            player_stat: int = getattr(player.stats, requirement)
            if player_stat >= requirement_stat:
                bool_list.append(True)
            else:
                bool_list.append(False)
        requirement_list: list[str] = list(self.requirement.keys())
        if print_falses:
            for i, boolean in enumerate(bool_list):
                if not boolean:
                    print(f"You require more {requirement_list[i]}!")

        return all(bool_list)


    def show_info(self, player: Player):
        cls()
        print(f"[ {self.name}'s info ]")
        print(f"Base Attack: {self.base_atk}")
        print(f"Requirements met: {"true" if self.check_requirements(False, player) else "false"}")
        if self.check_requirements(False, player):
            print(f"Current damage: {self.calc_damage(player)}")
        requirement_list: list[str] = list(self.requirement.keys())
        print("Requirements:")
        for requirement in requirement_list:
            print(f"~ {requirement.capitalize()}: {self.requirement[requirement]}")
        print(f"Scales with: {self.scaling["stat"].capitalize()}")
        print(f"Scaling: {self.scaling["scale"]}x")
        seperator()

    @classmethod
    def load(cls, wep_id):
        weapons_path: Path = root / "data" / "items" / "weapons.json"
        with open(weapons_path) as f:
            weapons_data: dict = json.load(f)

        if wep_id not in weapons_data:
            raise ValueError(f"Unknown weapon id: {wep_id}")

        return cls(weapons_data[wep_id])