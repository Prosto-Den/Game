import pygame
import button as btn
import variables as var

pygame.init()

screen = pygame.display.set_mode(var.RESOLUTION)
pygame.display.set_caption('Level Editor')

ground = btn.Button(screen, var.WIDTH + 10, 10)

btn_list = [ground]


def draw_grid() -> None:
    columns: int = var.WIDTH // var.TILE_SIZE
    rows: int = var.HEIGHT // var.TILE_SIZE

    for x in range(columns):
        pygame.draw.line(screen, var.BLACK, (x * var.TILE_SIZE + var.scroll, 0), (x * var.TILE_SIZE + var.scroll, var.HEIGHT), 2)

    for y in range(rows):
        pygame.draw.line(screen, var.BLACK, (0 + var.scroll, y * var.TILE_SIZE), (var.WIDTH + var.scroll, y * var.TILE_SIZE), 2)


clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                var.scroll_left = True

            if event.key == pygame.K_a:
                var.scroll_right = True

            if event.key == pygame.K_LSHIFT:
                var.increase_scroll_speed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                var.scroll_left = False

            if event.key == pygame.K_a:
                var.scroll_right = False

            if event.key == pygame.K_LSHIFT:
                var.increase_scroll_speed = False

    if not run:
        pygame.quit()
        break

    if var.increase_scroll_speed:
        var.scroll_speed = 10
    else:
        var.scroll_speed = 5

    if var.scroll_right:
        var.scroll += var.scroll_speed

    if var.scroll_left:
        var.scroll -= var.scroll_speed

    screen.fill('white')

    draw_grid()

    pygame.draw.rect(screen, var.MENU_COLOR, (var.WIDTH, 0, var.RIGHT_MARGIN, var.HEIGHT + var.BOTTOM_MARGIN))
    pygame.draw.rect(screen, var.MENU_COLOR, (0, var.HEIGHT, var.WIDTH + var.RIGHT_MARGIN, var.BOTTOM_MARGIN))

    for var.current_btn, i in enumerate(btn_list):
        if i.draw(screen):
            var.chosen_btn = var.current_btn

    pygame.draw.rect(screen, var.WHITE, btn_list[var.chosen_btn], 3)

    pygame.display.update()
    clock.tick(var.FPS)
