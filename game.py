import sys
import os
from sys import displayhook

from utils import cls, pinput
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
        self.player.display_stats()

        self.current_zone.display()

    def game_loop(self):
        self.current_zone = Zone.create_zone(self.player)
        message: str = "~ Type options to see all available commands"
        while True:
            cls()
            self.display_game()
            print(message)
            width: int = os.get_terminal_size().columns

            print(f"+{"-" * (width - 2)}+")

            player_input = pinput()
            command: str = player_input.split()[0]
            if len(player_input.split()) > 1:
                args: list = player_input.split(maxsplit=1)[1].split()

            zone = self.current_zone

            match command:
                case "forward":
                    message = zone.move_forward()
                case "back":
                    message = zone.move_back()
                case _:
                    message = "~ Type options to see all available commands"

    def set_player(self, player: Player):
        self.player = player


test_player: Player = Player("warrior", "testarious")
test_game: Game = Game()
test_game.set_player(test_player)
test_game.game_loop()