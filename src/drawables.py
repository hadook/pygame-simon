import pygame
from static import Dict


class Drawable:
    """Class for any game object that can be drawn to a surface."""

    def __init__(self, surf, x, y, width, height, border_width, border_radius, color):
        self.surf = surf
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_width = border_width
        self.border_radius = border_radius
        self.color = color

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def do(self, event, state):
        pass

    def draw(self):
        pygame.draw.rect(self.surf, self.color, self.rect, self.border_width, self.border_radius)


class Button(Drawable):
    """Class for any game object that can be interacted with through mouse events."""

    def __init__(self, surf, x, y, width, height, border_width, border_radius, color):
        super().__init__(surf, x, y, width, height, border_width, border_radius, color)
        self.highlight = False
        self.interactive = False

    @property
    def hovered(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)

    def do(self, event, state):
        if state == 0 or state == 2:
            self.interactive = True
        else:
            self.interactive = False

    def draw(self):
        super().draw()
        if (self.interactive and self.hovered) or self.highlight:
            pygame.draw.rect(self.surf, pygame.Color('white'), self.rect, 2, self.border_radius)


class Tile(Button):
    """Class defining the basic, interactive game tile (one of four colored square buttons)."""

    width = 235
    timeout = 150

    def __init__(self, _parent, x, y, colors, event_reset, event_verify, char):
        self.parent = _parent
        self.colors = colors
        self.event_reset = event_reset
        self.event_verify = event_verify
        self.char = char
        self.dict = Dict()
        super().__init__(self.parent.screen, x, y, self.width, self.width, 0, 15, colors[0])

    def do(self, event, state):
        super().do(event, state)
        # click event (states: 2)
        if state == 2 and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.animate(self.timeout)
                self.verify()
        # reset state event (states: 0, 1, 2)
        if event.type == self.event_reset:
            self.reset()

    def animate(self, timeout):
        self.color = self.colors[1]
        self.highlight = True
        pygame.time.set_timer(self.event_reset, timeout, 1)

    def reset(self):
        self.color = self.colors[0]
        self.highlight = False

    def verify(self):
        if self.parent.seq.matches(self.parent.seq.index, self.char):
            self.parent.seq.index += 1
            if self.parent.seq.index >= self.parent.seq.length:
                if self.parent.seq.length >= self.parent.victory:
                    pygame.time.set_timer(self.dict.events['VICTORY'], 1, 1)
                else:
                    pygame.time.set_timer(self.dict.events['PROGRAM_PHASE'], 1, 1)
        else:
            pygame.time.set_timer(self.dict.events['GAME_OVER'], 1, 1)


class Banner(Button):
    """Class defining the top-centered banner button with game notifications."""

    width = 300
    height = 60

    def __init__(self, surf, x, y):
        super().__init__(surf, x, y, self.width, self.height, 0, 5, pygame.Color('cadetblue3'))
        self.dict = Dict()

    def do(self, event, state):
        super().do(event, state)
        # click event (states: 0)
        if state == 0 and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.time.set_timer(self.dict.events['GAME_START'], 1, 1)

    def draw(self):
        super().draw()
        if not self.hovered:
            pygame.draw.rect(self.surf, pygame.Color('burlywood2'), self.rect, 2, self.border_radius)


class Text:
    """Class to display text frames."""

    def __init__(self, surf):
        self.surf = surf
        self.dict = Dict()
        self.caption = None
        self.font = pygame.font.SysFont('Calibri', 48, True)
        self.img = None
        self.rect = None
        self.render('START')

    def render(self, caption):
        self.caption = caption
        self.img = self.font.render(self.caption, True, pygame.Color('black'))
        self.rect = self.img.get_rect()
        self.rect.center = (250, 58)

    def do(self, event, state):
        # change label to indicate idle phase (state: 0)
        if state == 0 and event.type == self.dict.events['IDLE_PHASE']:
            self.render('START')
        # change label to indicate program phase (state: 1)
        if state == 1 and event.type == self.dict.events['PROGRAM_PHASE']:
            self.render('MEMORIZE')
        # change label to indicate player phase (state: 2)
        if state == 2 and event.type == self.dict.events['PLAYER_PHASE']:
            self.render('REPEAT')
        # change label to indicate game over (state: 3)
        if state == 3 and event.type == self.dict.events['GAME_OVER']:
            self.render('GAME OVER')
        # change label to indicate victory (state: 3)
        if state == 3 and event.type == self.dict.events['VICTORY']:
            self.render('VICTORY')

    def draw(self):
        self.surf.blit(self.img, self.rect)
