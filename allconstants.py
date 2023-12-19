from ctypes import windll


FPS = 30

# Цвета игры
BLUE = (90, 139, 207)
YELLOW = (255, 205, 0)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
WHITE = (250, 255, 255)
SPACE = (25, 25, 62)

# Размер окна
WIDTH, HEIGHT = windll.user32.GetSystemMetrics(0) - 10, windll.user32.GetSystemMetrics(1) - 80

# Физические константы в СИ
G = 6.6743 / 10 ** 11
M_SUN = 1.9885 * 10 ** 30
R_OWN_SUN = 100.34 * 10 ** 6
M_EARTH = 5.9742 * 10 ** 24
R_CIRCULATION_EARTH = 1.49598 * 10 ** 11
R_OWN_EARTH = 6.371 * 10 ** 6
V_ORBITAL_EARTH = 4 * 10 ** 4
V_OWN_ROTATION_EARTH = 465.1013  # на экваторе
# Радиус удаления от Солнца. Нужен, чтобы отдалить планеты от звезды, противодействует слипанию
R_START = 0
