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
pygame.display.set_icon(pygame.image.load('img/icon.png'))

# шрифт
font = pygame.font.SysFont('arial', 30)

# для стабильного FPS
clock = pygame.time.Clock()

# картинки
img_tiles = []

for i in range(1, var.TILE_TYPES + 1):
    img = pygame.image.load(f'img/tiles/tile{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (50, 50))

    img_tiles.append(img)

press = pygame.Surface((50, 50))

img_tiles.append(press)

save_img = font.render('SAVE', True, var.WHITE)
load_img = font.render('LOAD', True, var.WHITE)
clear_img = font.render('CLEAR', True, var.WHITE)

yes_img = font.render('YES', True, var.WHITE)
no_img = font.render('NO', True, var.WHITE)

# кнопки
save_btn = btn.Button(save_img, 500, var.HEIGHT)
load_btn = btn.Button(load_img, 600, var.HEIGHT)
clear_btn = btn.Button(clear_img, 550, var.HEIGHT + 50)
yes_btn = btn.Button(yes_img, 420, 440)
no_btn = btn.Button(no_img, 570, 440)


btn_list = []

for i in range(var.TILE_TYPES + 1):
    btn_list.append(btn.Button(img_tiles[i], var.WIDTH + (75 * var.btn_col) + 25, 75 * var.btn_row + 25, 'tile'))

    var.btn_col += 1

    if var.btn_col == 3:
        var.btn_row += 1
        var.btn_col = 0

bg_img = pygame.image.load('img/background/bg.png').convert_alpha()
carpet = pygame.image.load('img/background/carpet.png').convert_alpha()


# рисуем задний фон
def draw_bg():
    width = bg_img.get_width()

    for i in range(5):
        screen.blit(bg_img, ((i * width) - var.scroll * 0.5, 0))
        screen.blit(carpet, ((i * width) - var.scroll * 0.6, var.HEIGHT - carpet.get_height()))


# рисуем сетку
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
def draw_text(text: str, x: int, y: int, color: tuple):
    img = font.render(text, True, color)
    rect = img.get_rect(topleft=(x, y))

    screen.blit(img, rect)


# функция на проверку наличия игрока на поле
def check_for_player():
    for row in world_data:
        for tile in row:
            if tile == 6:
                return True

    return False


def save():
    pickle_out = open(f'created levels/level_data_{var.level}', 'wb')

    pickle.dump(world_data, pickle_out)

    pickle_out.close()

    var.timer_save = 250


def load(file):
    global world_data

    world_data = pickle.load(file)

    file.close()

    var.player_created = check_for_player()


# основной цикл
run = True

while run:
    # обработчик событий
    for event in pygame.event.get():
        # выход из редактора
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            var.exit_menu = True
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

    # скроллинг мира
    if var.scroll_left and var.scroll > 0:
        var.scroll -= var.scroll_speed
    if var.scroll_right and var.scroll < var.COLUMNS * var.TILE_SIZE - var.WIDTH:
        var.scroll += var.scroll_speed

    # получаем координаты курсора
    pos = pygame.mouse.get_pos()
    x = (pos[0] + var.scroll) // var.TILE_SIZE
    y = pos[1] // var.TILE_SIZE

    # проверяем, находится ли курсор на поле
    if (pos[0] < var.WIDTH and pos[1] < var.HEIGHT) and var.can_place:
        # создаём блок при нажатии ЛКМ
        if pygame.mouse.get_pressed()[0]:
            # если в клетку помещаем блок, отличный от находящегося там
            if world_data[y][x] != var.current_tile:
                # меняем значение в массиве
                world_data[y][x] = var.current_tile

                # если ставиться игрок, но игрок уже есть на поле
                if var.current_tile == 6 and var.player_created:
                    world_data[y][x] = -1

                # проверяем, есть ли игрок на поле
                var.player_created = check_for_player()

        # удаление блока с поля при нажании ПКМ
        if pygame.mouse.get_pressed()[2]:
            var.player_created = check_for_player()
            if world_data[y][x] != -1:
                world_data[y][x] = -1

    if var.can_place_timer > 0:
        var.can_place_timer -= 1

    else:
        var.can_place = True

    # рисуем задний фон
    screen.fill(var.WHITE)
    draw_bg()

    # рисуем сетку
    draw_grid()

    # рисуем мир на поле
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
        var.save_menu = True

    # загружаем уровень
    if load_btn.draw(screen):
        try:
            pickle_in = open(f'created levels/level_data_{var.level}', 'rb')
            var.load_menu = True

        except FileNotFoundError:
            var.timer_error = 150

    # очищаем поле
    if clear_btn.draw(screen):
        for i in range(var.ROWS):
            for j in range(var.COLUMNS):
                world_data[i][j] = -1

        var.player_created = check_for_player()

    # отображаем номер уровня, в котором сейчас работаем
    draw_text(f'Level: {var.level}', 0, var.HEIGHT, var.WHITE)

    # отображаем сообщение об ошибке, если не удалось открыть файл
    if var.timer_error > 0:
        draw_text('There is not such file', 700, var.HEIGHT + 25, var.RED)

        var.timer_error -= 1

    # ссообщение о том, что уровень был успешно сохранён
    if var.timer_save > 0:
        draw_text('Level has been successfully saved', 700, var.HEIGHT + 25, var.GREEN)

        var.timer_save -= 1

    # окно выхода из редактора
    if var.exit_menu:
        # закрываем окно сохранения и загрузки уровня
        if var.save_menu:
            var.save_menu = False

        elif var.load_menu:
            var.load_menu = False

        # забираем возможность размещать блоки
        var.can_place = False

        # рисуем окно
        pygame.draw.rect(screen, var.MENU_COLOR, (250, 300, 500, 200))

        # текст
        draw_text('Are you sure you want to exit?', 340, 320, var.WHITE)
        draw_text('All unsaved changes wil be lost!', 330, 349, var.WHITE)

        # если нажата кнопка да, закрываем редактор
        if yes_btn.draw(screen):
            pygame.quit()
            run = False
            break

        # если нажата кнопка нет, закрываем окно выхода из редактора
        elif no_btn.draw(screen):
            var.exit_menu = False
            var.can_place_timer = 50

    # окно сохранения уровня
    if var.save_menu:
        var.can_place = False

        pygame.draw.rect(screen, var.MENU_COLOR, (250, 300, 500, 200))

        draw_text(f'Save as level {var.level}?', 420, 320, var.WHITE)

        if yes_btn.draw(screen):
            save()
            var.save_menu = False
            var.can_place_timer = 50

        elif no_btn.draw(screen):
            var.save_menu = False
            var.can_place_timer = 50

    # окно загрузки уровня
    elif var.load_menu:
        var.can_place = False

        pygame.draw.rect(screen, var.MENU_COLOR, (250, 300, 500, 200))

        draw_text(f'Load level {var.level}?', 420, 320, var.WHITE)
        draw_text('All unsaved changes would be lost!', 300, 360, var.WHITE)

        if yes_btn.draw(screen):
            load(pickle_in)
            var.load_menu = False
            var.can_place_timer = 50

        elif no_btn.draw(screen):
            var.load_menu = False
            var.can_place_timer = 50

    # выделяем выбранную кнопку
    pygame.draw.rect(screen, var.WHITE, btn_list[var.current_tile], 3)

    # обновление экрана
    pygame.display.flip()
    clock.tick(var.FPS)
