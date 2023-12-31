import math
import matplotlib.pyplot as plt
import pygame
from allconstants import *

# Масштабные коэффициенты (могут меняться для каждого тела); коэффициент увелечения скорости:
# увеличение линейного размера тел, увеличение расстояния между телами; коэффициент увелечения скорости
K_OWN, K_CIRCULATION, K_CIRCULATION_START = 1 / 10 ** 6 / 2, 1 / 10 ** 10 / 0.3, 1 / 10 ** 10 / 0.3
# Время в с, за которое сменяется кадр
TIME = 288 * 10 ** 3
CHANGE_TIME = 5000

# Время одной итерации в с
dt = 500


class BaseBody:
    """ Класс BaseBody
    описывает тела, движущиеся в системе звезды по различным траекториям.
    """

    def __init__(self, scr, angle=0.0, m=M_EARTH,
                 r_own=R_OWN_EARTH, r_circulation=R_CIRCULATION_EARTH, color=BLUE,
                 k_own=K_OWN, k_circulation=K_CIRCULATION, v=0):
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
        self.screen = scr
        self.r_own, self.k_own, self.k_circulation = r_own, k_own, k_circulation
        self.color, self.r_circulation = color, r_circulation
        self.time = 0
        if v == 0:
            v = math.sqrt(G * M_SUN / r_circulation)
        self.vx, self.vy = -1 * v * math.sin(angle), v * math.cos(angle)
        self.m = m
        self.x, self.y = Sun.x + self.r_circulation * math.cos(angle), Sun.y + self.r_circulation * math.sin(angle)
        self.angle = angle
        self.__ax, self.__ay = 0, 0
        self.acceleration()
        self.tick = 0  # переменная для подсчёта количество выполненных циклов и перевод их в дни и годы
        self.object_track_X = []
        self.object_track_Y = []
        self.memoryV = [(self.vx**2+self.vy**2)**0.5/1000]
        self.memoryT = [0]

    def acceleration(self):
        a_sun_acceleration = G * M_SUN / ((self.x - Sun.x) ** 2 + (self.y - Sun.y) ** 2)
        self.angle = math.atan2(self.y - Sun.y, self.x - Sun.x)
        self.__ax = -1 * a_sun_acceleration * math.cos(self.angle)
        self.__ay = -1 * a_sun_acceleration * math.sin(self.angle)

    def move(self):
        """Перемещает тело по прошествии единицы времени.

        Метод описывает перемещение тела за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy.
        """
        self.acceleration()
        self.vx -= self.__ax * dt
        self.vy -= self.__ay * dt
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
    def __init__(self, scr, angle=0.0, m=M_EARTH,
                 r_own=R_OWN_EARTH, r_circulation=R_CIRCULATION_EARTH, color=BLUE,
                 k_own=K_OWN, k_circulation=K_CIRCULATION, v=0):
        super().__init__(scr, angle, m, r_own, r_circulation, color, k_own, k_circulation, v)
        self.auto_zoomer = False
        self.distance_from_voyager_2 = 10**22


