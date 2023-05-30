import pygame
import variables as var


# класс для выхода с уровня
class Exit:
    def __init__(self, game, x, y):
        self.game = game

        img = pygame.image.load('img/exit/tile9.png').convert_alpha()

        self.image = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))

    # отрисовка на экране
    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)

    # переход на следующий уровень
    def exit(self):
        if self.rect.colliderect(self.game.player.rect):
            # если это не последний уровень уровень
            if var.level < var.MAX_LEVEL:
                var.level += 1
                self.game.restart()

            # если это был последний уровень
            elif var.level == var.MAX_LEVEL:
                var.level = 0
                var.congratulation_timer = 500
                var.main_menu = True
                self.game.restart()
