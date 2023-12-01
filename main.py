import math
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

WIDTH, HEIGHT = 1400, 700
G = 6.6743 / 10**11
M_SUN = 3.955 * 10**30
R_SELF_SUN = 695.5 * 10**6
R_CIRCULATION_EARTH = 149.6 * 10**11
R_OWN_EARTH = 6.371 * 10**6


class Planet:
    def __init__(self, screen, x=40, y=450, vx=0, vy=0, ax=0, ay=0,
                 r_own=R_OWN_EARTH, r_circulation=R_CIRCULATION_EARTH, color=BLACK):
        """ Конструктор класса Planet
        Args:
        x - начальное положение планеты по горизонтали
        y - начальное положение планеты по вертикали
        vx - начальная скорость планеты по горизонтали
        vy - начальная скорость планеты по вертикали
        ax - начальное ускорение планеты по горизонтали
        ay - начальное ускорение планеты по вертикали
        r_own - радиус планеты
        r_circulation - радиус обращения планеты вокруг звезды
        color - цвет планеты

        """
        self.screen = screen
        self.x, self.y = x, y
        self.r_own = r_own
        self.color, self.r_circulation = color, r_circulation
        self.vx, self.vy = vx, vy
        self.ax, self.ay = ax, ay

    def set_acceleration(self):
        """Задаёт ускорение планеты.

        Метод рассчитывает ускорение планеты с учётом сил, действующих на тело.
        """
        # NEED TO BE FIXED
        pass

    def change_speed(self):
        """Меняет скорость планеты по прошествии единицы времени.

        Метод описывает изменение скорости планеты за один кадр перерисовки. То есть, обновляет значения
        self.vx и self.vy с учетом ускорений self.ax и self.ay.
        """
        self.vx += self.ax
        self.vy -= self.ay

    def move(self):
        """Перемещает планету по прошествии единицы времени.

        Метод описывает перемещение планеты за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.r_own)


class Voyager:
    def __init__(self, screen, x=40, y=450, color=BLACK):
        self.screen = screen
        self.color = color

    def event1(self, event):
        pass

    def event2(self, event):
        pass

    def event3(self, event):
        pass

    def draw(self):
        pygame.draw.circle(self.screen, self.color,(100, 100), 200)


class Star:
    def __init__(self, screen):
        self.screen = screen
        self.color = GREEN

    def draw(self):
        pygame.draw.circle(self.screen, self.color,(10, 10), 20)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
star = Star(screen)
planet = Planet(screen)
voyager = Voyager(screen)

finished = False

while not finished:
    screen.fill(WHITE)
    star.draw()
    planet.draw()
    voyager.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            voyager.event1(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            voyager.event2(event)
        elif event.type == pygame.MOUSEMOTION:
            voyager.event3(event)


pygame.quit()
