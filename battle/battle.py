from __future__ import annotations
from typing import TYPE_CHECKING
from entities.enemy import Enemy
from data.ascii import asciis
from utils import seperator, pinput, cls, dia_input
from items.weapons import Weapon
from battle.skills import load_skill, Skill

if TYPE_CHECKING:
    from entities.player import Player

class Battle:
    def __init__(self, player: Player, enemies: list[Enemy]):
        self.player = player
        self.enemies = enemies
        self.target = enemies[0]
        self.running = True

    def display(self):
        cls()
        print("\n[ Battle ]")
        print("\nEnemies:")
        for enemy in self.enemies:
            enemy.display_enemy()
        print("\nPlayer:")
        self.player.display_battle()
        print(f"~ Target: {self.target.name} {self.target.hp}/{self.target.max_hp}")
        print(f"~ Buffs:")
        if len(self.player.buffs) == 0:
            print("None")
        else:
            for b in self.player.buffs:
                buff: Skill = load_skill(b)
                print(f"{buff.name}: {buff.desc}")

    def player_turn(self):
        message: str = "~ Type options for all options"
        action_taken: bool = False
        player: Player = self.player
        while not action_taken:
            self.display()
            seperator()
            print(message)

            player_input = pinput()
            if not player_input.strip():
                continue

            command: str = player_input.split()[0]
            if len(player_input.split()) > 1:
                args: list = player_input.split(maxsplit=1)[1].split()
            else:
                args: list = []

            match command:
                case "attack" | "atk":
                    weapon: Weapon = player.weapon
                    damage = weapon.calc_damage(player)
                    if self.target.dead:
                        message = f"~ {self.target.name} is already dead!"
                        continue
                    else:
                        self.target.take_damage(damage)
                        print(f"~ {player.name} dealt {damage} damage to {self.target.name}!")
                        if self.target.dead:
                            alive = [e for e in self.enemies if not e.dead]
                            if alive:
                                self.target = alive[0]
                        dia_input()
                        action_taken = True
                case "skills" | "s":
                    if len(player.skills) == 0:
                        print("You have no skills.")
                        dia_input()
                        continue
                    else:
                        for i, s in enumerate(player.skills, start=1):
                            skill: Skill = load_skill(s)
                            print(f"{i}. {skill.name} | Cost: {skill.cost}")
                            print(f"~ {skill.desc}")
                    print()
                    chosen_skill: bool = False
                    while not chosen_skill:
                        print("What skill would you like to use?")
                        player_input: str = pinput()
                        if player_input.isnumeric():
                            skill_number: int = int(player_input) - 1
                            skill = load_skill(player.skills[skill_number])
                            if player.mp >= skill.cost:
                                skill.execute(player, self.target)
                                dia_input()
                                chosen_skill: bool = True
                                action_taken = True
                                if self.target.dead:
                                    alive = [e for e in self.enemies if not e.dead]
                                    if alive:
                                        self.target = alive[0]
                            else:
                                print("Not enough mana!")
                                dia_input()
                                break
                        else:
                            print(f"{player_input} is not a number.")
                            pass
                case "target" | "t":
                    if not args:
                        print("Who would you like to target?")
                        for i, enemy in enumerate(self.enemies, start=1):
                            print(f"{i}. {enemy.name} {enemy.hp}/{enemy.max_hp}")
                        while True:
                            command: str = pinput()

                            if not command.isnumeric():
                                print("Please enter a number. e.g. 1")
                            else:
                                if int(command) > len(self.enemies):
                                    print(f"{command} is not in range of amount of enemies")
                                else:
                                    self.target = self.enemies[int(command) - 1]
                                    print(f"Target is now {self.target.name}!")
                                    dia_input()
                                    break
                    else:
                        num: str = args[0]
                        if not num.isnumeric():
                            message = f"~ {args[0]} is not a number!"
                        else:
                            target_num: int = int(num) - 1
                            if target_num >= len(self.enemies):
                                message = f"~ {target_num + 1} is not in range of amount of enemies"
                            else:
                                self.target = self.enemies[target_num]
                                print(f"Target is now {self.target.name}!")
                                dia_input()
                case _:
                    message = f"~ {player_input} is not a valid command"

        player.tick_buff()
        for enemy in self.enemies:
            enemy.tick_debuff()

    def enemy_turn(self):
        for enemy in self.enemies:
            if self.player.dead:
                break
            if enemy.hp > 0:
                self.display()
                seperator()
                print(f"~ {enemy.name}'s turn.")

                enemy.attack(self.player)
                dia_input()

    def calc_enemy_hp(self):
        total: int = 0
        for enemy in self.enemies:
            total += enemy.hp

        return total

    def win_screen(self):
        cls()
        print(asciis["win_screen"])
        seperator()
        dia_input()

        for enemy in self.enemies:
            self.player.exp += enemy.exp_reward
        self.player.level_up()

        all_drops: list = []
        for enemy in self.enemies:
            all_drops += enemy.get_drops(self.player)

        drop_counts: dict = {}
        for item in all_drops:
            drop_counts[item.name] = drop_counts.get(item.name, 0) + 1

        if len(all_drops) > 0:
            cls()
            for name, amount in drop_counts.items():
                print(f"{amount}x {name}")
            dia_input()

    def lose_screen(self):
        cls()
        print(asciis["lose_screen"])
        seperator()
        dia_input()
        return False

    def battle(self) -> bool:
        while self.running:
            if self.player.dead:
                return self.lose_screen()
            else:
                self.player_turn()

            if self.calc_enemy_hp() == 0: # dead
                self.win_screen()
                break
            else: # alive
                self.enemy_turn()
        return True

