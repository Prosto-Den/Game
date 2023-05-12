import pygame
import variables as var


class Button:
    def __init__(self, image, x, y):
        img = image

        img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

        self.image = img
        self.rect = self.image.get_rect(topleft = (x, y))
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        return action
