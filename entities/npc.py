import json
from utils import cls, dia_input, root
from pathlib import Path
from gamedata.ascii import asciis

class NPC:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.sprite = asciis[data["sprite_id"]]
        self.dialogue = data["dialogue"]

    def speak(self, state: str = "default", **kwargs):
        lines: list[str] = self.dialogue.get(state, self.dialogue["default"])
        for line in lines:
            cls()
            print(self.sprite)
            print(f"[ {self.name} ]")
            print(f'"{line.format(**kwargs)}"')
            dia_input()

    @classmethod
    def load(cls, npc_id):
        npc_path: Path = root / "gamedata" / "npc.json"
        with open(npc_path) as f:
            data: dict = json.load(f)

        return cls(data[npc_id])