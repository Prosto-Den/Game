import pygame
import variables as var
import sticky

# массив для хранения липучих блоков
sticky_list = []

for i in range(var.ROWS):
    r = [0] * var.COLUMNS

    sticky_list.append(r)


# класс пульки
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()
        self.game = game

        # загружаем картинку
        img = pygame.image.load('img/bullet/1.png').convert_alpha()

        # создаём текстурку и хитбокс
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect(center = (x, y))

        # параметры для движения пули
        self.speed = 8
        self.vel_y = -3
        self.gravity = 0.3
        self.direction = direction

        # переменные для создания липкого блока
        self.slide_timer = 0
        self.counted = False
        self.stop = False

        # флаги для проверки, на стене пулька или на платформе
        self.on_wall = False
        self.on_platform = False

        # таймер время жизни пульки
        self.life_timer = 1000

    # обновляем положение пули
    def move(self):
        # переменные для передвижения
        dx = dy = 0
        x = y = 0

        """Рассчитываем перемещение по горизонтали"""
        dx = self.speed * self.direction

        # добавляем гравитацию
        self.vel_y += self.gravity

        # ограничиваем скорость падения
        if self.vel_y >= 10:
            self.vel_y = 10

        """Рассчитываем перемещение по вертикали"""
        dy += self.vel_y

        # столкновение со стенами
        for ground in self.game.obstacle_list:
            # тут просто останавливаем пулю, если она упала на землю или ударилась об потолок
            if ground[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                dx = 0

                if self.vel_y < 0:
                    """Меняем перемещение по вертикали"""
                    dy = ground[1].bottom - self.rect.top
                    # обнуляем вертикальную скорость
                    self.vel_y = 0

                if self.vel_y > 0:
                    """Меняем перемещение по вертикали"""
                    dy = ground[1].top - self.rect.bottom
                    """Не перемещаем пулю по горизонтали"""

                    # начинаем обратный отсчёт времени жизни пульки
                    self.life_timer -= 1

            # если же произошло столкновение по горизонтали, то тут всё интересней
            if ground[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                self.on_wall = True

                """Уменьшаем скорость по вертикали"""
                dy = 1

                # таймер до остановки
                if self.slide_timer < 25:
                    self.slide_timer += 1

                # как только время вышло
                else:
                    """Останавливаем пулю"""
                    dy = 0
                    self.stop = True
                    x = ground[1].x
                    y = ground[1].y

        # проверка на столкновение с коробками
        for box in self.game.boxes:
            # столкновение по вертикали
            if box.rect.colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                """Останавливаем пулю по горизонтали"""
                dx = 0

                # если падаем на коробку
                if self.vel_y > 0:
                    """Перерасчитываем перемещение по вертикали"""
                    dy = box.rect.top - self.rect.bottom

                    # начинаем обратный отчёт времени жизни
                    self.life_timer -= 1

            # столкновение по горизонтали
            if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                """Перерасчёт передвижения по горизонтали"""
                if dx > 0:
                    dx = box.rect.left - self.rect.right

                elif dx < 0:
                    dx = box.rect.right - self.rect.left

        # столкновение с платформой
        for plat in self.game.platform_list:
            # по вертикали
            if plat.rect.colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                dx = plat.dx

                # если сталкивается снизу
                if self.vel_y < 0:
                    self.vel_y = 0

                    """Перерасчитываем перемещение по вертикали"""
                    dy = plat.rect.bottom - self.rect.top

                # если падает сверху
                elif self.vel_y > 0:
                    """Перерасчитываем все перемещения"""
                    dy = plat.rect.top - self.rect.bottom
                    # начинаем обратный отчёт
                    self.life_timer -= 1

            # столкновение по горизонтали
            if plat.rect.colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                self.on_wall = True

        # если столкнулся со стенкой
        if self.on_wall:
            """Обнуляем перемещение по горизонтали"""
            dx = 0

        # обновляем координаты пули
        self.rect.x += dx
        self.rect.y += dy

        if self.stop:
            # получаем координаты блока, на котором она остановилась
            tile_x = x // var.TILE_SIZE
            tile_y = y // var.TILE_SIZE

            # прибавляем значение к счётчику пуль
            if sticky_list[tile_y][tile_x] < 3 and not self.counted:
                sticky_list[tile_y][tile_x] += 1
                self.counted = True

            # если на блоке уже 3 пульки
            elif sticky_list[tile_y][tile_x] == 3:
                # нужен для проверки создания блока
                stick_created = False

                # считаем координаты липкого блока
                coord_x = x - 0.2 * var.TILE_SIZE * self.direction
                coord_y = y

                # проверяем, не создан ли уже на этом месте блок
                for stick in self.game.sticky_group:
                    if stick.rect.topleft == (coord_x, coord_y):
                        stick_created = True
                        break

                # если не создан
                if not stick_created:
                    # создаём липкий блок
                    stick = sticky.Sticky(self.game, coord_x, coord_y, self.direction)

                    # добавляем его в группу
                    self.game.sticky_group.add(stick)

                # уничтожаем пульку
                self.kill()

        # если таймер времени жизни упал до 0
        if self.life_timer == 0:
            # уничтожаем объект
            self.kill()

    # рисуем пулю
    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)
