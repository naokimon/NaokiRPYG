from utils import cls, pinput, yn
from entities.player import Player

def charactercreation():
    cls()

    print("What is your name..?")

    while True:
        name = pinput()

        if yn(f"Are you sure your name is {name}? Y/N"):
            break

    rpg_class: str = ""
    while True:
        print("Choose your class...")
        print(r"""1. Warrior
2. Mage
3. Rogue
4. Cleric
5. Archer
            """)

        choice: str = pinput().lower().strip()

        match choice:
            case "1" | "warrior":
                rpg_class = "warrior"
            case "2" | "mage":
                rpg_class = "mage"
            case "3" | "rogue":
                rpg_class = "rogue"
            case "4" | "cleric":
                rpg_class = "cleric"
            case "5" | "archer":
                rpg_class = "archer"
            case _:
                print("Enter a valid number or class.")
                continue

        if yn(f"Are you sure you want to start as a {rpg_class}? Y/N"):
            break

    print(f"You are now {name}, the {rpg_class.capitalize()}!")
    player: Player = Player(rpg_class, name)
    player.display_stats()
charactercreation()