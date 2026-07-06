from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
import json

if TYPE_CHECKING:
    from entities.player import Player

root: Path = Path(__file__).parent.parent

class Consumable:
    def __init__(self, data: dict, name: str, description: str):
        self.data = data
        self.name = name
        self.description = description

    def use(self, player: Player):
        player.hp = min(player.hp, player.max_hp)
        player.mp = min(player.mp, player.max_mp)


class HealingPotion(Consumable):
    def __init__(self, data: dict, name: str, description: str):
        super().__init__(data, name, description)
        self.amount = data["amount"]

    def use(self, player: Player) -> bool:
        old_hp = player.hp
        player.hp += self.amount
        super().use(player)
        healed = player.hp - old_hp
        if healed <= 0:
            return False
        else:
            return True


class ManaPotion(Consumable):
    def __init__(self, data: dict, name: str, description: str):
        super().__init__(data, name, description)
        self.amount = data["amount"]

    def use(self, player: Player) -> bool:
        old_mp = player.mp
        player.mp += self.amount
        super().use(player)
        healed = player.mp - old_mp
        if healed <= 0:
            return False
        else:
            return True

def load_consum(iid: str):
    consum_path: Path = root / "data" / "items" / "consumables.json"
    with open(consum_path) as f:
        consum_data = json.load(f)

    data = consum_data[iid]

    match data["type"]:
        case "health":
            return HealingPotion(data, data["name"], data["description"])
        case "mana":
            return ManaPotion(data, data["name"], data["description"])
        case _:
            raise ValueError(f"Unknown consumable type: {data['type']}")
