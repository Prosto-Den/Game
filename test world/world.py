import pygame
import player
import pickle
import variables as var

ground_img = pygame.Surface((var.TILE_SIZE, var.TILE_SIZE))
ground1_img = pygame.Surface((var.TILE_SIZE, var.TILE_SIZE))
ground1_img.fill(var.BROWN)
player_img = pygame.Surface((var.TILE_SIZE, var.TILE_SIZE))
player_img.fill('grey')


img_tiles = [ground_img, ground1_img, player_img]


class World:
    def __init__(self, game):
        self.game = game

        data = open('levels/level_data_0', 'rb')

        self.world_data = pickle.load(data)

        data.close()

    def proceed_data(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_tiles[tile]
                    rect = img.get_rect()

                    rect.x = x * var.TILE_SIZE
                    rect.y = y * var.TILE_SIZE

                    tile_data = (img, rect)

                    if 0 <= tile <= 1:
                        self.game.obstacle_list.append(tile_data)

                    elif tile == 2:
                        self.game.player = player.Player(self.game, x * var.TILE_SIZE + 100, y * var.TILE_SIZE)

    def draw(self):
        for tile in self.game.obstacle_list:
            tile[1][0] += var.scroll

            self.game.screen.blit(tile[0], tile[1])
