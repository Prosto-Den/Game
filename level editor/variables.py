# размеры экрана
WIDTH = 1000
HEIGHT = int(0.8 * WIDTH)

RIGHT_MARGIN = 250
BOTTOM_MARGIN = 100

RESOLUTION = (WIDTH + RIGHT_MARGIN, HEIGHT + BOTTOM_MARGIN)

# цвета
MENU_COLOR = (132, 177, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (204, 0, 0)

# размеры уровня
ROWS = 16
COLUMNS = 150

# для пролистывания
scroll = 0
scroll_speed = 5
scroll_left = False
scroll_right = False

# для кнопок
current_tile = 0
btn_count = 0

# размер клетки
TILE_SIZE = 50

# номер создаваемого уровня
level = 0

# таймер для ошибки
timer_error = 0

# меню выхода
exit_menu = False

# FPS
FPS = 144
