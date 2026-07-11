from pathlib import Path
import json
from entities.player import Player
import random
from world.rooms import Room
from items.consumables import load_consum
from entities.enemy import Enemy

root: Path = Path(__file__).parent.parent

class Zone:

    zone_count: int = 1

    def __init__(self, zone_id: str, name: str, description: str, rooms: list[dict], entry_room: str, zone_data: dict):
        self.zone_id: str = zone_id
        self.name: str = name
        self.description: str = description
        self.rooms: list[dict] = rooms
        self.entry_room: str = entry_room
        self.zone_data: dict = zone_data
        self.current_room: Room = Room.load(self.entry_room, self.zone_data["rooms"])
        self.cleared_rooms: set[str] = set() # finish adding cleared rooms
        Zone.zone_count += 1

        if Zone.zone_count > 5:
            Zone.zone_count = 1

    @classmethod
    def create_zone(cls, player: Player):
        zones_path: Path = root / "data" / "zones" / str(Zone.zone_count)
        files: list[Path] = sorted(zones_path.glob("*.json"))
        zone_path: Path = random.choice(files)

        with open(zone_path) as f:
            zone_data: dict = json.load(f)

        return cls(
            zone_data["id"],
            zone_data["name"],
            zone_data["description"],
            zone_data["rooms"],
            zone_data["entry_room_id"],
            zone_data,
        )

    def display(self):
        print(f"{self.name} — {self.current_room.name}")
        print()

        if not self.current_room.room_id in self.cleared_rooms:
            if self.current_room.enemies:
                enemies_str = ", ".join(f"{count}x {Enemy.load(eid).name}" for eid, count in self.current_room.enemies)
                print(enemies_str)
        else:
            print("Room has been cleared!")

        if self.current_room.items:
            for item_id, amount in self.current_room.items:
                item = load_consum(item_id)
                print(f"  {item.name} x{amount}")

        if self.current_room.npc:
            print(f"NPC:  {self.current_room.npc}")

        print()
        exits = [k for k, v in self.current_room.exits.items() if v is not None]
        print(f"Exits: {', '.join(exits)}")

    def move_forward(self):
        next_room_id: str = self.current_room.exits["forward"]
        if next_room_id is None:
            return f"~ Are you ready to leave..?"
        else:
            self.current_room: Room = Room.load(next_room_id, self.zone_data["rooms"])
            return f"~ You moved forward towards {self.current_room.name}"

    def move_back(self):
        previous_room_id: str = self.current_room.exits["back"]
        if previous_room_id is None:
            return f"~ There is nothing behind you..."
        else:
            self.current_room: Room = Room.load(previous_room_id, self.zone_data["rooms"])
            return f"~ You moved back to {self.current_room.name}"




