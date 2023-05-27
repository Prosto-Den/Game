import pygame


# класс коробки (Блок, который игрок может толкать)
class Box(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.game = game  # объект главного класса, в котором хранятся объекты других классов

        # создаём картинку и хитбокс
        self.image = image

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect(topleft=(x, y))

    # отрисовка коробки в мире
    def draw(self, scroll):
        # добавляем скроллинг
        self.rect.x += scroll

        self.game.screen.blit(self.image, self.rect)

    # метод толкания коробок
    def move(self, dx):
        # отслеживает, столкнулись со стеной или нет
        wall = False

        for box in self.game.boxes:
            for tile in self.game.obstacle_list:
                if tile[1].colliderect(box.rect.x + dx, box.rect.y, box.width, box.height):
                    wall = True
                    break

            if box != self and not wall:
                if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = box.move(dx)

        if wall:
            dx = 0

        # меняем координату
        self.rect.x += dx

        return dx
