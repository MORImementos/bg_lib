from container import Deck, CardContainer, ContainerContainer
from game import Game
from dataclasses import dataclass
from player import Player
from controller.controller import ActionController
from controller.action import *

standard_works_limit = 5
extended_works_limit = 6


@dataclass
class MottainaiGame(Game):
    deck: Deck = None
    floor: CardContainer = None
    action_controller: ActionController = ActionController()

    def __post_init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.floor = CardContainer(name="floor")


@dataclass
class MottainaiPlayer(Player):
    tableau: ContainerContainer = None

    def __post_init__(self):
        self.tableau = initialize_tableau()


def initialize_tableau():
    tableau = ContainerContainer(allowable_container_types={CardContainer, ContainerContainer})

    tableau.add_component(CardContainer(name="task", max_capacity=1))
    tableau.add_component(CardContainer(name="craft_bench"))
    tableau.add_component(
        ContainerContainer(
            name="left_wing",
            allowable_container_types={CardContainer},
            containers=[
                CardContainer(name="works", max_capacity=standard_works_limit),
                CardContainer(name="materials")
            ]
        )
    )
    tableau.add_component(
        ContainerContainer(
            name="right_wing",
            allowable_container_types={CardContainer},
            containers=[
                CardContainer(name="works", max_capacity=standard_works_limit),
                CardContainer(name="materials")
            ]
        )
    )
    tableau_components = tableau.get_components()
    for comp in tableau_components:
        print(comp.name)
        if comp.name == "left_wing" or comp.name == "right_wing":
            for subcomp in comp.get_components():
                print('-', subcomp.name)

    return tableau


game = MottainaiGame(
    players=[
        MottainaiPlayer(name='Me'),
        MottainaiPlayer(name='You')
    ])
