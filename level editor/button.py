import pygame
import variables as var


class Button:
    def __init__(self, image: pygame.Surface, x: int, y: int):
        super().__init__()

        image = pygame.transform.scale(image, (var.TILE_SIZE, var.TILE_SIZE))
        self.image: pygame.Surface = image
        self.rect = self.image.get_rect(topleft = (x, y))

        self.clicked = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        return action
