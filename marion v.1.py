import pygame
import os
import sys


pygame.init()
size = width, height = (550, 550)
screen = pygame.display.set_mode(size)
fps = 50
clock = pygame.time.Clock()
running = True
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player = None


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit(0)


def start_screen():
    # level_name = input('Введите название уровня (1, 2, 3): ') + '.txt'
    # if not level_name in os.listdir('data'):
    #     print('Уровень не найден. Будет загружен уровень № 1.')
    #     level_name = '1.txt'

    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return #  level_name  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def load_level(filename):
    filename = 'data/' + filename

    with open(filename, 'r') as mapFile:
        level_map = [s.strip() for s in mapFile]
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level)):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y

# classes

tile_images = {'wall': pygame.transform.scale(load_image('gay.png'), (50, 50)), 'empty': load_image('grass.png')}
player_image = load_image('mario.png', -1)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.v = 15
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def go_left(self):
        self.rect = self.rect.move(-self.v, 0)

    def go_up(self):
        self.rect = self.rect.move(0, -self.v)

    def go_right(self):
        self.rect = self.rect.move(self.v, 0)

    def go_down(self):
        self.rect = self.rect.move(0, self.v)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

    # позиционировать камеру на объекте target
    # def update(self, target):
    #     self.dx = -(target.rect.x - self.curx)
    #     self.dy = -(target.rect.y - self.cury)
    #     self.curx = target.rect.x
    #     self.cury = target.rect.y

#

level_name = start_screen()
camera = Camera()
player, level_x, level_y = generate_level(load_level('map.txt'))
camera.update(Tile(''))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_UP:
                player.go_up()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_DOWN:
                player.go_down()


    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()