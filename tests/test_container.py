import pytest
from container import Deck, Container, Board, ContainerContainer, LoggingContainer, CardContainer
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

def test_container_container_add_disallowed_type():
    outer_container = ContainerContainer(allowable_container_types={CardContainer})
    disallowed_container = Container(allowable_component_types={Card})

    with pytest.raises(ValueError) as excinfo:
        outer_container.add_component(disallowed_container)
    assert "not allowed" in str(excinfo.value)

def test_container_container_max_capacity():
    outer_container = ContainerContainer(
        max_capacity_per_type={CardContainer: 1}
    )
    allowed_container = CardContainer()

    outer_container.add_component(allowed_container)
    assert allowed_container in outer_container.get_components()

    another_container = CardContainer()
    with pytest.raises(ValueError) as excinfo:
        outer_container.add_component(another_container)
    assert "Maximum capacity" in str(excinfo.value)


def test_logging_container():
    log_cont = LoggingContainer()
    card = Card()
    log_cont.add_component(card)
    assert card in log_cont.get_components()

    log_cont.remove_component(card)
    assert card not in log_cont.get_components()

    log_cont.clear_components()
    assert not log_cont.get_components()


def test_card_container():
    cc = CardContainer()
    card = Card()
    cc.add_component(card)
    assert card in cc.get_components()
    comp = Component()
    with pytest.raises(ValueError) as excinfo:
        cc.add_component(comp)
    assert "Only Card" in str(excinfo.value)


def test_card_container_add_component():
    container = CardContainer()
    card = Card('Ace of Spades')
    container.add_component(card)
    assert card in container.components


def test_card_container_add_invalid_component():
    container = CardContainer()
    non_card_component = Component()  # Assuming Component is a different class
    with pytest.raises(ValueError):
        container.add_component(non_card_component)


def test_card_container_contains_card():
    container = CardContainer()
    card = Card('Ace of Spades')
    container.add_component(card)
    assert container.contains_card(card)


def test_card_container_find_card():
    container = CardContainer()
    card = Card('Ace of Spades')
    container.add_component(card)
    assert container.find_card(card) == 0


def test_card_container_card_count():
    container = CardContainer()
    card = Card('Ace of Spades')
    container.add_component(card)
    assert container.card_count() == 1


def test_deck_shuffle_on_init():
    initial_cards = [Card('Ace of Spades'), Card('King of Hearts')]
    deck = Deck()
    deck.rebuild_and_shuffle(initial_cards)
    initial_order = deck.components.copy()
    deck.shuffle()
    assert deck.components != initial_order


def test_deck_draw_card():
    deck = Deck(shuffle_on_init=False)
    deck.rebuild_and_shuffle([Card('Ace of Spades'), Card('King of Hearts')])
    drawn_cards = deck.draw_card(1)
    assert isinstance(drawn_cards[0], Card)


def test_deck_draw_card_invalid():
    deck = Deck()
    with pytest.raises(ValueError):
        deck.draw_card(5)  # Assuming the deck is empty or has fewer than 5 cards


def test_deck_peek():
    deck = Deck(shuffle_on_init=False)
    deck.rebuild_and_shuffle([Card('Ace of Spades'), Card('King of Hearts')])
    peeked_cards = deck.peek(1)
    assert isinstance(peeked_cards[0], Card)


def test_deck_peek_invalid():
    deck = Deck()
    with pytest.raises(ValueError):
        deck.peek(3)


def test_deck_iter():
    initial_cards = [Card(f'Card {i}') for i in range(10)]  # Create a list of 10 cards
    deck = Deck(initial_cards)
    deck.rebuild_and_shuffle(initial_cards)
    initial_order = deck.components.copy()
    deck.shuffle()
    assert deck.components != initial_order


def test_deck_rebuild_and_shuffle():
    deck = Deck()
    new_cards = [Card('Ace of Spades'), Card('King of Hearts')]
    deck.rebuild_and_shuffle(new_cards)
    assert deck.components == new_cards


# def test_board_initialization_from_json():
#     board = Board(width=3, height=3, config_path="config.json", board_type="custom")
#     board.init_board_from_json()
#     # Assuming specific content in your JSON file
#     assert len(board.grid) == 3