from container import *
from component import *
import pytest

if __name__ == '__main__':
    # Container
    container = Container()
    # ContainerContainer
    container_container = ContainerContainer()
    # LoggingContainer
    logging_container = LoggingContainer()

    # Build a market
    top_row = ContainerContainer()

    card1 = StandardPlayingCard(name="Ace", suit="Hearts", value="A")
    card2 = StandardPlayingCard(name="King", suit="Spades", value="K")
    card3 = StandardPlayingCard(name="Queen", suit="Diamonds", value="Q")
    generic_container = Container()
    generic_container.add_component(card1)
    generic_container.add_component(card2)

    for component in generic_container.get_components():
        print(component.get_info())

    generic_container.remove_component(card1)

    card_container = Container(allowable_component_types={Card})

    # Adding cards
    card_container.add_component(card1)
    card_container.add_component(card2)

    generic_component = Component()
    # card_container.add_component(generic_component)  # This will raise ValueError

    # Displaying components
    for component in card_container.get_components():
        print(component.get_info())

    # Removing a component
    card_container.remove_component(card2)

    limited_container = Container(max_capacity=3)

    limited_container.add_component(card1)
    limited_container.add_component(card2)
    limited_container.add_component(generic_component)



