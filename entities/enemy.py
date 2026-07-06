from pathlib import Path
import json
import random
from battle.attack import Attack

root: Path = Path(__file__).parent.parent

class Enemy:
    def __init__(self, data: dict):
        self.eid = data["id"]
        self.name = data["name"]
        self.max_hp = data["hp"]
        self.hp = data["hp"]
        self.max_mp = data["mp"]
        self.mp = data["mp"]
        self.attacks = data["attacks"]

    @classmethod
    def load(cls, eid: str):
        enemy_file = eid.split("_", 1)[0] + ".json"
        enemies_path: Path = root / "data" / "enemies" / enemy_file
        with open(enemies_path) as f:
            enemy_json: dict = json.load(f)
        if enemy_json.get(eid):
            return cls(enemy_json[eid])
        else:
            raise ValueError(f"Unknown enemy ID: {eid}")

    def display_enemy(self):
        print(f"[ {self.name} ]")
        width: int = 20
        pct = self.hp / self.max_hp
        filled = int(pct * width)
        empty = width - filled
        print(f"HP: [{'█' * filled}{'░' * empty}] {self.hp}/{self.max_hp}")

    def choose_attack(self) -> str:
        available = [a for a in self.attacks if self.mp >= a["cost"]]
        return random.choice(available)

    def attack(self):
        atk_id: str = self.choose_attack()
        attack_path: Path = root / "data" / "attacks.json"
        with open(attack_path) as f:
            data: dict = json.load(f)
        if data.get(atk_id):
            atk_data = data[atk_id]
        else:
            raise ValueError(f"Unknown attack ID: {atk_id}")




goblin: Enemy = Enemy.load("goblin_1")
goblin.display_enemy()