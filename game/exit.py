import pygame
import variables as var


class Exit:
    def __init__(self, game, x, y):
        self.game = game

        img = pygame.image.load('img/exit/tile9.png').convert_alpha()

        self.image = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)

    def exit(self):
        if self.rect.colliderect(self.game.player.rect):
            if var.level < var.MAX_LEVEL:
                var.level += 1
                self.game.restart()