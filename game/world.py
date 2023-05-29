import pygame.transform
import player
import pickle
import box
import platform
import enemy
import lava
import trampoline
import exit
import variables as var
import os

dir_tiles = os.listdir('img/tiles')

# список с картинками
IMG_LIST = []

# преобразуем картинки
for i in dir_tiles:
    img = pygame.image.load(f'img/tiles/{i}')
    img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

    IMG_LIST.append(img)


# класс для обработки данных уровня
class World:
    def __init__(self, game):
        self.game = game
        self.world_data = []

    # метод обработки данных. Нужен для первичной загрузки мира и рестарта
    def process_data(self):
        # загружаем данные
        with open(f'levels/level_data_{var.level}', 'rb') as data:
            self.world_data = pickle.load(data)

        counter = 0

        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                # если на месте клетки что-то есть
                if tile >= 0:
                    # если это земля
                    if tile == 0:
                        img = IMG_LIST[tile].convert_alpha()
                        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

                        rect = img.get_rect(topleft=(x * var.TILE_SIZE, y * var.TILE_SIZE))

                        tile_data = (img, rect)

                        self.game.obstacle_list.append(tile_data)

                    # если это коробка
                    elif tile == 1:
                        img = IMG_LIST[tile].convert_alpha()
                        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

                        b = box.Box(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE, img)

                        self.game.boxes.append(b)

                    # если это блок лавы
                    elif tile == 2:
                        img = IMG_LIST[tile].convert_alpha()
                        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

                        lav = lava.Lava(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE, img)

                        self.game.ketchup_group.add(lav)

                    # если это батут
                    elif tile == 3:
                        img = IMG_LIST[tile].convert_alpha()
                        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

                        tramp = trampoline.Trampoline(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE, img)

                        self.game.trampolines.append(tramp)

                    # если это блок вертикальной платформы
                    elif tile == 4:
                        counter += 1

                        if row[x + 1] == 4:
                            continue

                        img = IMG_LIST[tile].convert_alpha()

                        img = pygame.transform.scale(img, (img.get_width() * counter, img.get_height()))
                        plat = platform.Platform(self.game, (x - counter + 1) * var.TILE_SIZE,
                                                 y * var.TILE_SIZE, 0, 1, img)

                        self.game.platform_list.append(plat)

                        counter = 0

                    # если это блок горизонтальной платформы
                    elif tile == 5:
                        counter += 1

                        if row[x + 1] == 5:
                            continue

                        img = IMG_LIST[tile - 1].convert_alpha()

                        img = pygame.transform.scale(img, (img.get_width() * counter, img.get_height()))
                        plat = platform.Platform(self.game, (x - counter + 1) * var.TILE_SIZE,
                                                 y * var.TILE_SIZE, 1, 0, img)

                        self.game.platform_list.append(plat)

                        counter = 0

                    # если это игрок
                    elif tile == 6:
                        self.game.player = player.Player(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE)

                    # если это противник
                    elif tile == 7:
                        enm = enemy.Enemy(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE)
                        self.game.enemies.add(enm)

                    # если это блок выхода с уровня
                    if tile == 8:
                        self.game.exit_tile = exit.Exit(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE)

    # рисуем мир
    def draw(self):
        # добавляем пролистывание (скроллинг)
        for tile in self.game.obstacle_list:
            tile[1][0] += var.scroll

            self.game.screen.blit(tile[0], tile[1])
