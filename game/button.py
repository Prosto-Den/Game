import pygame


# класс кнопки
class Button:
    def __init__(self, game, x, y, img: pygame.Surface):
        self.game = game

        # создаём картинку и хитбокс
        self.image = img
        self.rect = self.image.get_rect(center = (x, y))

        # флаг проверки, нажимали на кнопку или нет
        self.active = True

    # метод отрисовки кнопки
    def draw(self):
        clicked = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.active:
                clicked = True
                self.active = False

            elif not pygame.mouse.get_pressed()[0]:
                self.active = True

        self.game.screen.blit(self.image, self.rect)

        return clicked
