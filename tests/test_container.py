import pytest
from container import Container, Board, ContainerContainer, LoggingContainer
from component import Card, StandardPlayingCard, Component
# from player import Player
# from game import Game


def test_generic_container():
    cont = Container()
    card1 = StandardPlayingCard(name="Ace", suit="Hearts", value="A")
    card2 = StandardPlayingCard(name="King", suit="Spades", value="K")

    cont.add_component(card1)
    cont.add_component(card2)

    assert card1 in cont.get_components()
    assert card2 in cont.get_components()

    cont.remove_component(card1)
    assert card1 not in cont.get_components()


def test_container_with_type_restriction():
    cont = Container(allowable_component_types={Card})
    card1 = StandardPlayingCard(name="Ace", suit="Hearts", value="A")
    card2 = StandardPlayingCard(name="King", suit="Spades", value="K")

    cont.add_component(card1)
    cont.add_component(card2)

    assert card1 in cont.get_components()
    assert card2 in cont.get_components()

    with pytest.raises(ValueError):
        non_card_component = Component(name="NonCard")
        cont.add_component(non_card_component)


def test_container_with_limited_capacity():
    cont = Container(max_capacity=2)
    card1 = StandardPlayingCard(name="Ace", suit="Hearts", value="A")
    card2 = Card()
    card3 = StandardPlayingCard(name="King", suit="Spades", value="K")
    card4 = StandardPlayingCard(name="Queen", suit="Diamonds", value="Q")

    cont.add_component(card1)
    cont.add_component(card2)

    assert len(cont.get_components()) == 2

    with pytest.raises(ValueError):
        cont.add_component(card3)


def test_board_initialization_square():
    board = Board(width=3, height=3, board_type="square")
    assert len(board.grid) == 3
    assert all(len(row) == 3 for row in board.grid)


def test_board_initialization_hex():
    board = Board(width=3, height=3, board_type="hex")
    board.init_hex_board()
    assert len(board.grid) == 3
    assert all(len(row) <= 3 for row in board.grid)


def test_board_get_set_cell():
    board = Board(width=3, height=3, board_type="square")
    container = Container()
    board.set_cell(0, 0, container)
    assert board.get_cell(0, 0) == container

    with pytest.raises(ValueError):
        board.get_cell(-1, -1)  # Out of bounds
    with pytest.raises(ValueError):
        board.set_cell(-1, -1, container)  # Out of bounds


def test_board_get_rows_columns():
    board = Board(width=3, height=3, board_type="square")
    assert len(board.get_rows()) == 3
    assert len(board.get_columns()) == 3
    assert len(board.get_rows(index=0)) == 1
    assert len(board.get_columns(index=0)) == 1

    with pytest.raises(IndexError):
        board.get_rows(index=10)
    with pytest.raises(IndexError):
        board.get_columns(index=10)


def test_container_container():
    outer_container = ContainerContainer()
    inner_container = Container()
    outer_container.add_component(inner_container)
    assert inner_container in outer_container.get_components()

    outer_container.remove_component(inner_container)
    assert inner_container not in outer_container.get_components()

    outer_container.add_component(inner_container)
    outer_container.clear_components()
    assert not outer_container.get_components()


def test_logging_container():
    log_cont = LoggingContainer()
    card = Card()
    log_cont.add_component(card)
    assert card in log_cont.get_components()

    log_cont.remove_component(card)
    assert card not in log_cont.get_components()

    log_cont.clear_components()
    assert not log_cont.get_components()


# def test_board_initialization_from_json():
#     board = Board(width=3, height=3, config_path="config.json", board_type="custom")
#     board.init_board_from_json()
#     # Assuming specific content in your JSON file
#     assert len(board.grid) == 3