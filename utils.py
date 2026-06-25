import os
from pathlib import Path
import json
from entities.player import Player, Stats

root: Path = Path(__file__).parent

def cls() -> None:
    os.system("CLS")

def pinput() -> str:
    inp: str = input(">_ ")
    return inp

def yn(text: str | None = None) -> bool:
    if text:
        print(text)
    else:
        print("Are you sure? Y/N:")
    while True:
        choice: str = pinput().lower().strip()

        if choice in ["y", "yes", "yeah"]:
            return True
        elif choice in ["n", "no", "nah"]:
            return False
        else:
            print("Enter a valid option")
