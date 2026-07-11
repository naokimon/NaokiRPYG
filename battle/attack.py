class Attack:
    def __init__(self, data: dict):
        self.atk_id = data["id"]
        self.name = data["name"]
        self.damage = data["damage"]
        self.cost = data["cost"]

    def execute(self, attacker, target):
        attacker.mp -= max(0, attacker.mp - self.cost)
        target.take_damage(self.damage)
        print(f"~ {attacker.name} used {self.name} on {target.name} for {self.damage}!")

