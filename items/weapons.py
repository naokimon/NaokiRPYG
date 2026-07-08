from __future__ import annotations
from typing import TYPE_CHECKING
import json
from pathlib import Path

if TYPE_CHECKING:
    from entities.player import Player

root: Path = Path(__file__).parent.parent

class Weapon:
    def __init__(self, player: Player, wep_data: dict):
        self.player = player
        self.name: str = wep_data["name"]
        self.id: str = wep_data["id"]
        self.base_atk: int = wep_data["atk"]
        self.requirement: dict = wep_data["requirements"]
        self.scaling: dict = wep_data["scaling"]

    def calc_damage(self) -> int:
        stat_amount: int = getattr(self.player.stats, self.scaling["stat"])
        scale: float = self.scaling["scale"]
        return int(self.base_atk + (stat_amount * scale))

    @classmethod
    def load(cls, player: Player, wep_id):
        weapons_path: Path = root / "data" / "items" / "weapons.json"
        with open(weapons_path) as f:
            weapons_data: dict = json.load(f)

        if wep_id not in weapons_data:
            raise ValueError(f"Unknown weapon id: {wep_id}")

        return cls(player, wep_id["id"])