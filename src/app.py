import pygame
from pygame.locals import *
from drawables import Tile, Banner, Text
from gameplay import Sequencer
from static import Dict


class App:
    """This class represents the main application instance."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        pygame.display.set_caption('SimonSays')
        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 0
        self.victory = 20
        self.tiles = []
        self.objects = []
        self.dict = Dict()

        self.create_objects()
        self.seq = self.start_sequencer()

    def run(self):
        """Run the main event loop."""
        while self.running:
            for event in pygame.event.get():
                self.do(event)
            self.draw()
        pygame.quit()

    def do(self, event):
        """Handle application and object events."""
        if event.type == QUIT:
            self.running = False
        if event.type == self.dict.events['GAME_START']:
            self.seq.reset()
            self.state = 1
            pygame.time.set_timer(self.dict.events['PROGRAM_PHASE'], 1, 1)
        if event.type == self.dict.events['PROGRAM_PHASE']:
            self.state = 1
        if event.type == self.dict.events['PLAYER_PHASE']:
            self.state = 2
        if event.type == self.dict.events['GAME_OVER'] or event.type == self.dict.events['VICTORY']:
            self.state = 3
            pygame.time.set_timer(self.dict.events['IDLE_PHASE'], 2000, 1)
        if event.type == self.dict.events['IDLE_PHASE']:
            self.state = 0
        for obj in self.objects:
            obj.do(event, self.state)

    def draw(self):
        """Draw game screen and all objects."""
        self.screen.fill(pygame.Color('grey20'))
        for obj in self.objects:
            obj.draw()
        self.clock.tick(60)
        pygame.display.flip()

    def add_tile(self, x, y, colors, event_reset, event_verify, char):
        """Create a new tile instance and add it to object list."""
        tile = Tile(self, x, y, colors, event_reset, event_verify, char)
        self.tiles.append(tile)
        self.objects.append(tile)
        return tile

    def add_banner(self, x, y):
        """Create a banner button and add it to the object list."""
        banner = Banner(self.screen, x, y)
        self.objects.append(banner)
        return banner

    def add_text(self):
        """Creates a text object for the banner captions."""
        text = Text(self.screen)
        self.objects.append(text)
        return text

    def start_sequencer(self):
        """Create and initialize the sequence controller."""
        seq = Sequencer(self.tiles, 0)
        self.objects.append(seq)
        return seq

    def create_objects(self):
        """Create all game objects on app init."""
        self.add_tile(10, 110, self.dict.colors['red'],
                      self.dict.events['RED_RESET'], self.dict.events['RED_VERIFY'], 'R')
        self.add_tile(255, 110, self.dict.colors['green'],
                      self.dict.events['GREEN_RESET'], self.dict.events['GREEN_VERIFY'], 'G')
        self.add_tile(10, 355, self.dict.colors['blue'],
                      self.dict.events['BLUE_RESET'], self.dict.events['BLUE_VERIFY'], 'B')
        self.add_tile(255, 355, self.dict.colors['yellow'],
                      self.dict.events['YELLOW_RESET'], self.dict.events['YELLOW_VERIFY'], 'Y')
        self.add_banner(100, 25)
        self.add_text()


if __name__ == '__main__':
    App().run()
