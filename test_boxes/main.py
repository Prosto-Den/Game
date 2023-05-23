import pygame
import world
import variables as var


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(var.RESOLUTION)
        pygame.display.set_caption('Test')

        self.clock = pygame.time.Clock()

        self.player = None

        self.boxes = []
        self.obstacle_list = []

        self.world = world.World(self)

        self.font = pygame.font.SysFont('arial', 30)

    def draw_bg(self):
        self.screen.fill(var.WHITE)

    def draw_grid(self):
        x = var.WIDTH // var.TILE_SIZE
        y = var.HEIGHT // var.TILE_SIZE

        for i in range(y):
            pygame.draw.line(self.screen, var.BLACK, (0, i * var.TILE_SIZE), (var.WIDTH, i * var.TILE_SIZE), 2)

        for i in range(x):
            pygame.draw.line(self.screen, var.BLACK, (i * var.TILE_SIZE, 0), (i * var.TILE_SIZE, var.HEIGHT))

    def show_FPS(self):
        img = self.font.render(f'FPS: {self.clock.get_fps():.1f}', True, var.GREEN)
        rect = img.get_rect(topleft=(0, 0))

        self.screen.blit(img, rect)

    def draw_objects(self):
        self.world.draw()

        self.player.draw()

        for box in self.boxes:
            box.draw(var.scroll)

    def update(self):
        var.scroll = self.player.move()

    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(var.FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.moving_right = True

                if event.key == pygame.K_a:
                    self.player.moving_left = True

                if event.key == pygame.K_w:
                    self.player.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.player.moving_right = False

                if event.key == pygame.K_a:
                    self.player.moving_left = False

                if event.key == pygame.K_w:
                    self.player.jump = False

        return True


if __name__ == '__main__':
    game = Game()

    while game.events():
        game.draw_bg()

        game.draw_grid()

        game.update()
        game.draw_objects()

        game.show_FPS()

        game.update_screen()
