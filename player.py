from dataclasses import dataclass, field
from component import Component
from container import Hand


@dataclass
class Player(Component):
    name: str
    hand: Hand = field(default_factory=Hand)

    def perform_action(self):
        pass # pragma: no cover

