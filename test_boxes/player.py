import pygame
import variables as var
import bullet


# класс игрока
class Player:
    def __init__(self, game, x: int, y: int):
        self.game = game

        # загружаем картинку и создаём хитбокс
        img = pygame.image.load('img/player/1.png').convert_alpha()
        self.image = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))
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

        # для прилипания к стенке
        self.sticky = False
        self.ground = True

        self.on_platform = False

    # отрисовка игрока на экране
    def draw(self):
        self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    # перемещение игрока
    def move(self):
        # переменные для перемещения
        dx = dy = 0

        # переменная для скроллинга
        scroll = 0

        col_thresh = 20

        # направо
        if self.moving_right:
            dx += self.speed
            self.direction = 1
            self.flip = False
            self.ground = True

        # налево
        if self.moving_left:
            dx -= self.speed
            self.direction = -1
            self.flip = True
            self.ground = True

        # прыжок
        if self.jump and not self.in_air and not self.sticky:
            self.vel_y = -self.jump_force
            self.jump = False
            self.in_air = True

        # стрельба
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

        # проверка на прилипание
        if pygame.sprite.spritecollide(self, self.game.sticky_group, False):
            self.sticky = True
            self.ground = False

        else:
            self.sticky = False

        # если прилип
        if self.sticky:
            dy = 0
            self.in_air = False

            if self.jump:
                self.vel_y = -self.jump_force
                dy = self.vel_y

                self.sticky = False
                self.in_air = True

        # если уже отлип, но ещё не на земле
        if not self.sticky and not self.ground:
            if self.direction < 0 and not self.moving_left:
                dx += self.speed * 2

            elif self.direction > 0 and not self.moving_right:
                dx -= self.speed * 2

        # проверка стокновения с платформой
        for plat in self.game.platform_list:
            if plat.rect.colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                self.ground = True
                dx = 0

            if plat.rect.colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                if abs((self.rect.top + dy) - plat.rect.bottom) < col_thresh:
                    self.vel_y = 0
                    dy = plat.rect.bottom - self.rect.top

                elif abs((self.rect.bottom + dy) - plat.rect.top) < col_thresh:
                    self.rect.bottom = plat.rect.top - 1
                    dy = 0
                    self.in_air = False

                if plat.move_x != 0:
                    self.rect.x += plat.dx

        # проверка на столкновения со стенками/полом
        for tile in self.game.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top

                elif self.vel_y >= 0 \
                        and not tile[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(),
                                                    self.image.get_height()):
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

                    self.ground = True

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
                    self.ground = True

        # проверка выхода за границу экрана сверху
        if self.rect.top + dy < 0:
            dy = -self.rect.top

        # изменяем координаты игрока
        self.rect.x += dx
        self.rect.y += dy

        # скроллинг
        if (self.rect.right > var.WIDTH - var.SCROLL_THRESH and var.bg_scroll < var.COLUMNS * var.TILE_SIZE - var.WIDTH) \
                or (self.rect.left <= var.SCROLL_THRESH and var.bg_scroll > abs(dx)):
            self.rect.x -= dx
            scroll -= dx

        return scroll
