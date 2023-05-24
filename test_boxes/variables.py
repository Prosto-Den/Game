import pygame
import os

# разрешение окна
WIDTH = 1000
HEIGHT = 800

RESOLUTION = (WIDTH, HEIGHT)

# цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# частота кадров
FPS = 144

# переменные для скроллинга
scroll = 0
SCROLL_THRESH = 200

# размер клеток
TILE_SIZE = 50

# Размеры мира
ROWS = 16
COLUMNS = 150

# картинки клеток
dir_tiles = os.listdir('img/tiles')

# список с картинками
IMG_LIST = []

# преобразуем картинки
for i in dir_tiles:
    img = pygame.image.load(f'img/tiles/{i}')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    IMG_LIST.append(img)

# добавляем изображение игрока
player_img = pygame.image.load('img/player/1.png')
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

IMG_LIST.append(player_img)
