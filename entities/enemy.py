from pathlib import Path
import json
import random
from battle.attack import Attack
from entities.player import Player
from items.weapons import Weapon
from items.consumables import load_consum, Consumable

root: Path = Path(__file__).parent.parent

def load_attacks() -> dict:
    attack_path: Path = root / "data" / "attacks.json"
    with open(attack_path) as f:
        return json.load(f)

class Enemy:
    def __init__(self, data: dict):
        self.eid: str = data["id"]
        self.name: str = data["name"]
        self.max_hp: int = data["hp"]
        self.hp: int = data["hp"]
        self.max_mp: int = data["mp"]
        self.mp: int = data["mp"]
        self.attacks: list[str] = data["attacks"]
        self.exp_reward: int = data["exp_reward"]
        self.drops: dict = data["drops"]
        self.dead: bool = False

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

    def choose_attack(self, data: dict) -> str:
        available = [data[a] for a in self.attacks if a in data and self.mp >= data[a]["cost"]]
        attack_data = random.choice(available)
        return attack_data["id"]

    def attack(self, player: Player):
        data = load_attacks()
        atk_id: str = self.choose_attack(data)
        atk_data = data[atk_id]

        attack: Attack = Attack(atk_data)
        attack.execute(self, player)

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)
        if self.hp is 0:
            self.dead = True

    def get_drops(self, player: Player) -> list:
        x: int = 0
        drops_rewarded: list = []
        while x < 2: # rerolls voor drops
            for i_type, drop_list in self.drops.items():
                for drop in drop_list:
                    if random.random() < drop["chance"]:
                        match i_type:
                            case "consum":
                                consum_inv: dict = player.inventory["consum_inv"]
                                consum_inv[drop["id"]] = consum_inv.get(drop["id"], 0) + 1
                                consumable: Consumable = load_consum(drop["id"])
                                drops_rewarded.append(consumable)
                            case "equip":
                                match drop["type"]:
                                    case "weapon":
                                        equip_inv: dict = player.inventory["equipment_inv"]
                                        type_list: list = equip_inv[drop["type"]]
                                        if not drop["id"] in type_list:
                                            type_list.append(drop["id"])
                                            weapon: Weapon = Weapon.load(drop["id"]) # add armor cases later
                                            drops_rewarded.append(weapon)
                            case "key":
                                key_inv: dict = player.inventory["key_inv"]
                                key_inv[drop["id"]] = key_inv.get(drop["id"], 0) + 1 # add key item to list later
            x += 1
        return drops_rewarded