import pygame
import variables as var


class Sticky(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.image = pygame.Surface((50, 50))
        self.image.fill('green')

        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self):
        for sticky in self.game.sticky_group:
            sticky.rect.x += var.scroll

            self.game.screen.blit(sticky.image, sticky.rect)
