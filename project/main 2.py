import pygame
import os
import random
import sys

# init
pygame.init()

# options
size = width, height = (750, 750)
screen = pygame.display.set_mode(size)
fps = 50
tile_width = tile_height = 75
clock = pygame.time.Clock()



# groups
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


# funcs

# load img
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


# terminate
def terminate():
    pygame.quit()
    sys.exit()


# load level
def load_level(filename):

    filename = 'data/' + filename

    with open(filename, 'r') as mapFile:
        level_map = [s.strip() for s in mapFile]
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# generate level
def generate_level(level):

    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level)):
            if level[y][x] == '.':
                Tile(x, y)
            elif level[y][x] == '@':
                Tile(x, y)
                new_player = Player(0, x, y)
            elif level[y][x] == '#':
                Tile(x, y)
                Enemy(x, y)
    return new_player, x, y


# textures

tile_images = [
    pygame.transform.scale(load_image('floor1.png'), (tile_width, tile_height)),
    pygame.transform.scale(load_image('floor2.png'), (tile_width, tile_height)),
    pygame.transform.scale(load_image('floor2.png'), (tile_width, tile_height))
]

player_image = [
    pygame.transform.scale(load_image('mainhero_front.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('mainhero_left.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('mainhero_back.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('mainhero_right.png', -1), (tile_width, tile_height)),
]

enemy_image = [
    pygame.transform.scale(load_image('enemy_front.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy_front.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_3.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_5.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_4.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_5.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('knight_4.png', -1), (tile_width, tile_height)),

]


# classes

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[random.randint(0, len(tile_images) - 1)]
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)


# player
class Player(pygame.sprite.Sprite):

    def __init__(self, pos_type, x, y):
        super().__init__(all_sprites, hero_group)
        self.pos_type = pos_type
        self.image = player_image[pos_type]

        self.speed = 3
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            if self.pos_type == 2:
                self.rect = self.rect.move((0, 5))
            if self.pos_type == 0:
                self.rect = self.rect.move((0, -5))
            if self.pos_type == 1:
                self.rect = self.rect.move((5, 0))
            if self.pos_type == 3:
                self.rect = self.rect.move((-5, 0))

    def go_right(self):
        self.image = player_image[3]
        self.pos_type = 3
        self.rect = self.rect.move(self.speed, 0)

    def go_left(self):
        self.image = player_image[1]
        self.pos_type = 1
        self.rect = self.rect.move(-self.speed, 0)

    def go_up(self):
        self.image = player_image[2]
        self.pos_type = 2
        self.rect = self.rect.move(0, -self.speed)

    def go_down(self):
        self.image = player_image[0]
        self.pos_type = 0
        self.rect = self.rect.move(0, self.speed)


class CheckForPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        super().__init__(all_sprites)
        self.image = pygame.Surface([1, (y + r) - (y - r)])
        self.rect = pygame.Rect(x - r, y - r, x + r, y + r)

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, enemy_group)
        self.frames = enemy_image[:]
        self.healthpoints = 2
        self.cur_frame = 0
        self.counter = 0
        self.speed = 1
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 8)
        # print(self.frames[self.cur_frame])

    def update(self):
        if self.counter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % (len(self.frames) - 2)
            self.image = self.frames[self.cur_frame + 2]
        self.counter += 1
        # pass

    def check_for_player(self, player):
        r = 210
        x = self.rect.x + (tile_width // 2)
        y = self.rect.y + (tile_height // 2)
        rect = CheckForPlayer(x, y, r)
        if pygame.sprite.collide_rect(rect, player):
            return True

    def chase_the_player(self, player):
        if self.check_for_player(player):
            x1 = player.rect.x + (tile_width // 2)
            y1 = player.rect.y - (tile_height // 2)
            x = self.rect.x + (tile_width // 2)
            y = self.rect.y - (tile_height // 2)
            if not abs(x1 - x) <= 65 or not abs(y1 - y) <= 65:
                if x1 < x:
                    if y1 > y:
                        self.rect = self.rect.move((-self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((-self.speed, -self.speed))
                if x1 > x:
                    if y1 > y:
                        self.rect = self.rect.move((self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((self.speed, -self.speed))
                if y == y1:
                    if x1 > x:
                        self.rect = self.rect.move((self.speed, 0))
                    if x1 < x:
                        self.rect = self.rect.move((-self.speed, 0))
                elif x == x1:
                    if y1 > y:
                        self.rect = self.rect.move((0, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((0, -self.speed))
            else:
                return True

    def check_healthpoints(self):
        if self.healthpoints == 0:
            print(123)
            self.kill()


# camera
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


# generating level
camera = Camera()
fon = pygame.transform.scale(load_image('lava.png'), (700, 700))
player, level_x, level_y = generate_level(load_level('level test.txt'))

# allowing flags
running = True
key_down = False
key = ''
start_time = None
attacked = False

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            key = event.key
            key_down = True
            if event.key == pygame.K_d:
                for sprite in enemy_group:
                    sprite.healthpoints -= 1
        if event.type == pygame.KEYUP:
            key_down = False

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    for enemy in enemy_group:
        enemy.check_healthpoints()
        if enemy.chase_the_player(player):
            enemy.update()
        else:
            enemy.cur_frame = 0
            enemy.update()

    if key_down:
        if key == pygame.K_RIGHT:
            player.go_right()
        if key == pygame.K_LEFT:
            player.go_left()
        if key == pygame.K_UP:
            player.go_up()
        if key == pygame.K_DOWN:
            player.go_down()

    screen.blit(fon, (0, 0))
    # all_sprites.draw(screen)
    tiles_group.draw(screen)
    enemy_group.draw(screen)
    hero_group.draw(screen)

    for sprite in (*enemy_group,):
        player.update(sprite)

    pygame.display.flip()
    clock.tick(fps)
