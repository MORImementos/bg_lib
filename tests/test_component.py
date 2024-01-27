import pytest
from container import *
from component import *

def test_generic_component():
    comp = Component()
    info = comp.get_info()
    assert type(info) == str


def test_card_flip():
    card = Card()
    fl = card.front_side_up
    assert fl == True
    card.flip()
    fl = card.front_side_up
    assert fl == False


def test_two_sided_card_flip_and_info():
    card = TwoSidedCard(front=Card(description="Front"), back=Card(description="Back"))
    assert card.front_side_up == True
    assert card.get_active_side() == card.front
    card.flip()
    assert card.front_side_up == False
    assert card.get_active_side() == card.back
    assert card.get_info() == card.back.get_info()


def test_standard_playing_card_get_info():
    card = StandardPlayingCard(suit="Hearts", value="4")
    assert card.get_info() == "4 of Hearts"