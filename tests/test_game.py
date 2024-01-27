import pytest
from game import Game
from player import Player


def test_game_and_player_list():
    game = Game(players=[Player("Jim"), Player("John")])
    assert game.players[0].name == "Jim"
