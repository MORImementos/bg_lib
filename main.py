from examples.blackjack import deal_initial_cards, create_blackjack_deck
from container import Hand
from player import Player
from game import CardGame

def main() -> None:
    # blackjack test to determine current difficulty of using to implement a game
    deck = create_blackjack_deck()
    player_hand = Hand()
    dealer_hand = Hand()
    players = [Player("Player"), Player("Dealer")]
    game = CardGame(players, deck)

    deal_initial_cards(deck, player_hand, dealer_hand)

    print(player_hand.get_components())
    print(dealer_hand.get_components())





if __name__ == '__main__':
    main()