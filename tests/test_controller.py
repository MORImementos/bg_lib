from controller.action import MoveCard, PlayCard, FlipCard
from controller.controller import ActionController
from component import Card


# Test ActionController execute
def test_action_controller_execute():
    controller = ActionController()
    card = Card("Ace of Spades")
    flip_action = FlipCard(card)
    controller.execute(flip_action)
    assert not card.front_side_up
    assert flip_action in controller.undo_stack

# Test ActionController undo
def test_action_controller_undo():
    controller = ActionController()
    card = Card("Ace of Spades")
    flip_action = FlipCard(card)
    controller.execute(flip_action)
    controller.undo()
    assert card.front_side_up
    assert flip_action in controller.redo_stack

# Test ActionController redo
def test_action_controller_redo():
    controller = ActionController()
    card = Card("Ace of Spades")
    flip_action = FlipCard(card)
    controller.execute(flip_action)
    controller.undo()
    controller.redo()
    assert not card.front_side_up
    assert flip_action in controller.undo_stack

# Test ActionController with no actions to undo
def test_action_controller_no_undo():
    controller = ActionController()
    controller.undo()
    assert len(controller.undo_stack) == 0

# Test ActionController with no actions to redo
def test_action_controller_no_redo():
    controller = ActionController()
    controller.redo()
    assert len(controller.redo_stack) == 0