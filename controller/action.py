from typing import Protocol
from dataclasses import dataclass
from typing import List
from component import Card

@dataclass
class Action(Protocol):
    def execute(self):
        ...  # pragma: no cover

    def undo(self):
        ...  # pragma: no cover

    def redo(self):
        ...  # pragma: no cover


@dataclass
class MoveCard(Action):
    card: Card
    source: List[Card]
    destination: List[Card]

    def execute(self):
        if self.card in self.source:
            self.source.remove(self.card)
            self.destination.append(self.card)

    def undo(self):
        if self.card in self.destination:
            self.destination.remove(self.card)
            self.source.append(self.card)

    def redo(self):
        if self.card in self.source:
            self.source.remove(self.card)
            self.destination.append(self.card)



@dataclass
class PlayCard(Action):
    card: Card
    source: List[Card]
    destination: List[Card]

    def execute(self):
        pass  # pragma: no cover

    def undo(self):
        pass  # pragma: no cover


@dataclass
class FlipCard(Action):
    card: Card

    def execute(self):
        self.card.front_side_up = not self.card.front_side_up

    def undo(self):
        self.card.front_side_up = not self.card.front_side_up

    def redo(self):
        self.card.front_side_up = not self.card.front_side_up

