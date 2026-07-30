import os
from pathlib import Path

root: Path = Path(__file__).parent

def cls() -> None:
    os.system("CLS")

def pinput() -> str:
    inp: str = input(">_ ").lower()
    return inp

def dia_input() -> None:
    input("~ Press enter to continue")

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

def seperator(outer_sym: str | None = None, inner_sym: str | None = None):
    width: int = os.get_terminal_size().columns
    if outer_sym:
        print(outer_sym + "-" * (width - (len(outer_sym * 2))) + outer_sym)
    elif outer_sym and inner_sym:
        print(outer_sym + inner_sym * (width - (len(outer_sym * 2))) + outer_sym)
    elif inner_sym:
        print("+" + inner_sym * (width - 2) + "+")
    else:
        print("+" + "-" * (width - 2) + "+")