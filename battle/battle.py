from __future__ import annotations
from typing import TYPE_CHECKING
from entities.enemy import Enemy

if TYPE_CHECKING:
    from entities.player import Player

class Battle:
    def __init__(self, player: Player, enemies: list[Enemy]):
        self.player = player
        self.enemies = enemies
        self.target = enemies[0]
        self.running = True

