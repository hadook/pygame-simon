import random
import pygame
from static import Dict


class Sequencer:
    """This class is responsible for generating random sequences and verifying player input."""

    labels = ['R', 'G', 'B', 'Y']
    timeout = 1000

    def __init__(self, tiles, length=0):
        self.length = 0
        self.index = 0
        self.animating = False
        self.pattern = []
        self.tiles = tiles
        self.dict = Dict()
        for i in range(length):
            self.roll()

    def do(self, event, state):
        # start sequence animation (states: 1)
        if state == 1 and event.type == self.dict.events['PROGRAM_PHASE'] and not self.animating:
            self.roll()
            self.start_animation()
        # animate next tile in sequence (states: 1)
        if state == 1 and event.type == self.dict.events['SEQUENCER_ANIMATE'] and self.animating:
            self.animate_tile()

    def draw(self):
        pass

    def roll(self):
        self.pattern.append(random.choice(self.labels))
        self.length += 1

    def reset(self):
        self.pattern.clear()
        self.length = 0

    def matches(self, pos, choice):
        if self.pattern[pos] == choice:
            return True
        else:
            return False

    def start_animation(self):
        if self.length >= 1:
            self.animating = True
            self.index = 0
            pygame.time.set_timer(self.dict.events['SEQUENCER_ANIMATE'], self.timeout, self.length)

    def animate_tile(self):
        tile = self.tiles[self.labels.index(self.pattern[self.index])]
        tile.animate(400)
        self.index += 1
        if self.index >= self.length:
            self.animating = False
            self.index = 0
            pygame.time.set_timer(self.dict.events['PLAYER_PHASE'], 1000, 1)
