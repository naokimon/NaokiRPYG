from __future__ import annotations
import random
from entities.player import Player
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.enemy import Enemy

root: Path = Path(__file__).parent.parent

class Skill:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.desc: str = data["description"]
        self.dmg: int = data["dmg"]
        self.cost: int = data["cost"]
        self.accuracy: float = data["accuracy"]
        self.type: str = data["type"]
        self.scaling: dict = data["scaling"]

    def calc_damage(self, player: Player, target: Enemy) -> int:
        WEAKNESS_MULTIPLIER: int = 2
        stat_amount: int = getattr(player.stats, self.scaling["stat"])
        damage = int(self.dmg + (stat_amount * self.scaling["scale"]))
        if target.weakness == self.type:
            damage = damage * WEAKNESS_MULTIPLIER
        return damage

    def execute(self, player: Player, target):
        player.mp = max(0, player.mp - self.cost)
        if random.random() <= self.accuracy:
            target.take_damage(self.calc_damage())
            print(f"~ {player.name} used {self.name} on {target.name} for {self.calc_damage()}")
        else:
            print(f"~ {player.name} used {self.name} on {target.name} and missed!")


def load_skill(sid: str) -> Skill:
    skill_path: Path = root / "data" / "skills.json"
    with open(skill_path) as f:
        data = json.load(f)

    return Skill(data[sid])

skill: Skill = load_skill("shoulder_bash")
print(skill.name)