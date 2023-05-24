import pygame
import variables as var
import bullet

# класс игрока
class Player:
    def __init__(self, game, x: int, y: int):
        self.game = game

        # загружаем картинку и создаём хитбокс
        self.image = var.player_img.convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

        # скорость игрока
        self.speed = 3

        # переменные для прыжка
        self.vel_y = 0
        self.gravity = 0.75
        self.jump_force = 11

        # направление игрока
        self.direction = 1
        self.flip = False

        # флаги для перемещения
        self.moving_right = False
        self.moving_left = False

        # флаги для прыжка
        self.jump = False
        self.in_air = True

        # флаг для стрельбы
        self.fire = False

        # отключаем скроллинг в самом начале игры
        self.on_scroll = False

        self.sticky = False
        self.sticky_timer = 0

    # отрисовка игрока на экране
    def draw(self):
        self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    # перемещение игрока
    def move(self):
        # переменные для перемещения
        dx = dy = 0

        # переменная для скроллинга
        scroll = 0

        # направо
        if self.moving_right:
            dx += self.speed
            self.direction = 1
            self.flip = False

        # налево
        if self.moving_left:
            dx -= self.speed
            self.direction = -1
            self.flip = True

        # прыжок
        if self.jump and not self.in_air and not self.sticky:
            self.vel_y = -self.jump_force
            self.jump = False
            self.in_air = True

        if self.fire:
            blt = bullet.Bullet(self.game, self.rect.centerx + self.image.get_width() * 0.6 * self.direction,
                                self.rect.centery - self.image.get_height() * 0.6, self.direction)

            self.game.bullet_group.add(blt)

            self.fire = False

        # добавляем гравитацию
        self.vel_y += self.gravity

        # ограничиваем скорость падения
        if self.vel_y >= 10:
            self.vel_y = 10

        """Вот тут изменяем переменную для перемещения"""
        dy += self.vel_y

        # проверка на столкновения со стенками/полом
        for tile in self.game.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

                    if self.sticky_timer > 0:
                        self.sticky_timer = 0

            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                dx = 0

        # проверка на столкновение с коробками
        for box in self.game.boxes:
            if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                dx = box.move(dx)

            if box.rect.colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                if self.vel_y > 0:
                    dy = box.rect.top - self.rect.bottom
                    self.in_air = False

        if pygame.sprite.spritecollide(self, self.game.sticky_group, False):
            self.sticky = True

        else:
            self.sticky = False

        if self.sticky:
            dy = 0
            self.in_air = False

            if self.jump:
                self.sticky_timer = 45

                self.vel_y = -self.jump_force
                dy = self.vel_y

                self.sticky = False
                self.in_air = True

        if self.sticky_timer > 0:
            self.sticky_timer -= 1

            if self.direction < 0 and not self.moving_left:
                dx += self.speed * 2

            elif self.direction > 0 and not self.moving_right:
                dx -= self.speed * 2

        if self.rect.top + dy < 0:
            dy = -self.rect.top

        # изменяем координаты игрока
        self.rect.x += dx
        self.rect.y += dy

        # включаем скроллинг
        if self.rect.x >= var.SCROLL_THRESH + 10:
            self.on_scroll = True

        # скроллинг
        if self.on_scroll:
            if self.rect.x >= var.WIDTH - var.SCROLL_THRESH or self.rect.x <= var.SCROLL_THRESH:
                self.rect.x -= dx
                scroll -= dx

        return scroll
