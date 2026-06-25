from ascii import asciis
import os
from utils import pinput
from game import charactercreation
from entities.player import Player

def main():
    print(asciis["title"])
    choosing: bool = True
    while choosing:
        menu_input: list[str] = pinput().lower().strip().split()
        choice: str = menu_input[0]

        match choice:
            case "1":
                player = charactercreation()
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


if __name__ == "__main__":
    main()