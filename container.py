from dataclasses import dataclass, field
from typing import List, Dict, Type, Optional, Set, Any
from abc import ABC, abstractmethod
from component import Component, Card
import random
import json
from os.path import exists


@dataclass
class AbstractContainer(ABC):
    @abstractmethod
    def add_component(self, component: Component):
        """Add a component to the container."""
        pass  # pragma: no cover

    @abstractmethod
    def remove_component(self, component: Component):
        """Remove a component from the container."""
        pass  # pragma: no cover

    @abstractmethod
    def get_components(self) -> List[Component]:
        """Retrieve all components from the container."""
        pass  # pragma: no cover

    @abstractmethod
    def clear_components(self):
        """Clear all components from container."""
        pass  # pragma: no cover


@dataclass
class Container(AbstractContainer):
    allowable_component_types: Set[Type[Component]] = field(default_factory=set)
    components: List[Component] = field(default_factory=list)
    # Sets limit on how many components can be within the given container.
    max_capacity: Optional[int] = None

    def add_component(self, component: Component):
        if self.allowable_component_types and not isinstance(component, tuple(self.allowable_component_types)):
            raise ValueError(f"Component of type {type(component).__name__} is not allowed in this container.")

        if self.max_capacity is not None and len(self.components) >= self.max_capacity:
            raise ValueError("Maximum capacity reached, cannot add more components.")

        self.components.append(component)

    def remove_component(self, component: Component):
        if component in self.components:
            self.components.remove(component)

    def get_components(self) -> List[Component]:
        return self.components

    def clear_components(self):
        self.components.clear()


@dataclass
class ContainerContainer(AbstractContainer):
    """Container with the purpose of holding other containers.
    Can be used as a starting point for things like a tableau."""
    # Define which subtypes of containers are allowed
    allowable_container_types: Set[Type[Container]] = field(default_factory=set)
    containers: List[Container] = field(default_factory=list)
    max_capacity_per_type: Optional[Dict[Type[Container], Optional[int]]] = None

    def add_component(self, container: Container):
        if self.allowable_container_types and type(container) not in self.allowable_container_types:
            raise ValueError(f"Container type {type(container).__name__} not allowed.")

        if self.max_capacity_per_type is not None:
            container_type = type(container)
            max_capacity = self.max_capacity_per_type.get(container_type)

            if max_capacity is not None:
                current_count = sum(1 for c in self.containers if isinstance(c, container_type))
                if current_count >= max_capacity:
                    raise ValueError(f"Maximum capacity for {container_type.__name__} reached.")

        self.containers.append(container)

    def remove_component(self, container: Container):
        if container in self.containers:
            self.containers.remove(container)

    def get_components(self) -> List[Container]:
        return self.containers

    def clear_components(self):
        """Not sure how to implement this... since containers are not components and don't(?) have clear() function"""
        self.containers.clear()


@dataclass
class LoggingContainer(Container):
    def add_component(self, component: Component):
        print(f"Adding component: {component}")
        super().add_component(component)

    def remove_component(self, component: Component):
        print(f"Removing component: {component}")
        super().remove_component(component)

    def get_components(self) -> List[Component]:
        print("Retrieving components")
        return super().get_components()

    def clear_components(self):
        print("Clearing components")
        super().clear_components()


@dataclass
class CardContainer(Container):
    def add_component(self, component: Component):
        if not isinstance(component, Card):
            raise ValueError(f"Only Card objects can be added to Deck.")
        super().add_component(component)

    def contains_card(self, card: Card) -> bool:
        return card in self.components

    def find_card(self, card: Card) -> Optional[int]:
        try:
            return self.components.index(card)
        except ValueError:
            return None

    def card_count(self):
        return len(self.components)


@dataclass
class Deck(CardContainer):
    shuffle_on_init: bool = False

    def __post_init__(self):
        if self.shuffle_on_init:
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.components)

    def draw_card(self, number_of_cards: int = 1) -> List[Component]:
        if number_of_cards > len(self.components):
            raise ValueError("Not enough cards in the deck to draw the requested number of cards.")
        drawn_cards = self.components[:number_of_cards]
        self.components = self.components[number_of_cards:]
        return drawn_cards

    # def return_card(self, card: Card):
    #     if not isinstance(card, Card):
    #         raise ValueError(f"Only Card objects can be returned to the bottom of the deck.")
    #     self.components.append(card)
    #

    def peek(self, number_of_cards: int = 1) -> List[Component]:
        if number_of_cards <= len(self.components):
            return self.components[:number_of_cards]
        raise ValueError(f"Not enough cards in the deck to peek at the requested number of cards.")

    def __iter__(self):
        return iter(self.components)

    def deck_size(self) -> int:
        return len(self.components)

    def rebuild_and_shuffle(self, cards: List[Card]):
        self.components = cards
        self.shuffle()


@dataclass
class Hand(CardContainer):
    def organize_hand(self):
        pass  # pragma: no cover


@dataclass
class TokenContainer(Container):
    pass  # pragma: no cover


@dataclass
class Board(ContainerContainer):
    width: int = 1
    height: int = 1
    config_path: Optional[str] = None
    grid: List[List[Container]] = field(init=False)
    board_type: str = "default"

    def __post_init__(self):
        if self.board_type == "hex":
            self.init_hex_board()
        elif self.board_type in ["square", "default"]:
            self.init_square_board()
        # else:
        #     self.init_board_from_json()

    def init_hex_board(self):
        self.grid = []
        for y in range(self.height):
            row_offset = y // 2
            row = [Container() for _ in range(self.width - row_offset)]
            self.grid.append(row)

    def init_square_board(self):
        self.grid = [[Container() for _ in range(self.width)] for _ in range(self.height)]

    # def init_board_from_json(self):
    #     # Assuming the JSON defines a 2D array of cells with their configurations
    #     with open(self.config_path, 'r') as config_file:
    #         config = json.load(config_file)
    #         self.grid = []
    #         for row_config in config:
    #             row = []
    #             for cell_config in row_config:
    #                 container = Container()
    #                 container.allowable_component_types = cell_config.get("allowable_component_types", [])
    #                 row.append(container)
    #             self.grid.append(row)

    def get_cell(self, x: int, y: int):
        """Retrieve the container at the specified coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            raise ValueError("Cell coordinates are out of bounds.")

    def set_cell(self, x: int, y: int, content: Container):
        """Set the content of a cell at specified coordinates."""

        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = content
        else:
            raise ValueError("Cell coordinates are out of bounds")

    def get_rows(self, index: Optional[int] = None) -> List[List[Container]]:
        """Retrieve rows of the board, or a specific row if index is provided."""
        if index is not None:
            if 0 <= index < self.height:
                return [self.grid[index]]
            raise IndexError("Row index out of bounds.")
        return self.grid

    def get_columns(self, index: Optional[int] = None) -> List[List[Container]]:
        """Retrieve columns of the board, or a specific column if index is provided."""
        columns = [list(column) for column in zip(*self.grid)]
        if index is not None:
            if 0 <= index < len(columns):
                return [columns[index]] if index < len(columns) else []
            raise IndexError("Column index out of bounds.")
        return columns
