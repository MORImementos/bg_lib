from controller.action import MoveCard, PlayCard, FlipCard
from controller.controller import ActionController
from component import Card

# Test FlipCard action
def test_flip_card():
    card = Card("Ace of Spades")
    flip_action = FlipCard(card)
    flip_action.execute()
    assert not card.front_side_up
    flip_action.undo()
    assert card.front_side_up
    flip_action.redo()
    assert not card.front_side_up

# Test MoveCard action
def test_move_card():
    card = Card("Ace of Spades")
    card2 = Card("Ace of Hearts")

    source = [card, card2]
    destination = []
    move_action = MoveCard(card, source, destination)
    move_action.execute()
    assert card not in source
    assert card in destination
    move_action.undo()
    assert card in source and card not in destination
    move_action.redo()
    assert card in destination and card not in source
