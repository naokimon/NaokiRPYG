class Skill:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.desc: str = data["description"]
        self.dmg: int = data["dmg"]
        self.cost: int = data["cost"]
        self.type: str = data["type"]
        self.scaling: dict = data["scaling"]

    def execute(self, player, target):
        # check if the mana is 0 to not do attack