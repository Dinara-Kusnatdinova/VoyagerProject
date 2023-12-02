import pygame
from ctypes import windll
# import math


FPS = 30

# Цвета игры
BLUE = (55, 105, 235)
YELLOW = (255, 205, 0)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
WHITE = (250, 255, 255)
SPACE = (25, 25, 62)

# Размер окна
WIDTH, HEIGHT = windll.user32.GetSystemMetrics(0) - 10, windll.user32.GetSystemMetrics(1) - 80

# Физические константы
G = 6.6743 / 10**11
M_SUN = 3.955 * 10**30
R_OWN_SUN = 696.34 * 10**6
M_EARTH = 5.9742 * 10**24
R_CIRCULATION_EARTH = 1.495978707 * 10**11
R_OWN_EARTH = 6.371 * 10**6

# Масштабные коэффициенты (могут меняться для каждого тела):
# увеличение линейного размера тел, увеличение расстояния между телами
K_OWN, K_CIRCULATION = 1 / 10**6 / 1.25, 1 / 10**9 / 3.5


class BaseBody:
    """ Класс BaseBody
    описывает тела, движущиеся в системе звезды по различным орбитам.
    """
    def __init__(self, screen, x=40, y=HEIGHT/2 * 10**9 * 3.5, vx=0, vy=0, ax=0, ay=0, m=M_EARTH,
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
        m - масса тела
        r_own - радиус тела
        r_circulation - радиус орбиты
        color - цвет тела
        k_own - коэффициент увеличения линейных размеров тела
        k_circulation - коэффициент увеличения расстояния от тела до звезды
        """
        self.screen = screen
        self.r_own, self.k_own, self.k_circulation = r_own, k_own, k_circulation
        self.color, self.r_circulation = color, r_circulation
        self.vx, self.vy = vx, vy
        self.ax, self.ay, self.m = ax, ay, m

        self.x, self.y = self.r_circulation, y
        # на данном этапе координаты задаются так, потом изменим

    def set_acceleration(self):
        """Задаёт ускорение тела.

        Метод рассчитывает ускорение тела с учётом сил, действующих на тело.
        """
        # NEED TO BE FIXED
        # Скорее всего потребует отдельной реализации в каждом наследуемом классе.
        # Тем не менее основные вычисления могут быть сделаны здесь:
        # подсчёт сил без проекций на оси x, y. Если получится спроецировать,
        # то данный метод будет наследоваться в зависимых классах, без дополнительной реализации в них.
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
        pygame.draw.circle(self.screen, center=(self.x * self.k_circulation, self.y * self.k_circulation),
                           radius=self.r_own * self.k_own, color=self.color)


class Planet(BaseBody):
    """ Класс Planet
    задаёт тела, движущиеся в системе звезды по орбитам, близким к круговым.
    """
    def set_acceleration(self):
        super().set_acceleration()
        # NEED TO BE FIXED


class Voyager(BaseBody):
    """ Класс Voyager
    описывает тело, совершающее гравитационный манёвр.
    """
    def set_acceleration(self):
        super().set_acceleration()
        # NEED TO BE FIXED


class Star:
    def __init__(self, screen, x=0, y=HEIGHT/2, r_own=R_OWN_SUN, color=YELLOW,
                 m=M_SUN, k_own=K_OWN, k_circulation=K_CIRCULATION):
        """ Конструктор класса Star
        Args:
        x - начальное положение тела по горизонтали
        y - начальное положение тела по вертикали
        m - масса звезды
        r_own - радиус звезды
        color - цвет звезды
        k_own - коэффициент увеличения размеров тела
        k_circulation - коэффициент увеличения расстояния от тела до звезды
        """
        self.screen = screen
        self.x, self.y, self.m = x, y, m
        self.r_own, self.k_own, self.k_circulation = r_own, k_own, k_circulation
        self.color = color

    def draw(self):
        """ Метод отрисовки звезды. Обновляет положение тела на экране с учетом self.x и self.y.
        """
        pygame.draw.circle(self.screen, center=(self.x, self.y), radius=self.r_own * self.k_own,
                           color=self.color)


# Инициализация окна, синхронизация со временем
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Инициализация Солнца
Sun = Star(screen, k_own=K_OWN / 5)
# Инициализация планет солнечной системы
Mercury = Planet(screen, m=3.3 * 10**23, r_own=2.4397 * 10**6, r_circulation=5.791 * 10**10, k_own=K_OWN * 1.25)
Venus = Planet(screen, m=4.87 * 10**24, r_own=6.0518 * 10**6, r_circulation=1.082 * 10**11)
Earth = Planet(screen)
Mars = Planet(screen, m=6.39 * 10**23, r_own=3.3895 * 10**6, r_circulation=2.279 * 10**11, k_own=K_OWN * 1.25)
Jupiter = Planet(screen, m=1.898 * 10**27, r_own=69.911 * 10**6, r_circulation=7.785 * 10**11, k_own=K_OWN/4)
Saturn = Planet(screen, m=5.683 * 10**26, r_own=58.232 * 10**6, r_circulation=1.434 * 10**12, k_own=K_OWN/3.75)
Uranus = Planet(screen, m=8.681 * 10**25, r_own=25.362 * 10**6, r_circulation=2.871 * 10**12, k_own=K_OWN/3.25)
Neptune = Planet(screen, m=1.024 * 10**26, r_own=24.622 * 10**6, r_circulation=4.495 * 10**12, k_own=K_OWN/3.25)
# Инициализация объекта, совершающего гравитационный манёвр
voyager = Voyager(screen, color=GREEN, y=(HEIGHT/2 + 5) * 10**9 * 3.5, r_own=100, k_own=K_OWN * 10**4 * 5)

# Цикл игры, прекращается при нажатии кнопки выхода
finished = False
while not finished:
    # Фон окна
    screen.fill(SPACE)
    # Отрисовка объектов
    Sun.draw()
    (Mercury.draw(), Venus.draw(), Earth.draw(), Mars.draw(),
     Jupiter.draw(), Saturn.draw(), Uranus.draw(), Neptune.draw())
    voyager.draw()
    pygame.display.update()

    # Синхронизация со временем
    clock.tick(FPS)
    # Обработка событий игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
