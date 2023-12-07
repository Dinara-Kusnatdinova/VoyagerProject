import pygame
from ctypes import windll
import math


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

# Физические константы в СИ
G = 6.6743 / 10**11
M_SUN = 1.9885 * 10**30
R_OWN_SUN = 100.34 * 10**6
M_EARTH = 5.9742 * 10**24
R_CIRCULATION_EARTH = 1.49598 * 10**11
R_OWN_EARTH = 6.371 * 10**6
V_ORBITAL_EARTH = 4 * 10**4
V_OWN_ROTATION_EARTH = 465.1013  # на экваторе
# Масштабные коэффициенты (могут меняться для каждого тела); коэффициент увелечения скорости:
# увеличение линейного размера тел, увеличение расстояния между телами; коэффициент увелечения скорости
K_OWN, K_CIRCULATION = 1 / 10**6 / 2, 1 / 10**10/0.3
# Радиус удаления от Солнца. Нужен, чтобы отдалить планеты от звезды, противодействует слипанию
R_START = 0
# Время в с, за которое сменяется кадр
TIME = 288 * 10**3

# Время одной итерации в с
dt = 500


class BaseBody:
    """ Класс BaseBody
    описывает тела, движущиеся в системе звезды по различным орбитам.
    """
    def __init__(self, screen, angle=0.0, m=M_EARTH,
                 r_own=R_OWN_EARTH, r_circulation=R_CIRCULATION_EARTH, color=BLUE,
                 k_own=K_OWN, k_circulation=K_CIRCULATION, time=TIME, v=0):
        """ Конструктор класса BaseBody
        Args:
        v - полная орбитальная скорость объекта
        angle - начальный угол (рисунок)
        m - масса тела
        r_own - радиус тела
        r_circulation - радиус орбиты
        color - цвет тела
        k_own - коэффициент увеличения линейных размеров тела
        k_circulation - коэффициент увеличения расстояния от тела до звезды
        k_speed - коэффициент увеличения скорости тела
        x - начальное положение тела по горизонтали
        y - начальное положение тела по вертикали
        vx - начальная скорость тела по горизонтали
        vy - начальная скорость тела по вертикали
        ax - начальное ускорение тела по горизонтали
        ay - начальное ускорение тела по вертикали
        """
        self.screen = screen
        self.r_own, self.k_own, self.k_circulation, self.time = r_own, k_own, k_circulation, time
        self.color, self.r_circulation = color, r_circulation
        if v == 0:
            v = math.sqrt(G * M_SUN / r_circulation)
        self.vx, self.vy = -1 * v * math.sin(angle), v * math.cos(angle)
        self.m = m
        self.x, self.y = Sun.x + self.r_circulation * math.cos(angle), Sun.y + self.r_circulation * math.sin(angle)
        self.ax, self.ay = 0, 0
        self.acceleration()
        self.tick = 0  # переменная для подсчёта количество выполненных циклов и перевод их в дни и годы
        self.object_track_X = []
        self.object_track_Y = []

    def acceleration(self):
        a_sun_perpendicular = G * M_SUN / ((self.x - Sun.x) ** 2 + (self.y - Sun.y) ** 2)
        self.angle = math.atan2(self.y - Sun.y, self.x - Sun.x)
        self.ax = -1 * a_sun_perpendicular * math.cos(self.angle)
        self.ay = -1 * a_sun_perpendicular * math.sin(self.angle)

    def move(self):
        """Перемещает тело по прошествии единицы времени.

        Метод описывает перемещение тела за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        for t in range(0, TIME, dt):
            self.acceleration()
            self.vx -= self.ax * dt
            self.vy -= self.ay * dt
            self.x -= self.vx * dt
            self.y -= self.vy * dt

    def draw(self):
        """Рисует тело по прошествии единицы времени.


        Метод отрисовки тела. Обновляет положение тела на экране с учетом self.x и self.y.
        """
        pygame.draw.circle(self.screen, center=(self.x * self.k_circulation,
                                                self.y * self.k_circulation),
                           radius=self.r_own * self.k_own, color=self.color)

        # Массивы хранящие информацию о треке

    def object_track_write(self):
        self.object_track_X.append(self.x)
        self.object_track_Y.append(self.y)

    def object_track_draw(self):
        for i in range(len(self.object_track_X) - 1):
            if len(self.object_track_X) > 1:
                pygame.draw.line(screen, BLUE,
                                 [self.object_track_X[i] * K_CIRCULATION,
                                  self.object_track_Y[i] * K_CIRCULATION],
                                 [self.object_track_X[i + 1] * K_CIRCULATION,
                                  self.object_track_Y[i + 1] * K_CIRCULATION], 1)


class Planet(BaseBody):
    """ Класс Planet
    задаёт тела, движущиеся в системе звезды по орбитам, близким к круговым.
    """
    pass


class Voyager(BaseBody):
    """ Класс Voyager
    описывает тело, совершающее гравитационный манёвр.
    """

    def acceleration(self):
        a_sun_perpendicular = G * M_SUN / ((self.x - Sun.x) ** 2 + (self.y - Sun.y) ** 2)
        self.angle = math.atan2(self.y - Sun.y, self.x - Sun.x)
        self.ax = -1 * a_sun_perpendicular * math.cos(self.angle)
        self.ay = -1 * a_sun_perpendicular * math.sin(self.angle)
        for plaret in Planets:
            self.ax += (G * plaret.m / (math.sqrt((plaret.x - self.x) ** 2 + (plaret.y - self.y) ** 2)) ** 3 *
                        (plaret.x - self.x))
            self.ay += (G * plaret.m / (math.sqrt((plaret.x - self.x) ** 2 + (plaret.y - self.y) ** 2)) ** 3 *
                        (plaret.y - self.y))

    def draw_information(self):
        self.tick += 1
        year = int((self.tick * TIME) // (365.25 * 86400))
        day = ((self.tick * TIME) // 86400) % 365
        f1 = pygame.font.Font(None, 36)
        if year > 1:
            if year > 4:
                text1 = f1.render(f'прошло {str(year)} лет {str(day)} дней',
                                  1, (255, 255, 255))
            else:
                text1 = f1.render(f'прошло {str(year)} года {str(day)} дней',
                                  1, (255, 255, 255))
        elif year == 1:
            text1 = f1.render(f'прошёл {str(year)} год {str(day)} дней',
                              1, (255, 255, 255))
        else:
            text1 = f1.render(f'прошло {str(day)} дней',
                              1, (255, 255, 255))
        text2 = f1.render('скорость Вояджера ' + str(round(math.sqrt(self.vx**2 + self.vy**2) / 1000, 2)) + ' км/с',
                          1, (255, 255, 255))
        text3 = f1.render('расстояние от Вояджера до Солнца ' +
                          str(round(math.sqrt((self.x - Sun.x) ** 2 +
                                              (self.y - Sun.y) ** 2) / R_CIRCULATION_EARTH, 2)) + ' а.е.',
                          1, (255, 255, 255))
        screen.blit(text1, (15, 15))
        screen.blit(text2, (15, 50))
        screen.blit(text3, (15, 85))


class Star:
    # Нужны для отрисовки трека при движении камеры

    def __init__(self, screen, x=WIDTH/2 / K_CIRCULATION, y=HEIGHT/2 / K_CIRCULATION, r_own=R_OWN_SUN,
                 color=YELLOW, m=M_SUN, k_own=K_OWN, k_circulation=K_CIRCULATION):
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
        self.object_track_X = []
        self.object_track_Y = []

    def draw(self):
        """ Метод отрисовки звезды. Обновляет положение тела на экране с учетом self.x и self.y.
        """
        pygame.draw.circle(self.screen, center=(self.x * K_CIRCULATION, self.y * K_CIRCULATION),
                           radius=self.r_own * self.k_own, color=self.color)


class Events:
    def move_object_on_the_camera(self, obj):
        # Здесь заложено перемещение заданной сущности
        if keys[pygame.K_w]:
            obj.y += 10/K_CIRCULATION
            for i in range(len(obj.object_track_X)):
                obj.object_track_Y[i] += 10 / K_CIRCULATION

        if keys[pygame.K_s]:
            obj.y -= 10/K_CIRCULATION
            for i in range(len(obj.object_track_X)):
                obj.object_track_Y[i] -= 10 / K_CIRCULATION

        if keys[pygame.K_d]:
            obj.x -= 10/K_CIRCULATION
            for i in range(len(obj.object_track_X)):
                obj.object_track_X[i] -= 10 / K_CIRCULATION

        if keys[pygame.K_a]:
            obj.x += 10/K_CIRCULATION
            for i in range(len(obj.object_track_X)):
                obj.object_track_X[i] += 10 / K_CIRCULATION

    def change_size(self):
        global K_CIRCULATION, K_OWN
        if keys[pygame.K_MINUS]:
            K_OWN /= 1.25
            K_CIRCULATION /= 1.25
            for object in Track_list:
                object.k_own /= 1.25
                object.k_circulation /= 1.25
            Sun.k_own /= 1.25
            Sun.k_circulation /= 1.25

        elif keys[pygame.K_EQUALS]:
            K_OWN *= 1.25
            K_CIRCULATION *= 1.25
            for object in Track_list:
                object.k_own *= 1.25
                object.k_circulation *= 1.25
            Sun.k_own *= 1.25
            Sun.k_circulation *= 1.25


# Инициализация окна, синхронизация со временем
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Инициализация Солнца
Event = Events()
Sun = Star(screen, k_own=K_OWN / 15)
# Инициализация планет солнечной системы
Mercury = Planet(screen, m=3.3 * 10**23, r_own=2.4397 * 10**6, r_circulation=0.387*R_CIRCULATION_EARTH,
                 k_own=K_OWN * 1.25, time=TIME, angle=1.4)
Venus = Planet(screen, m=4.87 * 10**24, r_own=6.0518 * 10**6, r_circulation=0.723*R_CIRCULATION_EARTH,
               time=TIME, angle=1.2)
Earth = Planet(screen)
Mars = Planet(screen, m=6.39 * 10**23, r_own=3.3895 * 10**6, r_circulation=1.523*R_CIRCULATION_EARTH,
              k_own=K_OWN * 1.25, time=TIME, angle=1.0)
Jupiter = Planet(screen, m=1.898 * 10**27, r_own=69.911 * 10**6, r_circulation=5.203*R_CIRCULATION_EARTH,
                 k_own=K_OWN/4, time=TIME, angle=0.8)
Saturn = Planet(screen, m=5.683 * 10**26, r_own=58.232 * 10**6, r_circulation=9.555*R_CIRCULATION_EARTH,
                k_own=K_OWN/3.75, time=TIME, angle=0.6)
Uranus = Planet(screen, m=8.681 * 10**25, r_own=25.362 * 10**6, r_circulation=19.22*R_CIRCULATION_EARTH,
                k_own=K_OWN/3.25, time=TIME, angle=0.4)
Neptune = Planet(screen, m=1.024 * 10**26, r_own=24.622 * 10**6, r_circulation=30.11*R_CIRCULATION_EARTH,
                 k_own=K_OWN/3.25, time=TIME, angle=0.2)
# список из всех планет
Planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

# Инициализация объекта, совершающего гравитационный манёвр
voyager = Voyager(screen, color=WHITE, angle=0.01, r_own=100, k_own=K_OWN * 10**4 * 4, v=34000)

# Список всех тел, чей трек мы хотим видеть (!ВАЖНО если это будет новый класс, у него должны присутсвовать
# self.object_track_X = [] self.object_track_Y = [])
Track_list = [voyager, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

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
    voyager.draw_information()

    # Отрисовка трека
    for object in Track_list:
        object.object_track_write()
        object.object_track_draw()

    # Движение тел
    (Mercury.move(), Venus.move(), Earth.move(), Mars.move(),
     Jupiter.move(), Saturn.move(), Uranus.move(), Neptune.move())
    voyager.move()
    # Синхронизация со временем
    clock.tick(FPS)

    # Обработка событий игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]:
        for object in Track_list:
            Event.move_object_on_the_camera(object)
        Event.move_object_on_the_camera(Sun)

    elif keys[pygame.K_MINUS] or keys[pygame.K_EQUALS]:
        Event.change_size()
    pygame.display.update()


pygame.quit()
