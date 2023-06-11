import pygame
import block
import variables as var


class Press:
    def __init__(self, game, x, y):
        self.game = game

        self.image = pygame.Surface((var.TILE_SIZE, var.TILE_SIZE))
        self.rect = self.image.get_rect(topleft = (x, y))

        self.blocks = []

        self.speed = 5
        self.direction = 1
        self.stop_timer = 50

    def draw(self):
        self.rect.x += var.scroll

        for blk in self.blocks:
            blk.rect.x += var.scroll
            self.game.screen.blit(blk.image, blk.rect)

        self.game.screen.blit(self.image, self.rect)

    def update(self):
        if len(self.blocks) == 0 and self.stop_timer == 0:
            blk = block.Block(self.rect.x, self.rect.y)
            self.blocks.append(blk)
            self.direction = 1
            self.speed = 5

        elif self.stop_timer == 0:
            dy = self.speed * self.direction
            main_blk = self.blocks[0]

            for tile in self.game.obstacle_list:
                if tile[1].colliderect(main_blk.rect.x, main_blk.rect.y + dy, main_blk.width, main_blk.height):
                    dy = tile[1].top - main_blk.rect.bottom
                    self.direction *= -1
                    self.speed //= 2

            for box in self.game.boxes:
                if box.rect.colliderect(main_blk.rect.x, main_blk.rect.y + dy, main_blk.width, main_blk.height):
                    dy = box.rect.top - main_blk.rect.bottom
                    self.direction *= -1

            for plat in self.game.platform_list:
                if plat.rect.colliderect(main_blk.rect.x, main_blk.rect.y + dy, main_blk.width, main_blk.height):
                    dy = plat.rect.top - main_blk.rect.bottom
                    self.direction *= -1

            for lava in self.game.ketchup_group:
                if lava.rect.colliderect(main_blk.rect.x, main_blk.rect.y + dy, main_blk.width, main_blk.height):
                    dy = lava.rect.top - main_blk.rect.bottom
                    self.direction *= -1

            if self.blocks[-1].rect.y >= self.rect.bottom:
                blk = block.Block(self.rect.x, self.rect.y)
                self.blocks.append(blk)

            if self.blocks[-1].rect.y <= self.rect.y and self.direction == -1:
                self.blocks.pop(-1)

            if len(self.blocks) == 0:
                self.stop_timer = 50

            for blk in self.blocks:
                blk.move(dy)

        if self.stop_timer > 0:
            self.stop_timer -= 1
