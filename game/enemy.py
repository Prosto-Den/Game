import pygame
import variables as var
import random


# класс противника
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # загружаем картинку и создаём хитбокс
        img = pygame.image.load('img/enemy/1.png').convert_alpha()
        self.image = pygame.transform.scale(img, (var.TILE_SIZE, var.TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))

        self.start = self.rect.x
        self.radius = 3

        # здоровье противника
        self.alive = True
        self.health = 3

        # размеры противника
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # для перемещения
        self.speed = 2
        self.direction = 1

        # таймер для остановки
        self.standing_timer = 0

    def check_alive(self):
        if self.health <= 0:
            self.alive = False
            self.health = 0

    def update(self):
        if self.alive:
            self.check_alive()
            self.move()

        else:
            self.kill()

    # метод для перемещения противника
    def move(self):
        dx = 0

        # случайная остановка
        if self.direction != 0 and random.randint(1, 100) == 5:
            self.direction = 0
            self.standing_timer = 100

        # таймер
        if self.standing_timer > 0:
            self.standing_timer -= 1

        elif self.direction == 0:
            self.direction = random.choice([-1, 1])

        dx += self.speed * self.direction

        # столкновение со стенами
        for tile in self.game.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.speed * self.direction

        # столкновение с коробками
        for box in self.game.boxes:
            if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.speed * self.direction

        self.rect.x += dx

    # метод отрисовки противника
    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)
