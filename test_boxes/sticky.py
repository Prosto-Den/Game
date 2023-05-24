import pygame
import variables as var


class Sticky(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()
        self.game = game

        img = pygame.image.load('img/sticky/1.png')
        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

        if direction == -1:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)