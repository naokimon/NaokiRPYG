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

def load_enemy(id: str):
    is_boss: bool = False
    if "boss" in id:
        is_boss = True

    if is_boss:
        boss_file = id.rsplit("_", 1)[0]
        boss_file = boss_file.split("_", 1)[1] + ".json"
        boss_path: Path = root / "data" / "boss" / boss_file
        with open(boss_path) as f:
            boss_json: dict = json.load(f)
        if boss_json.get(id):
            match id:
                case "boss_wolf_alpha_1":
                    return WolfBoss(boss_json[id])
        else:
            raise ValueError(f"Unknown boss ID: {id}")
    else:
        enemy_file = id.rsplit("_", 1)[0] + ".json"
        enemies_path: Path = root / "data" / "enemies" / enemy_file
        with open(enemies_path) as f:
            enemy_json: dict = json.load(f)
        if enemy_json.get(id):
            return Enemy(enemy_json[id])
        else:
            raise ValueError(f"Unknown enemy ID: {id}")

class Enemy:
    def __init__(self, data: dict):
        self.eid: str = data["id"]
        self.name: str = data["name"]
        self.max_hp: int = data["hp"]
        self.hp: int = data["hp"]
        self.max_mp: int = data["mp"]
        self.mp: int = data["mp"]
        self.weakness: str = data["weakness"]
        self.attacks: list[str] = data["attacks"]
        self.exp_reward: int = data["exp_reward"]
        self.drops: dict = data["drops"]
        self.dead: bool = False
        self.debuffs: dict[str, dict] = {}
        self.defense: float = 0

    def display_enemy(self):
        debuff_str: str = ""
        if self.debuffs:
            debuff_str = ", ".join(
                f"{'Poisoned' if s == 'poison' else 'Burned'} ({d['duration']} turns)" for s, d in self.debuffs.items())
        print(f"[ {self.name} {debuff_str}]")
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
        if "dazed" in self.debuffs:
            print(f"~ {self.name} was too dazed to attack!")
        else:
            atk_data = data[atk_id]

            attack: Attack = Attack(atk_data)
            attack.execute(self, player)

    def take_damage(self, amount: int) -> int:
        damage: int = int(amount - (amount * self.defense))
        self.hp = max(0, self.hp - damage)
        if self.hp == 0:
            self.dead = True
        return damage

    def apply_debuff(self, debuff_data):
        if self.debuffs.get(debuff_data["tick_status"]) is None:
            self.debuffs[debuff_data["tick_status"]] = {
                "damage": debuff_data["tick_damage"],
                "duration": debuff_data["tick_duration"]
            }
            return True
        else:
            return False

    def remove_debuff(self, status: str):
        self.debuffs.pop(status, None)
        print(f"~ {status.capitalize()} has worn off on {self.name}!")

    def tick_debuff(self):
        for status, debuff in list(self.debuffs.items()):
            damage = int(self.max_hp * debuff["damage"])
            self.take_damage(damage)
            print(f"~ {'Poisoned' if status == 'poison' else 'Burned'} for {damage} damage!")
            self.debuffs[status]["duration"] -= 1
            if self.debuffs[status]["duration"] == 0:
                self.remove_debuff(status)

    def get_drops(self, player: Player) -> list:
        x: int = 0
        drops_rewarded: list = []
        DROPS_REROLL: int = 2
        while x < DROPS_REROLL:
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

class WolfBoss(Enemy):
    def __init__(self, data: dict):
        super().__init__(data)
        self.defense: float = data["defense"]
        self.attack_list: list[str] = ["alpha_bite", "savage_howl", "rending_claws"]
        self.charge_attack: str = "feral_lunge"
        self.charging: bool = False
        self.phase_2: bool = False

    def choose_attack(self, data: dict):
        if self.hp / self.max_hp > 0.75:
            atk_id: str = random.choice(self.attack_list)
            return atk_id
        else:
            if not self.phase_2:
                self.phase_2 = True
                self.attack_list.append(self.charge_attack)
                return self.charge_attack
            else:
                atk_id: str = random.choice(self.attack_list)
                return atk_id

    def attack(self, player: Player):
        data = load_attacks()
        if not self.charging:
            atk_id: str = self.choose_attack(data)
            if atk_id == self.charge_attack:
                self.charging = True
                print(f"~ {self.name} poises for a strong lunge!")
            else:
                if "dazed" in self.debuffs:
                    print(f"~ {self.name} fought through the daze!")

                atk_data = data[atk_id]

                attack: Attack = Attack(atk_data)
                attack.execute(self, player)
        else:
            atk_data = data[self.charge_attack]

            attack: Attack = Attack(atk_data)
            attack.execute(self, player)

class FireDrake(Enemy):
    def __init__(self, data: dict):
        super().__init__(data)
        self.defense: float = data["defense"]
        self.attack_list: list[str] = ["dragon_bite", "fire_breath", "tail_sweep"]
        self.charge_attack: str = "inferno_roar"
        self.charging: bool = False
