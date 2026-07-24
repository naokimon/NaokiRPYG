from __future__ import annotations
import random
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player
    from entities.enemy import Enemy

root: Path = Path(__file__).parent.parent

def load_skill(sid: str) -> Skill:
    skill_path: Path = root / "data" / "skills.json"
    with open(skill_path) as f:
        data = json.load(f)

    skill_data: dict = data[sid]

    match skill_data["type"]:
        case "attack":
            return AttackSkill(skill_data)
        case "buff":
            return BuffSkill(skill_data)
        case _:
            raise ValueError(f"Skill {sid} not found")

class Skill:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.desc: str = data["description"]
        self.amount: int = data["amount"]
        self.cost: int = data["cost"]
        self.accuracy: float = data["accuracy"]
        self.element: str = data["element"]
        self.type: str = data["type"]
        self.scaling: dict = data["scaling"]

    def execute(self, player: Player, target):
        pass

class AttackSkill(Skill):
    def __init__(self, data: dict):
        super().__init__(data)
        debuff = all(k in data for k in ["tick_damage", "tick_status", "tick_duration"])
        if debuff:
            self.debuff = True
            self.t_damage = data["tick_damage"]
            self.t_status = data["tick_status"]
            self.t_duration = data["tick_duration"]

    def calc_damage(self, player: Player, target: Enemy) -> int:
        WEAKNESS_MULTIPLIER: int = 2
        stat_amount: int = getattr(player.stats, self.scaling["stat"])
        damage = int(self.amount + (stat_amount * self.scaling["scale"]))
        if target.weakness == self.element:
            damage = damage * WEAKNESS_MULTIPLIER
        return damage

    def execute(self, player: Player, target):
        player.mp = max(0, player.mp - self.cost)
        damage: int = self.calc_damage(player, target)
        if random.random() <= self.accuracy:
            target.take_damage(damage)
            status_text = ""
            if self.debuff:
                debuff_data = {
                    "tick_damage": self.t_damage,
                    "tick_status": self.t_status,
                    "tick_duration": self.t_duration
                }
                if target.apply_debuff(debuff_data):
                    status_text = f" and {'poisoned' if self.t_status == 'poison' else 'burned'} them"
            print(f"~ {player.name} used {self.name} on {target.name} for {damage}{status_text}!")
        else:
            print(f"~ {player.name} used {self.name} on {target.name} and missed!")

class BuffSkill(Skill):
    def __init__(self, data: dict):
        super().__init__(data)
        self.duration: int = data["duration"]

    def execute(self, player: Player, target):
        player.mp = max(0, player.mp - self.cost)
        if random.random() <= self.accuracy:
            if player.apply_buff(self):
                print(f"~ {player.name} used {self.name}")
            else:
                print(f"~ {player.name} already used {self.name}")
        else:
            print(f"~ {player.name} used {self.name} but it failed...")