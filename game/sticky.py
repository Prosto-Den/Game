import pygame
import variables as var


# класс "слизи". Позволяет прилипать к стенам
class Sticky(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int, direction: int):
        super().__init__()
        self.game = game

        # загружаем картинку
        img = pygame.image.load('img/sticky/1.png').convert_alpha()
        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

        if direction == -1:
            img = pygame.transform.flip(img, True, False)

        # создаём хитбокс
        self.image = img
        self.rect = self.image.get_rect(topleft = (x, y))

    # метод для отрисовки в мире
    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)