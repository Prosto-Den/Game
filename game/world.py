import pygame.transform
import player
import pickle
import box
import platform
import os
import variables as var

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

        # загружаем данные
        with open('levels/level_data_0', 'rb') as data:
            self.world_data = pickle.load(data)

        # сразу же их анализируем
        counter = 0

        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                # если на месте клетки что-то есть
                if tile >= 0:
                    # если это земля
                    if tile == 0:
                        img = IMG_LIST[tile].convert_alpha()
                        rect = img.get_rect(topleft=(x * var.TILE_SIZE, y * var.TILE_SIZE))

                        tile_data = (img, rect)

                        self.game.obstacle_list.append(tile_data)

                    # если это коробка
                    if tile == 1:
                        img = IMG_LIST[tile].convert_alpha()
                        b = box.Box(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE, img)

                        self.game.boxes.append(b)

                    if tile == 2:
                        pass

                    if tile == 3:
                        pass

                    if tile == 4:
                        counter += 1

                        if row[x + 1] == 4:
                            continue

                        img = IMG_LIST[tile].convert_alpha()

                        img = pygame.transform.scale(img, (img.get_width() * counter, img.get_height()))
                        plat = platform.Platform(self.game, (x - counter + 1) * var.TILE_SIZE,
                                                 y * var.TILE_SIZE, 0, 1, img)

                        self.game.platform_list.append(plat)

                        counter = 0

                    if tile == 5:
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
                    if tile == 6:
                        self.game.player = player.Player(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE)

    # рисуем мир
    def draw(self):
        # добавляем пролистывание (скроллинг)
        for tile in self.game.obstacle_list:
            tile[1][0] += var.scroll

            self.game.screen.blit(tile[0], tile[1])
