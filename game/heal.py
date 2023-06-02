import pygame
import variables as var


# класс аптечки
class Heal(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int):
        super().__init__()

        self.game = game

        img = pygame.image.load('img/heal/heal.png').convert_alpha()

        self.image = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))

    # метод для отрисовки земли
    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)
