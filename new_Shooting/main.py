import pygame
import variables as var
from time import time
import player


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(var.RESOLUTION)
        pygame.display.set_caption('Test')

        self.clock = pygame.time.Clock()
        self.last_time = time()

        self.bullet_group = pygame.sprite.Group()
        self.sticky_group = pygame.sprite.Group()

    def draw_screen(self):
        self.screen.fill(var.WHITE)
        pygame.draw.line(self.screen, var.RED, (0, 600), (var.WIDTH, 600), 2)
        pygame.draw.line(self.screen, var.RED, (800, 0), (800, 600), 2)
        pygame.draw.line(self.screen, var.RED, (200, 0), (200, 600), 2)

    def draw_grid(self):
        x, y = var.WIDTH // var.TILE_SIZE, int(var.HEIGHT / var.TILE_SIZE)

        for i in range(x):
            pygame.draw.line(self.screen, var.BLACK, (i * var.TILE_SIZE, 0), (i * var.TILE_SIZE, var.HEIGHT))

        for i in range(y):
            pygame.draw.line(self.screen, var.BLACK, (0, i * var.TILE_SIZE), (var.WIDTH, i * var.TILE_SIZE))

        #pos = pygame.mouse.get_pos()
        #print(pos[0] // var.TILE_SIZE, pos[1] // var.TILE_SIZE)

    def update_screen(self):
        self.clock.tick(var.FPS)
        pygame.display.flip()

    def draw_objects(self):
        self.bullet_group.draw(self.screen)
        self.sticky_group.draw(self.screen)

    def update_objects(self, dt):
        self.bullet_group.update(dt)

    def update_time(self):
        delta = time() - self.last_time
        self.last_time = time()

        return delta


if __name__ == '__main__':
    game = Game()
    player = player.Player(game, 500, 300)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
        if not run:
            pygame.quit()
            break

        dt = game.update_time()

        game.draw_screen()
        game.draw_grid()

        game.draw_objects()
        game.update_objects(dt)

        player.draw()
        player.move(dt)

        game.update_screen()
