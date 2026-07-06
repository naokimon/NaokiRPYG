class Attack:
    def __init__(self, data: dict):
        self.atk_id = data["id"]
        self.name = data["name"]
        self.damage = data["damage"]
        self.cost = data["cost"]

    def execute(self, attacker, target):
        attacker.mp -= self.cost
        target.hp -= self.damage
        print(f"~ {attacker.name} used {self.name} on {target.name} for {self.damage}!")

