from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

class Weapon:
    def __init__(self, player: Player, wep_data: dict):
        self.player = player
        self.name: str = wep_data["name"]
        self.id: str = wep_data["id"]
        self.base_atk: int = wep_data["atk"]
        self.requirement: dict = wep_data["requirements"]
        self.scaling: dict = wep_data["scaling"]

    def calc_damage(self) -> float:
        stat_amount: int = getattr(self.player.stats, self.scaling["stat"])
        scale: float = self.scaling["scale"]
        return self.base_atk + (stat_amount * scale)