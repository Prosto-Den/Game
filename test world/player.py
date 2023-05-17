import pygame
import bullet
import variables as var


class Player:
    def __init__(self, game, x, y):
        self.game = game

        self.image = pygame.Surface((50, 50))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x, y))

        self.speed = 450
        self.direction = 1

        self.gravity = 15
        self.vel_y = 0
        self.in_air = True

        self.can_fire = True

        self.timer = 0
        self.jump = False

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        pass

    def move(self, dt):
        dx = dy = 0
        scroll = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            dx += self.speed * dt
            self.direction = 1

        elif keys[pygame.K_a]:
            dx -= self.speed * dt
            self.direction = -1

        if keys[pygame.K_w] and not self.in_air:
            self.vel_y = -500
            self.in_air = True
            self.jump = False

        if keys[pygame.K_SPACE] and self.can_fire:
            blt = bullet.Bullet(self.game, self.rect.centerx + 0.7 * self.rect.width * self.direction, self.rect.y, self.direction)
            self.game.bullet_group.add(blt)

            self.can_fire = False

        if not keys[pygame.K_SPACE]:
            self.can_fire = True

        self.vel_y += self.gravity
        if self.vel_y >= 800:
            self.vel_y = 800

        dy = self.vel_y * dt

        for tile in self.game.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.image.get_width(), self.image.get_height()):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                if self.vel_y < 0:
                    self.vel_y = 0

                    dy = tile[1].bottom - self.rect.top

                else:
                    self.vel_y = 0
                    self.in_air = False

                    dy = tile[1].top - self.rect.bottom

        if pygame.sprite.spritecollide(self, self.game.sticky_group, False):
            if self.timer == 0:
                dy = 0

            if keys[pygame.K_w]:
                self.timer = 35
                self.vel_y = -500

        if self.timer > 0:
            self.timer -= 1

        self.rect.x += dx
        self.rect.y += dy

        return scroll
