import pygame
import variables as var
import sticky

massive = [0] * 12


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()

        self.game = game

        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect(center = (x, y))

        self.speed = 800
        self.vel_y = -300
        self.gravity = 5
        self.direction = direction
        self.slide_timer = 0
        self.counted = False
        self.sticky_created = False

    def update(self, dt):
        dx = dy = 0
        stop = False

        dx = self.speed * self.direction * dt

        self.vel_y += self.gravity
        if self.vel_y >= 800:
            self.vel_y = 800

        dy = self.vel_y * dt

        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom

        if self.rect.bottom == 600:
            dx = 0

        if self.rect.right + dx >= 800:
            dx = 800 - self.rect.right

            dy = 1

            if self.slide_timer < 25:
                self.slide_timer += 1
            else:
                dy = 0

                y = self.rect.y // var.TILE_SIZE

                if massive[y] < 3 and not self.counted:
                    self.counted = True
                    massive[y] += 1

                if massive[y] == 3:
                    if not self.sticky_created:
                        stick = sticky.Sticky(self.game,
                                              self.rect.x // var.TILE_SIZE * var.TILE_SIZE + var.TILE_SIZE * 0.9 * self.direction,
                                              y * var.TILE_SIZE)
                        self.game.sticky_group.add(stick)
                        self.sticky_created = True

                    self.kill()

        if self.rect.left + dx <= 200:
            dx = 200 - self.rect.left

            dy = 1

            if self.slide_timer < 25:
                self.slide_timer += 1
            else:
                dy = 0

                y = self.rect.y // var.TILE_SIZE

                if massive[y] < 3 and not self.counted:
                    self.counted = True
                    massive[y] += 1

                if massive[y] == 3:
                    if not self.sticky_created:
                        stick = sticky.Sticky(self.game,
                                              self.rect.x // var.TILE_SIZE * var.TILE_SIZE + var.TILE_SIZE * 0.9 * self.direction,
                                              y * var.TILE_SIZE)
                        self.game.sticky_group.add(stick)
                        self.sticky_created = True

                    self.kill()

        self.rect.x += dx
        self.rect.y += dy
