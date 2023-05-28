import pygame
import variables as var


class Trampoline:
    def __init__(self, game, x, y, img: pygame.Surface):
        self.game = game

        self.image = img
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)