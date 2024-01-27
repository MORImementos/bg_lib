from dataclasses import dataclass, field
from typing import Any, List, Dict, Type, Optional
import uuid
from abc import ABC, abstractmethod


@dataclass
class AbstractComponent(ABC):
    @abstractmethod
    def get_info(self):
        """Return information about the component."""
        pass # pragma: no cover


@dataclass
class Component(AbstractComponent):
    name: Optional[str] = None
    description: Optional[str] = None
    id: int = field(default_factory=lambda: uuid.uuid4())

    def get_info(self):
        return f"{self.name} ({type(self).__name__})"


@dataclass
class Card(Component):
    front_side_up: bool = True

    def flip(self):
        self.front_side_up = not self.front_side_up


@dataclass
class TwoSidedCard(Card):
    front_side_up: bool = True
    front: Card = None
    back: Card = None

    def flip(self):
        self.front_side_up = not self.front_side_up

    def get_active_side(self) -> Card:
        return self.front if self.front_side_up else self.back

    def get_info(self):
        return self.get_active_side().get_info()


@dataclass
class StandardPlayingCard(Card):
    suit: str = None
    value: str = None
    def get_info(self):
        return f"{self.value} of {self.suit}"



@dataclass
class Piece(Component):
    pass
