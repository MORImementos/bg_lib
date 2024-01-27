from dataclasses import dataclass
from component import Component
from typing import List
from player import Player


@dataclass
class Game(Component):
    players: List[Player] = None


@dataclass
class CardGame(Game):
    pass
