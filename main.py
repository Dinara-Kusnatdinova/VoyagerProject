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
R_OWN_SUN = 695.5 * 10**6
R_CIRCULATION_EARTH = 149.6 * 10**11
R_OWN_EARTH = 6.371 * 10**6
K_OWN, K_CIRCULATION = 1 / 10**6, 1 / 10**11


class BaseBody:
    """ Класс BaseBody
    описывает тела, движущиеся в системе звезды по различным орбитам.
    """
    def __init__(self, screen, x=40, y=450, vx=0, vy=0, ax=0, ay=0,
                 r_own=R_OWN_EARTH, r_circulation=R_CIRCULATION_EARTH, color=BLUE,
                 k_own=K_OWN, k_circulation=K_CIRCULATION):
        """ Конструктор класса BaseBody
        Args:
        x - начальное положение тела по горизонтали
        y - начальное положение тела по вертикали
        vx - начальная скорость тела по горизонтали
        vy - начальная скорость тела по вертикали
        ax - начальное ускорение тела по горизонтали
        ay - начальное ускорение тела по вертикали
        r_own - радиус тела
        r_circulation - радиус обращения тела вокруг звезды
        color - цвет тела
        k_own - коэффициент увеличения размеров тела
        k_circulation - коэффициент увеличения расстояния от тела до звезды
        """
        self.screen = screen
        self.x, self.y = x, y
        self.r_own, self.k_own, self.k_circulation = r_own, k_own, k_circulation
        self.color, self.r_circulation = color, r_circulation
        self.vx, self.vy = vx, vy
        self.ax, self.ay = ax, ay

    def set_acceleration(self):
        """Задаёт ускорение тела.

        Метод рассчитывает ускорение тела с учётом сил, действующих на тело.
        """
        # NEED TO BE FIXED
        pass

    def change_speed(self):
        """Меняет скорость тела по прошествии единицы времени.

        Метод описывает изменение скорости тела за один кадр перерисовки. То есть, обновляет значения
        self.vx и self.vy с учетом ускорений self.ax и self.ay.
        """
        self.vx += self.ax
        self.vy -= self.ay

    def move(self):
        """Перемещает тело по прошествии единицы времени.

        Метод описывает перемещение тела за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """Рисует тело по прошествии единицы времени.

        Метод отрисовки тела. Обновляет положение тела на экране с учетом self.x и self.y.
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r_own * self.k_own)


class Planet(BaseBody):
    """ Класс Planet
    задаёт тела, движущиеся в системе звезды по орбитам, близким к круговым.
    """
    def set_acceleration(self):
        super().set_acceleration()
        # NEED TO BE FIXED


class Voyager(BaseBody):
    """ Класс Voyager
    задаёт тело, совершающее гравитационный манёвр.
    """
    def set_acceleration(self):
        super().set_acceleration()
        # NEED TO BE FIXED


class Star:
    def __init__(self, screen, x=60, y=500, r_own=R_OWN_SUN, color=YELLOW,
                 k_own=K_OWN, k_circulation=K_CIRCULATION):
        """ Конструктор класса Star
        Args:
        x - начальное положение тела по горизонтали
        y - начальное положение тела по вертикали
        r_own - радиус звезды
        color - цвет звезды
        k_own - коэффициент увеличения размеров тела
        k_circulation - коэффициент увеличения расстояния от тела до звезды
        """
        self.screen = screen
        self.x, self.y = x, y
        self.r_own, self.k_own, self.k_circulation = r_own, k_own, k_circulation
        self.color = color

    def draw(self):
        """ Метод отрисовки звезды. Обновляет положение тела на экране с учетом self.x и self.y.
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r_own * K_OWN)


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
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.MOUSEMOTION:
            pass


pygame.quit()
