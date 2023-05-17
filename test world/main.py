import pygame
import player
import world
from time import time
import variables as var


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(var.RESOLUTION)
        pygame.display.set_caption('Test world')

        self.clock = pygame.time.Clock()
        self.last_time = time()

        self.player = None

        self.obstacle_list = []

        self.sticky_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.world = world.World(self)
        self.world.proceed_data()

    def draw_bg(self):
        self.screen.fill(var.WHITE)

    def draw_grid(self):
        for x in range(var.COLUMNS):
            pygame.draw.line(self.screen, var.BLACK, (x * var.TILE_SIZE, 0), (x * var.TILE_SIZE, var.HEIGHT), 2)

        for y in range(var.ROWS):
            pygame.draw.line(self.screen, var.BLACK, (0, y * var.TILE_SIZE), (var.WIDTH, y * var.TILE_SIZE), 2)

    def draw_objects(self):
        for sticky in self.sticky_group:
            sticky.draw()

        self.world.draw()

        self.player.draw()

        self.bullet_group.draw(self.screen)

    def update_objects(self):
        dt = time() - self.last_time
        self.last_time = time()

        var.scroll = self.player.move(dt)

        self.bullet_group.update(dt)

    def update_screen(self):
        pygame.display.flip()

        self.clock.tick(var.FPS)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return False

        return True


if __name__ == '__main__':
    game = Game()

    while game.check_event():

        game.draw_bg()

        game.draw_grid()

        game.update_objects()
        game.draw_objects()

        game.update_screen()
