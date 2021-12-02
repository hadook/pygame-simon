import unittest
import pygame
from gameplay import Sequencer
from drawables import Tile, Button
from app import App


class TestSequencer(unittest.TestCase):

    def setUp(self):
        self.seq1 = Sequencer([], 4)
        self.seq2 = Sequencer([], 0)

    def tearDown(self):
        pass

    def test_roll(self):
        self.assertEqual(self.seq1.length, 4)
        self.assertEqual(self.seq2.length, 0)

        for i in range(3):
            self.seq1.roll()
            self.seq2.roll()

        self.assertEqual(self.seq1.length, 7)
        self.assertEqual(self.seq2.length, 3)

    def test_reset(self):
        self.seq1.reset()
        self.seq2.reset()
        self.assertEqual(self.seq1.length, 0)
        self.assertEqual(self.seq2.length, 0)

    def test_matches(self):
        self.seq1.pattern = ['G', 'R', 'B', 'B', 'Y']
        self.seq2.pattern = ['Y', 'R']
        self.assertEqual(self.seq1.matches(3, 'B'), True)
        self.assertEqual(self.seq2.matches(0, 'R'), False)


class TestTile(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.app = App()
        self.tile1 = Tile(self.app, 20, 20, [pygame.Color('white'), pygame.Color('black')], 0, 1, 'R')
        self.tile2 = Tile(self.app, 150, 370, [pygame.Color('azure'), pygame.Color('blue')], 17, 4, 'B')

    def tearDown(self):
        pygame.quit()

    def test_animate(self):
        self.tile1.animate(1)
        self.assertEqual(self.tile1.color, self.tile1.colors[1])
        self.assertEqual(self.tile2.color, self.tile2.colors[0])
        self.assertEqual(self.tile1.highlight, True)
        self.assertEqual(self.tile2.highlight, False)

    def test_reset(self):
        self.tile1.animate(1)
        self.tile2.animate(1)
        self.tile1.reset()
        self.assertEqual(self.tile1.color, self.tile1.colors[0])
        self.assertEqual(self.tile2.color, self.tile2.colors[1])
        self.assertEqual(self.tile1.highlight, False)
        self.assertEqual(self.tile2.highlight, True)


class TestButton(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.app = App()
        self.bt_1 = Button(self.app.screen, 20, 20, 60, 30, 0, 10, pygame.Color('yellow'))
        self.bt_2 = Button(self.app.screen, 360, 360, 30, 60, 2, 0, pygame.Color('green'))

    def tearDown(self):
        pygame.quit()

    def test_do(self):
        self.bt_1.do(0, 1)
        self.bt_2.do(0, 2)
        self.assertEqual(self.bt_1.interactive, False)
        self.assertEqual(self.bt_2.interactive, True)

    def test_rect(self):
        rect1 = pygame.Rect(20, 20, 60, 30)
        rect2 = pygame.Rect(360, 360, 30, 60)
        self.assertEqual(self.bt_1.rect, rect1)
        self.assertEqual(self.bt_2.rect, rect2)


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = App()

    def tearDown(self):
        pass

    def test_start_sequencer(self):
        self.assertIsInstance(self.app.seq, Sequencer)


if __name__ == '__main__':
    unittest.main()
