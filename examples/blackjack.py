from component import StandardPlayingCard
from container import Deck


def create_blackjack_deck():
    suits = ["H", "D", "C", "S"]
    names_values = [("Ace", "A"), ("2", "2"), ("3", "3"), ("4", "4"),
                    ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"),
                    ("9", "9"), ("10", "10"), ("Jack", "J"),
                    ("Queen", "Q"), ("King", "K")]

    deck = Deck()
    for suit in suits:
        for name, value in names_values:
            deck.add_component(StandardPlayingCard(name=name, suit=suit, value=value))
    deck.shuffle()
    return deck


def deal_initial_cards(deck, player_hand, dealer_hand):
    for _ in range(2):
        player_hand.add_component(deck.draw_card()[0])
        dealer_hand.add_component(deck.draw_card()[0])


def calculate_hand_value(hand):
    # this could be done by creating a blackjack action manager and calling this action (?)
    pass