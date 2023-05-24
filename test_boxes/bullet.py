import pygame
import variables as var
import sticky

sticky_list = []

for i in range(var.ROWS):
    r = [0] * var.COLUMNS

    sticky_list.append(r)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        super().__init__()
        self.game = game

        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect(center = (x, y))

        self.speed = 6
        self.vel_y = -3
        self.gravity = 0.1
        self.direction = direction

        self.slide_timer = 0
        self.counted = False

    def move(self):
        dx = dy = 0

        dx = self.speed * self.direction

        self.vel_y += self.gravity

        if self.vel_y >= 10:
            self.vel_y = 10

        dy += self.vel_y

        for ground in self.game.obstacle_list:
            if ground[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                dy = ground[1].top - self.rect.bottom
                dx = 0

            if ground[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                if dx > 0:
                    dx = ground[1].left - self.rect.right

                elif dx < 0:
                    dx = ground[1].right - self.rect.left

                dy = 1

                if self.slide_timer < 25:
                    self.slide_timer += 1

                else:
                    dy = 0

                    x = ground[1].x // var.TILE_SIZE
                    y = ground[1].y // var.TILE_SIZE

                    if sticky_list[y][x] < 3 and not self.counted:
                        sticky_list[y][x] += 1
                        self.counted = True

                    elif sticky_list[y][x] == 3:
                        coord_x = ground[1].x - 0.2 * var.TILE_SIZE * self.direction
                        coord_y = ground[1].y

                        stick = sticky.Sticky(self.game, coord_x, coord_y, self.direction)

                        self.game.sticky_group.add(stick)

                        self.kill()

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        self.rect.x += var.scroll

        self.game.screen.blit(self.image, self.rect)