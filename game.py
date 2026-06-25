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
                    self.charactercreation()
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

    def charactercreation(self):
        cls()

        print("What is your name..?")

        while True:
            name = pinput()

            if yn(f"Are you sure your name is {name}? Y/N"):
                break

        rpg_class: str = ""
        while True:
            print("Choose your class...")
            classes: list[str] = ["warrior", "mage", "rogue", "cleric", "archer"]
            for index, rclass in enumerate(classes, start=1):
                print(f"{index}. {rclass.capitalize()}")

            choice: str = pinput().lower().strip()

            if choice in classes:
                rpg_class = choice
            elif choice.isdigit() and 1 <= int(choice) <= len(classes):
                rpg_class = classes[int(choice) - 1]
            else:
                print("Enter a valid number or class.")
                continue

            if yn(f"Are you sure you want to start as a {rpg_class}? Y/N"):
                break

        print(f"You are now {name}, the {rpg_class.capitalize()}!")
        player: Player = Player(rpg_class, name)
        self.player = player

    def tutorial(self):
        npc_king: NPC = NPC(king["name"], king["sprite"], king["dialogue"])

        npc_king.speak(state="tutorial", PLAYER_NAME=self.player.name)
