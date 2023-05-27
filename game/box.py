import pygame


# класс коробки (Блок, который игрок может толкать)
class Box(pygame.sprite.Sprite):
    def __init__(self, game, x: int, y: int, image: pygame.Surface):
        super().__init__()
        self.game = game  # объект главного класса, в котором хранятся объекты других классов

        # создаём картинку и хитбокс
        self.image = image

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

        # проверка столкновения со стенкой для самой коробки
        for ground in self.game.obstacle_list:
            if ground[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                dx = 0

        # сложная проверка для столкновения цепи коробок
        for box in self.game.boxes:
            if box != self:
                # если коробка столкнулась с другой коробкой
                if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                    # проверяем, столкнулась ли вторая коробка со стенкой
                    for ground in self.game.obstacle_list:
                        if ground[1].colliderect(box.rect.x + dx, box.rect.y, box.image.get_width(),
                                                 box.image.get_height()):
                            # если да, поднимаем флаг и выходим из цикла
                            wall = True
                            break
                    # если стены нет, двигаем коробку
                    if not wall:
                        dx = box.move(dx)

                    # если есть, стоим на месте
                    else:
                        dx = 0

        # меняем координату
        self.rect.x += dx

        return dx
