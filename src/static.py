import pygame
from pygame.locals import *


class Dict:
    """This class is a container for all static dictionaries."""

    def __init__(self):

        self.events = {
            'RED_RESET': USEREVENT + 1,
            'GREEN_RESET': USEREVENT + 2,
            'BLUE_RESET': USEREVENT + 3,
            'YELLOW_RESET': USEREVENT + 4,
            'SEQUENCER_ANIMATE': USEREVENT + 9,
            'RED_VERIFY': USEREVENT + 10,
            'GREEN_VERIFY': USEREVENT + 11,
            'BLUE_VERIFY': USEREVENT + 12,
            'YELLOW_VERIFY': USEREVENT + 13,
            'GAME_START': USEREVENT + 14,
            'IDLE_PHASE': USEREVENT + 15,
            'PROGRAM_PHASE': USEREVENT + 16,
            'PLAYER_PHASE': USEREVENT + 17,
            'GAME_OVER': USEREVENT + 18,
            'VICTORY': USEREVENT + 19
        }
        self.colors = {
            'grey': pygame.Color('grey20'),
            'white': pygame.Color('white'),
            'red': [pygame.Color('firebrick3'), pygame.Color('coral1')],
            'green': [pygame.Color('green4'), pygame.Color('green1')],
            'blue': [pygame.Color('dodgerblue4'), pygame.Color('deepskyblue')],
            'yellow': [pygame.Color('goldenrod3'), pygame.Color('yellow1')]
        }
