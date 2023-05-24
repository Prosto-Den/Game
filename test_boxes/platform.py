import pygame
import variables as var


# класс движущейся платформы
class Platform:
    def __init__(self, game, x: int, y: int, move_x: int, move_y: int, image: pygame.Surface):
        self.game = game

        # картинка и хитбокс
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        # стартовая позиция
        self.start_x = self.rect.x
        self.start_y = self.rect.y

        # радиус перемещения
        self.radius = 3

        # скорость перемещения
        self.speed = 1

        # переменные сдвига
        self.dx = 0
        self.dy = 0

        # направление передвижения платформы
        self.move_x = move_x
        self.move_y = move_y

    # отрисовка платформы на экране
    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    # перемещение платформы
    def move(self):
        # скроллинг
        self.rect.x += var.scroll
        self.start_x += var.scroll

        # если платформа двигается по горизонтали
        if self.move_x != 0:
            # проверка, вышла ли платформа за радиус перемещения
            if self.rect.x >= self.start_x + self.radius * var.TILE_SIZE or \
                    self.rect.x <= self.start_x - self.radius * var.TILE_SIZE:
                self.move_x *= -1

            # проверка на столкновение со стенами
            for ground in self.game.obstacle_list:
                if ground[1].colliderect(self.rect.x + self.dx, self.rect.y, self.image.get_width(),
                                         self.image.get_height()):
                    self.move_x *= -1

            # проверка на столкновение с другими платформами
            for plat in self.game.platform_list:
                if self != plat:
                    if plat.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.image.get_width(),
                                             self.image.get_height()):
                        plat.move_x *= -1
                        self.move_x *= -1

            # обновляем переменную передвижения
            self.dx = self.speed * self.move_x

        if self.move_y != 0:
            # проверка, вышла ли платформа за радиус перемещения
            if self.rect.y <= self.start_y - self.radius * var.TILE_SIZE or \
                    self.rect.y >= self.start_y + self.radius * var.TILE_SIZE:
                self.move_y *= -1

            # проверка на столкновение со стенами
            for ground in self.game.obstacle_list:
                if ground[1].colliderect(self.rect.x, self.rect.y + self.dy, self.image.get_width(), self.image.get_height()):
                    self.move_y *= -1

            self.dy = self.speed * self.move_y

        # двигаем платформу
        self.rect.x += self.dx
        self.rect.y += self.dy
