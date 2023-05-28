import pygame


# класс показателя здоровья
class HealthBar:
    def __init__(self, game):
        self.game = game

        # узнаём, сколько здоровья есть у персонажа
        self.health = self.game.player.health

        # шкала здоровья
        self.bar = []

        # шкала с кол-вом оставшегося у игрока здоровья
        self.hp = []

        # картинки
        heart = pygame.image.load('img/hp/heart.png').convert_alpha()
        dead_heart = pygame.image.load('img/hp/dead_heart.png').convert_alpha()

        # заполняем шкалы
        step = 0
        for i in range(self.health):
            tile_bar = (dead_heart, dead_heart.get_rect(topleft = (step, 0)))
            tile_hp = (heart, heart.get_rect(topleft = (step, 0)))

            self.bar.append(tile_bar)
            self.hp.append(tile_hp)

            step += 55

    # обновляем информацию по количеству здоровья
    def update_health(self):
        self.health = self.game.player.health

    # отрисовываем шкалу здоровья на экране
    def draw(self):
        self.update_health()

        for tile in self.bar:
            self.game.screen.blit(tile[0], tile[1])

        for hp in range(self.health):
            self.game.screen.blit(self.hp[hp][0], self.hp[hp][1])
