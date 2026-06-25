from utils import cls, dia_input

class NPC:
    def __init__(self, name: str, sprite: str, dialogue: dict):
        self.name = name
        self.sprite = sprite
        self.dialogue = dialogue

    def speak(self, state: str = "default", **kwargs):
        lines: list[str] = self.dialogue.get(state, self.dialogue["default"])
        for line in lines:
            cls()
            print(self.sprite)
            print(f"[ {self.name} ]")
            print(f'"{line.format(**kwargs)}"')
            dia_input()