class Voyager(BaseBody):
    """ Класс Voyager
    описывает тело, совершающее гравитационный манёвр.
    """

    def move(self):
        self.acceleration()
        self.vx -= self.__ax * dt
        self.vy -= self.__ay * dt
        self.x -= self.vx * dt
        self.y -= self.vy * dt

    def acceleration(self):
        a_sun_perpendicular = G * M_SUN / ((self.x - Sun.x) ** 2 + (self.y - Sun.y) ** 2)
        self.angle = math.atan2(self.y - Sun.y, self.x - Sun.x)
        self.__ax = -1 * a_sun_perpendicular * math.cos(self.angle)
        self.__ay = -1 * a_sun_perpendicular * math.sin(self.angle)
        for planet in Planets:
            self.__ax += (G * planet.m / (math.sqrt((planet.x - self.x) ** 2 + (planet.y - self.y) ** 2)) ** 3 *
                          (planet.x - self.x))
            self.__ay += (G * planet.m / (math.sqrt((planet.x - self.x) ** 2 + (planet.y - self.y) ** 2)) ** 3 *
                          (planet.y - self.y))

    def draw_information(self):
        self.time += TIME
        year = int(self.time // (365.25 * 86400))
        day = (self.time // 86400) % 365
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
        text2 = f1.render('скорость Вояджера ' + str(round(math.sqrt(self.vx ** 2 + self.vy ** 2) / 1000, 2)) + ' км/с',
                          1, (255, 255, 255))
        text3 = f1.render('расстояние от Вояджера до Солнца ' +
                          str(round(math.sqrt((self.x - Sun.x) ** 2 +
                                              (self.y - Sun.y) ** 2) / R_CIRCULATION_EARTH, 2)) + ' а.е.',
                          1, (255, 255, 255))
        text4 = f1.render(str(round(150 / self.k_circulation / 1000, 0)) + 'км', 1, (255, 255, 255))
        pygame.draw.line(screen, WHITE, [10, HEIGHT - 100], [160, HEIGHT - 100])
        pygame.draw.line(screen, WHITE, [10, HEIGHT - 105], [10, HEIGHT - 95])
        pygame.draw.line(screen, WHITE, [160, HEIGHT - 105], [160, HEIGHT - 95])
        screen.blit(text1, (15, 15))
        screen.blit(text2, (15, 50))
        screen.blit(text3, (15, 85))
        screen.blit(text4, (15, HEIGHT - 130))

    def memorize_vt(self):
        self.memoryV.append((self.vx**2+self.vy**2)**0.5/1000)
        self.memoryT.append(dt / (24 * 3600) + self.memoryT[-1])


class Star:
    def __init__(self, scr, x=WIDTH / 2 / K_CIRCULATION, y=HEIGHT / 2 / K_CIRCULATION, r_own=R_OWN_SUN,
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
        self.screen = scr
        self.x, self.y, self.m = x, y, m
        self.r_own, self.k_own, self.k_circulation = r_own, k_own, k_circulation
        self.color = color
        self.object_track_X = []
        self.object_track_Y = []
        self.auto_zoomer = True

    def draw(self):
        """ Метод отрисовки звезды. Обновляет положение тела на экране с учетом self.x и self.y.
        """
        pygame.draw.circle(self.screen, center=(self.x * K_CIRCULATION, self.y * K_CIRCULATION),
                           radius=self.r_own * self.k_own, color=self.color)


def move_object_on_the_camera():
    # Здесь заложено перемещение заданной сущности
    if keys[pygame.K_w]:
        for elem in Track_list:
            elem.y += 10 / K_CIRCULATION
            for i in range(len(elem.object_track_X)):
                elem.object_track_Y[i] += 10 / K_CIRCULATION
        Sun.y += 10 / K_CIRCULATION

    if keys[pygame.K_s]:
        for elem in Track_list:
            elem.y -= 10 / K_CIRCULATION
            for i in range(len(elem.object_track_X)):
                elem.object_track_Y[i] -= 10 / K_CIRCULATION
        Sun.y -= 10 / K_CIRCULATION

    if keys[pygame.K_d]:
        for elem in Track_list:
            elem.x -= 10 / K_CIRCULATION
            for i in range(len(elem.object_track_X)):
                elem.object_track_X[i] -= 10 / K_CIRCULATION
        Sun.x -= 10 / K_CIRCULATION

    if keys[pygame.K_a]:
        for elem in Track_list:
            elem.x += 10 / K_CIRCULATION
            for i in range(len(elem.object_track_X)):
                elem.object_track_X[i] += 10 / K_CIRCULATION
        Sun.x += 10 / K_CIRCULATION


def change_size(k=1.25, auto_little=False, auto_bigger=False):
    global K_CIRCULATION, K_OWN
    if keys[pygame.K_MINUS] or auto_little:
        K_OWN /= k
        K_CIRCULATION /= k
        for elem in Track_list:
            elem.k_own /= k
            elem.k_circulation /= k
        Sun.k_own /= k
        Sun.k_circulation /= k
        for elem in Track_list:
            elem.x += WIDTH * 0.100 / K_CIRCULATION
            elem.y += HEIGHT * 0.100 / K_CIRCULATION
            for i in range(len(elem.object_track_X)):
                elem.object_track_X[i] += WIDTH * 0.1 / K_CIRCULATION
                elem.object_track_Y[i] += HEIGHT * 0.1 / K_CIRCULATION
        Sun.x += WIDTH * 0.1 / K_CIRCULATION
        Sun.y += HEIGHT * 0.1 / K_CIRCULATION

    if keys[pygame.K_EQUALS] or auto_bigger:
        K_OWN *= k
        K_CIRCULATION *= k
        for elem in Track_list:
            elem.k_own *= k
            elem.k_circulation *= k
        Sun.k_own *= k
        Sun.k_circulation *= k
        for elem in Track_list:
            elem.x -= WIDTH * 0.125 / K_CIRCULATION
            elem.y -= HEIGHT * 0.125 / K_CIRCULATION
            for i in range(len(elem.object_track_X)):
                elem.object_track_X[i] -= WIDTH * 0.125 / K_CIRCULATION
                elem.object_track_Y[i] -= HEIGHT * 0.125 / K_CIRCULATION
        Sun.x -= WIDTH * 0.125 / K_CIRCULATION
        Sun.y -= HEIGHT * 0.125 / K_CIRCULATION


def auto_zoom(planet, change_radius=True, make_little=False, k_circulation_special=1/10 ** 7 / 1.25):
    global TIME, dt
    planet.auto_zoomer = True
    delta_x = (WIDTH / 2) / K_CIRCULATION - planet.x
    delta_y = (HEIGHT / 2) / K_CIRCULATION - planet.y
    for elem in Track_list:
        elem.x += delta_x
        for i in range(len(elem.object_track_X)):
            elem.object_track_X[i] += delta_x
    Sun.x += delta_x
    for elem in Track_list:
        elem.y += delta_y
        for i in range(len(elem.object_track_X)):
            elem.object_track_Y[i] += delta_y
    Sun.y += delta_y
    if not make_little:
        if 1 / K_CIRCULATION > 1/k_circulation_special and change_radius:
            change_size(auto_bigger=True)
        if 1 / K_CIRCULATION / 1.25 < 1/k_circulation_special:
            make_little = True
        if planet.r_own * planet.k_own > 4:
            planet.k_own *= 0.8
        if voyager.r_own * voyager.k_own > 4:
            voyager.k_own *= 0.8
    if make_little:
        if K_CIRCULATION > K_CIRCULATION_START and change_radius:
            change_size(auto_little=True)
        elif K_CIRCULATION <= K_CIRCULATION_START:
            TIME = 288 * 10 ** 3
        if planet.r_own * planet.k_own < 2:
            planet.k_own /= 0.8
        if voyager.r_own * voyager.k_own < 2:
            voyager.k_own /= 0.8


def change_time():
    global TIME, CHANGE_TIME
    if keys[pygame.K_r]:
        TIME += CHANGE_TIME
    if keys[pygame.K_f]:
        TIME -= CHANGE_TIME


# Инициализация окна, синхронизация со временем
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Инициализация Солнца
Sun = Star(screen, k_own=K_OWN / 5)
# Инициализация планет солнечной системы
Mercury = Planet(screen, m=3.3 * 10 ** 23, r_circulation=0.387 * R_CIRCULATION_EARTH,
                 angle=1.4, color=(188, 143, 143))
Venus = Planet(screen, m=4.869 * 10 ** 24, r_circulation=0.723 * R_CIRCULATION_EARTH,
               angle=1.2, color=(245, 222, 179))
Earth = Planet(screen, color=(0, 0, 205))
Mars = Planet(screen, m=6.419 * 10 ** 23, r_circulation=1.523 * R_CIRCULATION_EARTH,
              angle=5.65625, color=(205, 133, 63))
Jupiter = Planet(screen, m=1.899 * 10 ** 27, r_circulation=5.203 * R_CIRCULATION_EARTH,
                 angle=4.511, color=(210, 105, 30))
Saturn = Planet(screen, m=5.685 * 10 ** 26, r_circulation=9.555 * R_CIRCULATION_EARTH,
                angle=3.80045, color=(222, 184, 135))
Uranus = Planet(screen, m=8.685 * 10 ** 25, r_circulation=19.22 * R_CIRCULATION_EARTH,
                angle=3.1583086, color=(135, 206, 250))
Neptune = Planet(screen, m=1.024 * 10 ** 26, r_circulation=30.11 * R_CIRCULATION_EARTH,
                 angle=2.85, color=(65, 105, 225))
# список из всех планет
Planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

# Инициализация объекта, совершающего гравитационный манёвр
voyager = Voyager(screen, color=WHITE, angle=-0.01, r_own=100, k_own=K_OWN * 10 ** 4 * 5, v=40300)

# Список всех тел, чей трек мы хотим видеть (!ВАЖНО если это будет новый класс, у него должны быть
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
    for obj in Track_list:
        obj.object_track_write()
        obj.object_track_draw()

    # Движение тел
    for t in range(0, TIME, dt):
        (Mercury.move(), Venus.move(), Earth.move(), Mars.move(),
         Jupiter.move(), Saturn.move(), Uranus.move(), Neptune.move())
        voyager.move()
        # Запись скорости и времени для графика
        voyager.memorize_vt()

    # Синхронизация со временем
    clock.tick(FPS)

    # Обработка событий игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]:
        move_object_on_the_camera()

    elif keys[pygame.K_MINUS] or keys[pygame.K_EQUALS]:
        change_size()

    for item in Track_list[4:]:
        if (item.x - voyager.x) ** 2 + (item.y - voyager.y) ** 2 < 10 ** 21:
            s = (item.x - voyager.x) ** 2 + (item.y - voyager.y) ** 2
            if (item.distance_from_voyager_2 > s) and 10 ** 17 < s < 10 ** 20:
                TIME = 25 * 10 ** 2
                auto_zoom(item)
            elif s < 10 ** 17 + 1:
                TIME = 500
                auto_zoom(item, k_circulation_special=1 / 10 ** 6 * 2)
            elif (item.distance_from_voyager_2 < s) and 10 ** 17 < s < 10 ** 19:
                TIME = 25 * 10 ** 2
                auto_zoom(item)
            elif (item.distance_from_voyager_2 < s) and 2 * 10 ** 19 > s > 10 ** 19 and item.auto_zoomer:
                TIME = 25 * 10 ** 2
                auto_zoom(item, make_little=True)
            elif (item.distance_from_voyager_2 < s) and s > 2 * 10 ** 19 and item.auto_zoomer:
                TIME = 288 * 10 ** 3
                auto_zoom(item, make_little=True)
            item.distance_from_voyager_2 = s
    change_time()
    pygame.display.update()

pygame.quit()

plt.plot(voyager.memoryT, voyager.memoryV)
plt.xlabel('t, дни')
plt.ylabel("V, км/с")
plt.grid()
plt.title("Зависимость Скорости от времени")
plt.show()
