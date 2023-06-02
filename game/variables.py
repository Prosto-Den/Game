import os

# разрешение окна
WIDTH = 1000
HEIGHT = 800

RESOLUTION = (WIDTH, HEIGHT)

# цвета
MENU_COLOR = (132, 177, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# частота кадров
FPS = 120

# переменные для скроллинга
scroll = 0
bg_scroll = 0
SCROLL_THRESH = 400

# размер клеток
TILE_SIZE = 50

# номер текущего уровня
level = 0

# кол-во уровней
MAX_LEVEL = len(os.listdir('levels')) - 1

# переменная для отображения главного меню
main_menu = True

# таймеры
restart_timer = 100
congratulation_timer = 0

# Размеры мира
ROWS = 16
COLUMNS = 150
