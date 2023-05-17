import pygame
import variables as var
import sticky

massive = []

for i in range(var.ROWS):
    r = [0] * var.COLUMNS

    massive.append(r)

print(massive)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()

        self.game = game

        self.image = pygame.Surface((10, 10))
        self.image.fill(var.RED)
        self.rect = self.image.get_rect(center = (x, y))

        self.speed = 400
        self.vel_y = -200
        self.gravity = 5
        self.direction = direction

        self.slide_timer = 0
        self.counted = False
        self.sticky_created = False
        self.on_wall = False

    def update(self, dt):
        dx = dy = 0
        stop = False

        dx = self.speed * self.direction * dt

        self.vel_y += self.gravity
        if self.vel_y >= 800:
            self.vel_y = 800

        dy = self.vel_y * dt

        for tile in self.game.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                self.speed = 0

                if self.vel_y > 0:
                    self.vel_y = 0

                    dy = tile[1].top - self.rect.bottom

                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top

            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                if dx > 0:
                    dx = tile[1].left - self.rect.right

                elif dx < 0:
                    dx = tile[1].right - self.rect.left

                dy = 1

                if self.slide_timer < 25:
                    self.slide_timer += 1
                else:
                    dy = 0

                    x = self.rect.x // var.TILE_SIZE
                    y = self.rect.y // var.TILE_SIZE

                    if massive[y][x] < 3 and not self.counted:
                        self.counted = True
                        massive[y][x] += 1

                    if massive[y][x] == 3:
                        if not self.sticky_created:
                            sticky_x = x * var.TILE_SIZE + var.TILE_SIZE * self.direction * 0.9
                            sticky_y = y * var.TILE_SIZE

                            stick = sticky.Sticky(self.game, sticky_x, sticky_y)
                            self.game.sticky_group.add(stick)

                            self.sticky_created = True

                        self.kill()

        self.rect.x += dx
        self.rect.y += dy
