class Room:

    def __init__(self, room_id: str, name: str, exits: dict, enemies: list[tuple[str, int]], items: list[tuple[str, int]],  npc: str):
        self.room_id = room_id
        self.name = name
        self.exits = exits
        self.enemies: list[tuple[str, int]] = enemies
        self.items: list[tuple[str, int]] = items
        self.npc = npc

    @classmethod
    def load(cls, room_id: str, room_data: list):
        data = next((r for r in room_data if r["id"] == room_id), None)
        if data is None:
            raise RuntimeError(f"Room '{room_id}' was not found.")
        return cls(
            room_id=data["id"],
            name=data["name"],
            exits=data["exits"],
            enemies=data.get("enemies", []),
            items=data.get("items", []),
            npc=data.get("npc", None)
        )