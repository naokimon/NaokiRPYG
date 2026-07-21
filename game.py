import sys
from battle.battle import Battle
from entities.enemy import Enemy
from utils import cls, pinput, seperator
from entities.player import Player
from world.zones import Zone
from data.ascii import asciis
from npc import NPC
from data.dialogue import king

class Game:
    def __init__(self):
        self.player: Player | None = None
        self.current_zone: Zone | None = None
        self.running: bool = False

    def start(self):
        self.running = True
        self.main_menu()

    def main_menu(self):
        print(asciis["title"])
        choosing: bool = True
        while choosing:
            menu_input: list[str] = pinput().lower().strip().split()
            choice: str = menu_input[0]

            match choice:
                case "1":
                    cls()
                    self.player = Player.charactercreation()
                    self.tutorial()
                    choosing = False
                case "2":
                    player: Player = Player("warrior", "John Doe")
                    player.load_game()
                case "3":
                    print("Config")
                case "4":
                    print("Exiting...")
                    sys.exit()
                case _:
                    print("Choose a valid option.")

    def tutorial(self):
        npc_king: NPC = NPC(king["name"], king["sprite"], king["dialogue"])

        npc_king.speak(state="tutorial", PLAYER_NAME=self.player.name)

    def display_game(self):
        self.player.display_info()

        self.current_zone.display()

    def game_loop(self):
        self.current_zone = Zone.create_zone(self.player)
        message: str = "~ Type options to see all available commands"
        while True:
            cls()
            self.display_game()

            seperator()
            print(message)

            player_input = pinput()
            if not player_input.strip():
                continue

            command: str = player_input.split()[0]
            if len(player_input.split()) > 1:
                args: list = player_input.split(maxsplit=1)[1].split()

            zone = self.current_zone

            match command:
                case "forward":
                    message = zone.move_forward()
                case "back":
                    message = zone.move_back()
                case "inventory" | "inv":
                    self.player.show_inventory()
                case "stats" | "stat":
                    self.player.show_stats()
                case "battle" | "b":
                    if not zone.current_room.room_id in zone.cleared_rooms:
                        enemy_list: list[Enemy] = []
                        enemies = self.current_zone.current_room.enemies
                        for i, enemy in enumerate(enemies):
                            enemy_id: str = enemy[0]
                            enemy_amount: int = enemy[1]
                            if enemy_amount > 1:
                                for e in range(enemy_amount):
                                    enemy_obj: Enemy = Enemy.load(enemy_id)
                                    enemy_list.append(enemy_obj)
                            else:
                                enemy_obj: Enemy = Enemy.load(enemy_id)
                                enemy_list.append(enemy_obj)
                        battle: Battle = Battle(self.player, enemy_list)
                        if not battle.battle():
                            cls()
                            self.main_menu()
                        else:
                            zone.cleared_rooms.add(zone.current_room.room_id)
                    else:
                        message = f"~ Room has already been cleared."
                case _:
                    message = "~ Type options to see all available commands"

    def set_player(self, player: Player):
        self.player = player


