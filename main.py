import math
from random import choice
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Planet:
    def __init__(self, screen, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение планеты по горизонтали
        y - начальное положение планеты по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.r)


class Voyager:
    def __init__(self, screen):
        self.screen = screen
        self.color = GREY

    def event_1(self, event):
        pass

    def event_2(self, event):
        pass

    def event_3(self, event):
        pass

    def draw(self):
        # FIXIT don't know how to do it
        pygame.draw.circle(self.screen, self.color,(5, 5), 5)


class Star:
    def __init__(self, screen):
        self.screen = screen
        self.color = GREY

    def draw(self):
        pygame.draw.circle(self.screen, self.color,(50, 50), 50)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
voyager = Voyager(screen)
star = Star(screen)
planet = Planet(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    star.draw()
    voyager.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            voyager.event_1(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            voyager.event_2(event)
        elif event.type == pygame.MOUSEMOTION:
            voyager.event_3(event)

pygame.quit()
