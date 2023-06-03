import pygame
import variables as var


# класс лавы. При соприкосновении с этим блоком игрок будет мгновенно умирать
class Lava(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.game = game

        self.image = image
        self.rect = self.image.get_rect(topleft = (x, y))

        self.rect.height -= 1
        self.rect.width -= 1

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    # метод для отрисовки блока
    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)