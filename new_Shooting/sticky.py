import pygame


class Sticky(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.image = pygame.Surface((50, 50))
        self.image.fill('green')

        self.rect = self.image.get_rect(topleft = (x, y))