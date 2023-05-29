import pygame
import world
import button as btn
import health_bar as bar
import variables as var


# основной игровой класс
class Game:
    def __init__(self):
        pygame.init()

        # экран
        self.screen = pygame.display.set_mode(var.RESOLUTION)
        pygame.display.set_caption('PileSOS')

        # часы. Для ограничения FPS
        self.clock = pygame.time.Clock()

        # игрок. Он появится при создании мира
        self.player = None

        # список с коробками
        self.boxes = []

        # список со стенами
        self.obstacle_list = []

        # список с платформами
        self.platform_list = []

        self.trampolines = []

        # группа с лавой
        self.ketchup_group = pygame.sprite.Group()

        # группа с противниками
        self.enemies = pygame.sprite.Group()

        self.exit_tile = None

        # игровой мир
        self.world = world.World(self)
        self.world.process_data()

        self.health_bar = bar.HealthBar(self)

        # группа с пулями
        self.bullet_group = pygame.sprite.Group()

        # группа с липкой поверхностью
        self.sticky_group = pygame.sprite.Group()

        # фон
        self.bg_img = pygame.image.load('img/background/bg.png').convert_alpha()
        self.carpet = pygame.image.load('img/background/carpet.png').convert_alpha()

        # шрифт
        self.font = pygame.font.SysFont('arial', 30)

        self.start_image = self.font.render('START', True, var.WHITE)
        self.exit_image = self.font.render('EXIT', True, var.WHITE)
        self.restart_image = self.font.render('RESTART', True, var.WHITE)

        self.start_button = btn.Button(self, var.WIDTH // 2 - 50, var.HEIGHT // 2, self.start_image)
        self.exit_button = btn.Button(self, var.WIDTH // 2 + 50, var.HEIGHT // 2, self.exit_image)
        self.restart_button = btn.Button(self, var.WIDTH // 2, var.HEIGHT // 2, self.restart_image)

        self.exit = True

    # метод для отрисовки фона
    def draw_bg(self):
        self.screen.fill(var.WHITE)

        width = self.bg_img.get_width()

        # это для параллакса
        for i in range(5):
            self.screen.blit(self.bg_img, ((i * width) - var.bg_scroll * 0.5, 0))
            self.screen.blit(self.carpet, ((i * width) - var.bg_scroll * 0.6, var.HEIGHT - self.carpet.get_height()))

        if var.restart_timer == 0:
            if self.restart_button.draw():
                self.restart()

    # метод для отрисовки сетки
    def draw_grid(self):
        x = var.WIDTH // var.TILE_SIZE
        y = var.HEIGHT // var.TILE_SIZE

        for i in range(y):
            pygame.draw.line(self.screen, var.BLACK, (0, i * var.TILE_SIZE), (var.WIDTH, i * var.TILE_SIZE), 2)

        for i in range(x):
            pygame.draw.line(self.screen, var.BLACK, (i * var.TILE_SIZE, 0), (i * var.TILE_SIZE, var.HEIGHT))

    # метод для отображения FPS
    def show_FPS(self):
        img = self.font.render(f'FPS: {self.clock.get_fps():.1f}', True, var.GREEN)
        rect = img.get_rect(topright=(var.WIDTH, 0))

        self.screen.blit(img, rect)

    # метод для отрисовки главного меню
    def main_menu(self):
        self.screen.fill(var.MENU_COLOR)

        if self.start_button.draw():
            var.main_menu = False

        elif self.exit_button.draw():
            self.exit = False

    # метод для отрисовки объектов
    def draw_objects(self):
        # отрисовываем мир
        self.world.draw()

        # отрисовываем игрока
        self.player.draw()

        # отрисовка здоровья персонажа
        self.health_bar.draw()

        # отрисовываем пули
        for bullet in self.bullet_group:
            bullet.draw()

        # отрисовываем коробки
        for box in self.boxes:
            box.draw(var.scroll)

        # отрисовываем платформы
        for plat in self.platform_list:
            plat.draw()

        # отрисовываем липкие поверхности
        for stick in self.sticky_group:
            stick.draw()

        # отрисовываем противников
        for enemy in self.enemies:
            enemy.draw()

        # отрисовываем лаву
        for lava in self.ketchup_group:
            lava.draw()

        # отрисовка батутов
        for tramp in self.trampolines:
            tramp.draw()

        if self.exit_tile is not None:
            self.exit_tile.draw()

    # обновляем объекты в мире
    def update(self):
        # обновляем игрока
        self.player.update()

        # передвигаем пули
        for bullet in self.bullet_group:
            bullet.move()

        # передвигаем платформы
        for plat in self.platform_list:
            plat.move()

        for enemy in self.enemies:
            enemy.update()

        if self.exit_tile is not None:
            self.exit_tile.exit()

    # метод для обновления экран
    def update_screen(self):
        pygame.display.flip()
        self.clock.tick(var.FPS)

    # метод для рестарта уровня
    def restart(self):
        # очищаем всё, что можно
        self.player = None
        self.boxes = []
        self.obstacle_list = []
        self.platform_list = []
        self.trampolines = []
        self.ketchup_group.empty()
        self.bullet_group.empty()
        self.enemies.empty()
        self.sticky_group.empty()
        self.exit_tile = None

        # сбрасываем переменные для скроллинга
        var.scroll = var.bg_scroll = 0

        # возвращаем значение таймера в исходное состояние
        var.restart_timer = 100

        # загружаем уровень
        self.world.process_data()

    # метод обработки событий
    def events(self):
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                self.exit = False

            if not var.main_menu:
                # обработка нажатия на клавишу
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.player.moving_right = True

                    if event.key == pygame.K_a:
                        self.player.moving_left = True

                    if event.key == pygame.K_w:
                        self.player.jump = True

                    if event.key == pygame.K_SPACE:
                        self.player.fire = True

                # обработка отпускания клавиши
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.player.moving_right = False

                    if event.key == pygame.K_a:
                        self.player.moving_left = False

                    if event.key == pygame.K_w:
                        self.player.jump = False

        return self.exit


# тут происходит вызов методов
if __name__ == '__main__':
    game = Game()

    while game.events():
        if var.main_menu:
            game.main_menu()

        else:
            game.draw_bg()

            # game.draw_grid()

            game.update()
            game.draw_objects()

            game.show_FPS()

        game.update_screen()
