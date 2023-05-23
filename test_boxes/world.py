import player
import pickle
import box
import variables as var


# класс для обработки данных уровня
class World:
    def __init__(self, game):
        self.game = game

        # загружаем данные
        with open('levels/level_data_0', 'rb') as data:
            self.world_data = pickle.load(data)

        # сразу же их анализируем
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                # если на месте клетки что-то есть
                if tile >= 0:
                    # загружаем картинку и создаём хитбокс
                    img = var.IMG_LIST[tile].convert_alpha()
                    rect = img.get_rect(topleft=(x * var.TILE_SIZE, y * var.TILE_SIZE))

                    tile_data = (img, rect)

                    # если это земля
                    if tile == 0 or 2 <= tile <= 4:
                        self.game.obstacle_list.append(tile_data)

                    # если это коробка
                    if tile == 1:
                        b = box.Box(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE, img)

                        self.game.boxes.append(b)

                    # если это игрок
                    if tile == 5:
                        self.game.player = player.Player(self.game, x * var.TILE_SIZE, y * var.TILE_SIZE)

    # рисуем мир
    def draw(self):
        # добавляем пролистывание (скроллинг)
        for tile in self.game.obstacle_list:
            tile[1][0] += var.scroll

            self.game.screen.blit(tile[0], tile[1])
