from utils import cls, pinput, yn
from entities.player import Player
from rooms import Room
from data.ascii import asciis
import os
from npc import NPC
from data.dialogue import king

class Game:
    def __init__(self):
        self.player: Player | None = None
        self.current_room: Room | None = None
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
                    os.abort()
                case _:
                    print("Choose a valid option.")

    def tutorial(self):
        npc_king: NPC = NPC(king["name"], king["sprite"], king["dialogue"])

        npc_king.speak(state="tutorial", PLAYER_NAME=self.player.name)
