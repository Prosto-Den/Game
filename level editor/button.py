import pygame
import variables as var


# класс кнопка
class Button:
    def __init__(self, image, x, y):
        img = image

        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

        self.image = img
        self.rect = self.image.get_rect(topleft = (x, y))
        self.clicked = False

    # отображение на экране и проверка, нажата ли кнопка
    def draw(self, screen):
        # рисуем кнопку на экране
        screen.blit(self.image, self.rect)

        action = False

        # получаем позицию мыши
        pos = pygame.mouse.get_pos()

        # если мышь и кнопка пересекаются
        if self.rect.collidepoint(pos):
            # если ЛКМ нажата и до этого кнопку ещё не нажимали
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True

            # если ЛКМ не нажата
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        # возвращаем действие
        return action
