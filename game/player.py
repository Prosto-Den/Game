import pygame
import variables as var
import bullet
import os


# класс игрока
class Player:
    def __init__(self, game, x: int, y: int):
        self.game = game

        # список со всеми анимациями
        action_list = ['stand', 'walk', 'jump', 'push', 'death']

        # для анимации
        self.animation_list = []
        self.action = 0
        self.frame = 0

        # загрузка картинок
        for i in action_list:
            temp_list = []

            images = os.listdir(f'img/player/{i}')

            for j in images:
                img = pygame.image.load(f'img/player/{i}/{j}').convert_alpha()
                img = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))

                temp_list.append(img)

            self.animation_list.append(temp_list)

        # выбираем картинку и создаём хитбокс
        self.image = self.animation_list[0][0]
        self.rect = self.image.get_rect(topleft = (x, y))

        # размеры игрока
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.health = 3
        self.alive = True
        self.invincibility = False
        self.invincibility_timer = 0

        # скорость игрока
        self.speed = 3

        # переменные для прыжка
        self.vel_y = 0
        self.gravity = 0.5
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

    # отрисовка игрока на экране
    def draw(self):
        self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    # метод для полного обновления игрока. Нужен, чтобы не вызывать много методов
    def update(self):
        # анимируем
        self.animate()

        # если персонаж жив
        if self.alive:
            # даём возможность перемещать персонажа и получаем переменную для скроллинга
            var.scroll = self.move()

            # переменная для параллакса
            var.bg_scroll -= var.scroll

        else:
            self.death()

    # метод для анимации персонажа
    def animate(self):
        self.frame += 0.15

        if self.frame >= len(self.animation_list[self.action]):
            self.frame = 0

        self.image = self.animation_list[self.action][int(self.frame)]

    # изменяет анимацию
    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame = 0

    # метод для гибели персонажа. Покойся с миром, дружок :(
    def death(self):
        # снижаем здоровье до 0
        self.health = 0

        # убираем скроллинг
        var.scroll = 0

        # ставим анимацию смерти
        self.update_action(4)

        dy = 0

        # перемещение нашего приведения
        if self.rect.y > var.HEIGHT // 2 - 100:
            dy -= self.speed

        # таймер до появления кнопки рестарта
        elif var.restart_timer > 0:
            var.restart_timer -= 1

        self.rect.y += dy

    # перемещение игрока
    def move(self):
        # проверяем, жив ли игрок
        if self.health <= 0 or self.rect.y > var.HEIGHT:
            self.alive = False

            return 0

        # переменные для перемещения
        dx = dy = 0

        # переменная для скроллинга
        scroll = 0

        # для правильной работы столкновения с платформами
        col_thresh = 20

        # проверяем, толкаем мы коробку или нет
        push = False

        # движение направо
        if self.moving_right:
            dx += self.speed
            self.flip = False
            self.direction = 1
            self.ground = True

        # движение налево
        if self.moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
            self.ground = True

        # прыжок
        if self.jump and not self.in_air and not self.sticky:
            self.vel_y = -self.jump_force
            self.in_air = True
            #self.jump = False

        # стрельба
        if self.fire:
            if self.flip:
                blt = bullet.Bullet(self.game, self.rect.centerx + self.width // 2 * self.direction, self.rect.y, -1)

            else:
                blt = bullet.Bullet(self.game, self.rect.centerx + self.width // 2 * self.direction, self.rect.y, 1)

            self.game.bullet_group.add(blt)

            self.fire = False

        # гравитация
        self.vel_y += self.gravity

        # ограничение для вертикальной скорости
        if self.vel_y >= 10:
            self.vel_y = 10

        """Меняем переменную перемещения"""
        dy += self.vel_y

        # прилипание к стенкам
        if pygame.sprite.spritecollide(self, self.game.sticky_group, False):
            self.sticky = True
            self.in_air = False
            self.ground = False

        else:
            self.sticky = False

        # если прилипли
        if self.sticky:
            dy = 0

            if self.jump:
                self.vel_y = -self.jump_force
                dy = self.vel_y

                self.sticky = False
                self.in_air = True

        # если уже отлипли от стены, но ещё не приземлились
        if not self.sticky and not self.ground:
            if self.direction < 0 and not self.moving_left:
                self.flip = False
                dx += self.speed

            elif self.direction > 0 and not self.moving_right:
                self.flip = True
                dx -= self.speed

        # столкновение со стенками
        for tile in self.game.obstacle_list:
            # по горизонтали
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            # по вертикали
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # если прыгаем
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0

                # если падаем
                else:
                    dy = tile[1].top - self.rect.bottom

                    self.vel_y = 0

                    self.in_air = False
                    self.sticky = False
                    self.ground = True

                    self.jump_force = 11

        # столкновение с коробками
        for box in self.game.boxes:
            # по горизонтали
            if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                push = True
                dx = box.move(dx)

            # по вертикали
            if box.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y >= 0:
                    self.vel_y = 0

                    dy = box.rect.top - self.rect.bottom

                    self.in_air = False
                    self.sticky = False
                    self.ground = True

                    self.jump_force = 11

        # столкновение с платформами
        for plat in self.game.platform_list:
            # по горизонтали
            if plat.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.sticky = False
                self.ground = True

            # по вертикали
            if plat.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # если прыгаем
                if abs((self.rect.top + dy) - plat.rect.bottom) < col_thresh:
                    dy = plat.rect.bottom - self.rect.top
                    self.vel_y = 0

                # если падаем
                elif abs((self.rect.bottom + dy) - plat.rect.top) < col_thresh:
                    self.rect.bottom = plat.rect.top - 1
                    dy = 0

                    # если персонаж никуда не идёт
                    if not self.moving_right and not self.moving_left:
                        # даём ему то же перемещение, что и у платформы
                        dx = plat.dx

                    # меняем значение флагов
                    self.in_air = False
                    self.sticky = False
                    self.ground = True

                    self.jump_force = 11

        # проверяем, стоит ли игрок на батуте
        for tramp in self.game.trampolines:
            if tramp.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = tramp.rect.top - self.rect.bottom
                self.jump_force = 18
                self.in_air = False

        # взаимодействие с аптечкой
        for heal in self.game.heals:
            if heal.rect.colliderect(self.rect) and self.health < 3:
                self.health += 1
                heal.kill()

        # столкновение с противником
        if pygame.sprite.spritecollide(self, self.game.enemies, False) and not self.invincibility:
            # уменьшаем здоровье
            self.health -= 1

            # даём неуязвимость
            self.invincibility = True
            self.invincibility_timer = 100

            # убираем флаг (чтобы не писать отпрыгивание по новой)
            self.ground = False

            # добавляем небольшое подпрыгивание
            self.vel_y = -self.jump_force // 2
            dy = self.vel_y

        # таймер неуязвимости (чтобы от врага не помереть сразу же)
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        else:
            self.invincibility = False

        # столкновение с "лавой"
        if pygame.sprite.spritecollide(self, self.game.ketchup_group, False):
            dy = 0
            self.in_air = False
            self.alive = False

        # изменение анимации
        # толкание
        if push:
            self.update_action(3)

        # ходьба
        elif self.moving_left or self.moving_right:
            self.update_action(1)

        # прыжок
        elif self.in_air:
            self.update_action(2)

        # стоит на месте
        else:
            self.update_action(0)

        # проверка на столкновение с верхней границей экрана
        if self.rect.y + dy < 0:
            self.vel_y = 0
            dy = -self.rect.top

        # перемещаем игрока
        self.rect.x += dx
        self.rect.y += dy

        # скроллинг
        if (self.rect.right > var.WIDTH - var.SCROLL_THRESH and var.bg_scroll < var.COLUMNS * var.TILE_SIZE - var.WIDTH) \
                or (self.rect.left <= var.SCROLL_THRESH and var.bg_scroll > abs(dx)):
            self.rect.x -= dx
            scroll -= dx

        return scroll
