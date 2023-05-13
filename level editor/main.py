import pygame
import variables as var
import button as btn
import pickle

pygame.init()

# данные по миру
world_data = []

for row in range(var.ROWS):
    r = [-1] * var.COLUMNS
    world_data.append(r)

# экран редактора уровней
screen = pygame.display.set_mode(var.RESOLUTION)
pygame.display.set_caption('Level editor')

# шрифт
font = pygame.font.SysFont('arial', 30)

# для стабильного FPS
clock = pygame.time.Clock()

# картинки
ground_img = pygame.Surface((var.TILE_SIZE, var.TILE_SIZE))
ground1_img = pygame.Surface((var.TILE_SIZE, var.TILE_SIZE))
ground1_img.fill((184, 151, 94))

save_img = font.render('SAVE', True, var.WHITE)
load_img = font.render('LOAD', True, var.WHITE)
clear_img = font.render('CLEAR', True, var.WHITE)

img_tiles = [ground_img, ground1_img]

# кнопки
ground_btn = btn.Button(ground_img, var.WIDTH + 10, 10)
ground1_btn = btn.Button(ground1_img, var.WIDTH + 70, 10)

save_btn = btn.Button(save_img, 500, var.HEIGHT)
load_btn = btn.Button(load_img, 600, var.HEIGHT)
clear_btn = btn.Button(clear_img, 550, var.HEIGHT + 50)

btn_list = [ground_btn, ground1_btn]


def draw_grid():
    for x in range(var.COLUMNS):
        pygame.draw.line(screen, var.BLACK, (x * var.TILE_SIZE - var.scroll, 0),
                         (x * var.TILE_SIZE - var.scroll, var.HEIGHT), 2)

    for y in range(var.ROWS):
        pygame.draw.line(screen, var.BLACK, (0, y * var.TILE_SIZE), (var.WIDTH, y * var.TILE_SIZE))


# рисуем мир на экране
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_tiles[tile], (x * var.TILE_SIZE - var.scroll, y * var.TILE_SIZE))


# рисуем текст
def draw_text(text, x, y, color):
    img = font.render(text, True, color)
    rect = img.get_rect(topleft=(x, y))

    screen.blit(img, rect)


# основной цикл
run = True
while run:
    # обработчик событий
    for event in pygame.event.get():
        # выход из редактора
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
            break

        # нажатие клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                var.scroll_right = True

            if event.key == pygame.K_a:
                var.scroll_left = True

            if event.key == pygame.K_LSHIFT:
                var.scroll_speed = 10

            if event.key == pygame.K_w:
                var.level += 1

            if event.key == pygame.K_s and var.level > 0:
                var.level -= 1

        # отпускание клавиши
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                var.scroll_right = False

            if event.key == pygame.K_a:
                var.scroll_left = False

            if event.key == pygame.K_LSHIFT:
                var.scroll_speed = 5

    # выход их основного цикла
    if not run:
        break

    # скроллинг мира
    if var.scroll_left and var.scroll > 0:
        var.scroll -= var.scroll_speed

    if var.scroll_right and var.scroll < var.COLUMNS * var.TILE_SIZE - var.WIDTH:
        var.scroll += var.scroll_speed

    pos = pygame.mouse.get_pos()
    x = (pos[0] + var.scroll) // var.TILE_SIZE
    y = pos[1] // var.TILE_SIZE

    if pos[0] < var.WIDTH and pos[1] < var.HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != var.current_tile:
                world_data[y][x] = var.current_tile

        if pygame.mouse.get_pressed()[2]:
            if world_data[y][x] != -1:
                world_data[y][x] = -1

    # рисуем задний фон
    screen.fill(var.WHITE)

    # рисуем сетку
    draw_grid()

    draw_world()

    # отрисовка фона меню
    pygame.draw.rect(screen, var.MENU_COLOR, (var.WIDTH, 0, var.RIGHT_MARGIN, var.HEIGHT + var.BOTTOM_MARGIN))
    pygame.draw.rect(screen, var.MENU_COLOR, (0, var.HEIGHT, var.WIDTH, var.BOTTOM_MARGIN))

    # отрисовка кнопок и обработка на их нажатие
    for var.btn_count, i in enumerate(btn_list):
        if i.draw(screen):
            var.current_tile = var.btn_count

    # сохраняем уровень
    if save_btn.draw(screen):
        pickle_out = open(f'created levels/level_data_{var.level}', 'wb')

        pickle.dump(world_data, pickle_out)

        pickle_out.close()

    # загружаем уровень
    if load_btn.draw(screen):
        # ловим ошибку
        try:
            # открываем файл
            pickle_in = open(f'created levels/level_data_{var.level}', 'rb')

            # считываем данные уровня
            world_data = pickle.load(pickle_in)

            # закрываем файл
            pickle_in.close()

        # если такого файла нет
        except FileNotFoundError:
            var.timer_error = 150

    # очищаем поле
    if clear_btn.draw(screen):
        for i in range(var.ROWS):
            for j in range(var.COLUMNS):
                world_data[i][j] = -1

    # отображаем номер уровня, в котором сейчас работаем
    draw_text(f'Level: {var.level}', 0, var.HEIGHT, var.WHITE)

    # отображаем сообщение об ошибке, если не удалось открыть файл
    if var.timer_error > 0:
        draw_text('There is not such file', 700, var.HEIGHT + 25, var.RED)

        var.timer_error -= 1

    # выделяем выбранную кнопку
    pygame.draw.rect(screen, var.WHITE, btn_list[var.current_tile], 3)

    # обновление экрана
    pygame.display.flip()
    clock.tick(var.FPS)
