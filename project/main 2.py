import pygame
import os
import random
import sys

# init
pygame.init()

# options
size = width, height = (1000, 1000)
screen = pygame.display.set_mode(size)
fps = 50
tile_width = tile_height = 100
clock = pygame.time.Clock()



# groups
all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
skill_group = pygame.sprite.Group()
grave_group = pygame.sprite.Group()
ghost_group = pygame.sprite.Group()


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
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),
# attack 1 - 7
    pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_3.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_4.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_5.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/attack_2/e_attack_1.png', -1), (tile_width, tile_height)),
# moving 7 - 10 l
    pygame.transform.scale(load_image('enemy/moving/e_move_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/moving/e_move_2.png', -1), (tile_width, tile_height)),
    # pygame.transform.scale(load_image('enemy/moving/e_move_1.png', -1), (tile_width, tile_height)),
    pygame.transform.scale(load_image('enemy/moving/knight_12.png', -1), (tile_width, tile_height)),
# moving 10 - 14 r
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/moving/e_move_1.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/moving/e_move_2.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/moving/knight_12.png', -1), (tile_width, tile_height)), True, False),
    # pygame.transform.flip(pygame.transform.scale(load_image('enemy/moving/e_move_1.png', -1), (tile_width, tile_height)), True, False),
# attack 14 - 18
    pygame.transform.flip(
        pygame.transform.scale(load_image('knight_12.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/attack_2/e_attack_1.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/attack_2/e_attack_3.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/attack_2/e_attack_4.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/attack_2/e_attack_5.png', -1), (tile_width, tile_height)), True, False),
    pygame.transform.flip(
        pygame.transform.scale(load_image('enemy/attack_2/e_attack_1.png', -1), (tile_width, tile_height)), True, False),
]
# classes


class Grave(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, grave_group)
        w = (tile_width // 2) + tile_width // 4
        h = (tile_height // 2) + tile_height // 4
        self.image = pygame.transform.scale(load_image('grave.png', -1), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.transform.scale(load_image('grass.png'), [1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            # self.image = pygame.Surface([x2 - x1, 1])
            self.image = pygame.transform.scale(load_image('grass.png'), [x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, ghost_group)
        self.image = pygame.transform.scale((load_image('ghost.png', -1)), (tile_width, tile_width))
        self.rect = self.image.get_rect().move(x, y)
        self.healthpoints = 2
        self.counter = 0
        self.attack_points = 2
        self.speed = 3

    def check_for_enemy(self, enemy):
        r = 210
        x = self.rect.x + (tile_width // 2)
        y = self.rect.y + (tile_height // 2)
        rect = CheckForPlayer(x, y, r)
        if pygame.sprite.collide_rect(rect, enemy):
            return True

    def chase_the_enemy(self, enemy):
        if self.check_for_enemy(enemy):
            x1 = enemy.rect.x + (tile_width // 2)
            y1 = enemy.rect.y - (tile_height // 2)
            x = self.rect.x + (tile_width // 2)
            y = self.rect.y - (tile_height // 2)
            if not abs(x1 - x) <= 65 or not abs(y1 - y) <= 65:
                #
                if x1 < x:
                    if y1 > y:
                        self.rect = self.rect.move((-self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((-self.speed, -self.speed))
                #
                if x1 > x:
                    if y1 > y:
                        self.rect = self.rect.move((self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((self.speed, -self.speed))
                        #
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
        if self.healthpoints <= 0:
            self.kill()

    def attack(self, enemy):
        if self.counter % 130 == 0:
            enemy.healthpoints -= self.attack_points

    def count(self):
        self.counter += 1


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = tile_images[random.randint(0, len(tile_images) - 1)]
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)


# mist coil spell
class MistCoil(pygame.sprite.Sprite):

    def __init__(self, pos, nav):
        super().__init__(all_sprites, skill_group)
        self.image = load_image('star.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.nav = nav

    def update(self, groups):
        for sprite in groups:
            if pygame.sprite.collide_rect(self, sprite):
                if type(sprite) == Enemy:
                    sprite.healthpoints -= 2
                self.kill()

    def moving(self):
        if self.nav == 2:
            self.rect = self.rect.move((0, -16))
        if self.nav == 3:
            self.rect = self.rect.move((16, 0))
        if self.nav == 0:
            self.rect = self.rect.move((0, 16))
        if self.nav == 1:
            self.rect = self.rect.move((-16, 0))


# player
class Player(pygame.sprite.Sprite):

    def __init__(self, pos_type, x, y):
        super().__init__(all_sprites, hero_group)
        self.pos_type = pos_type
        self.image = player_image[pos_type]
        self.r = 210

        self.max_dummies = 2
        self.haste_used = False
        self.counter = 0
        self.healthpoints = 8
        self.speed = 3
        self.rect = self.image.get_rect().move(tile_width * x + 10, tile_height * y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def collisions(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            if self.pos_type == 0:
                self.rect = self.rect.move((0, -5))
            if self.pos_type == 1:
                self.rect = self.rect.move((5, 0))
            if self.pos_type == 2:
                self.rect = self.rect.move((0, 5))
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

    def check_healthpoints(self):
        if self.healthpoints <= 0:
            self.kill()

    def cast_mist_coil(self):
        if self.counter > 30:
            MistCoil((self.rect.x, self.rect.y), self.pos_type)
            self.counter = 0

    def haste(self):
        if self.counter > 100:
            self.speed = 6
            self.haste_used = False
            self.counter = 0
        elif self.counter == 45:

            self.speed = 3
            self.haste_used = True

    def raise_the_dead(self, grave):
        if self.counter > 210:
            x = self.rect.x + (tile_width // 2)
            y = self.rect.y + (tile_height // 2)
            rect = CheckForPlayer(x, y, self.r)
            if pygame.sprite.collide_rect(rect, grave):
                return True

    def count(self):
        self.counter += 1


class CheckForPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, r):
        super().__init__(all_sprites)
        self.image = pygame.Surface([1, (y + r) - (y - r)])
        self.rect = pygame.Rect(x - r, y - r, x + r, y + r)


# Enemy
class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(all_sprites, enemy_group)
        #
        self.frames = enemy_image[:]
        self.attack_frames_l = enemy_image[1:7]
        self.attack_frames_r = enemy_image[14:]
        self.moving_frames_l = enemy_image[7:10]
        self.moving_frames_r = enemy_image[11:14]
        #
        self.healthpoints = 5
        self.attack_points = 1
        #
        self.cur_frame = 0
        self.attack_cur_frame_l = 0
        self.attack_cur_frame_r = 0
        self.moving_cur_frame_l = 0
        self.moving_cur_frame_r = 0
        #
        self.counter = 0
        self.speed = 1
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(tile_width * x + 15, tile_height * y + 8)
        # print(self.frames[self.cur_frame])

    def count(self):
        self.counter += 1

    def update(self):
        if self.counter % 7 == 0:
            self.attack_cur_frame_l = (self.attack_cur_frame_l + 1) % (len(self.attack_frames_l))
            self.image = self.attack_frames_l[self.attack_cur_frame_l]
        # pass

    def check_for_player(self, player):
        r = 600
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
            if not abs(x1 - x) <= 95 or not abs(y1 - y) <= 95:
                #
                if x1 < x:
                    if self.counter % 16 == 0:
                        self.moving_cur_frame_l = (self.moving_cur_frame_l + 1) % len(self.moving_frames_l)
                        self.image = self.moving_frames_l[self.moving_cur_frame_l]
                    if y1 > y:
                        self.rect = self.rect.move((-self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((-self.speed, -self.speed))
#

                if x1 > x:
                    if self.counter % 16 == 0:
                        self.moving_cur_frame_r = (self.moving_cur_frame_r + 1) % len(self.moving_frames_r)
                        self.image = self.moving_frames_r[self.moving_cur_frame_r]

                    if y1 > y:
                        self.rect = self.rect.move((self.speed, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((self.speed, -self.speed))

                        #
                if y == y1:
                    if x1 > x:
                        # if self.counter % 16 == 0:
                        #     print('l')
                        #     self.moving_cur_frame_r = (self.moving_cur_frame_r + 1) % len(self.moving_frames_r)
                        #     self.image = self.moving_frames_r[self.moving_cur_frame_r]
                        self.rect = self.rect.move((self.speed, 0))

                    if x1 < x:
                        if self.counter % 16 == 0:
                            self.moving_cur_frame_l = (self.moving_cur_frame_l + 1) % len(self.moving_frames_l)
                            self.image = self.moving_frames_l[self.moving_cur_frame_l]
                        self.rect = self.rect.move((-self.speed, 0))
                elif x == x1:
                    if self.counter % 16 == 0:
                        self.moving_cur_frame_l = (self.moving_cur_frame_l + 1) % len(self.moving_frames_l)
                        self.image = self.moving_frames_l[self.moving_cur_frame_l]
                    if y1 > y:
                        self.rect = self.rect.move((0, self.speed))
                    if y1 < y:
                        self.rect = self.rect.move((0, -self.speed))
            else:
                return True

    def check_healthpoints(self):
        if self.healthpoints <= 0:
            Grave(self.rect.x, self.rect.y)
            self.kill()

    def attack(self, player):
        if self.counter % 85 == 0:
            player.healthpoints -= self.attack_points


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
level_y += 1
level_x += 1
Border(0, 0, level_x * tile_width, 0)
Border(0, level_y * tile_height, level_x * tile_width, level_y * tile_height)
Border(0, 0, 0, level_x * tile_width)
Border(level_x * tile_width, 0, level_x * tile_width, level_y * tile_height)

# allowing flags
running = True
key_down = False
dead_raised = False
key = ''
start_time = None
hasted = False
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
            if event.key == pygame.K_z:
                player.cast_mist_coil()
            if event.key == pygame.K_x:
                hasted = True
            if event.key == pygame.K_c:
                dead_raised = True

        if event.type == pygame.KEYUP:
            key_down = False

    # изменяем ракурс камеры
    camera.update(player)
    player.check_healthpoints()
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    for enemy in enemy_group:
        enemy.check_healthpoints()
        if enemy.chase_the_player(player):
            enemy.attack(player)
            enemy.update()
        else:
            enemy.attack_cur_frame = -1
        enemy.count()

    for ghost in ghost_group:
        ghost.check_healthpoints()
        for enemy in enemy_group:
            if ghost.chase_the_enemy(enemy):
                ghost.attack(enemy)
                break
        ghost.count()

    for sprite in (vertical_borders, horizontal_borders, enemy_group):
        skill_group.update(sprite)

    for sprite in skill_group:
        sprite.moving()

    if dead_raised:
        for grave in grave_group:
            if player.max_dummies >= len(ghost_group) + 1:
                if player.raise_the_dead(grave):
                    Ghost(grave.rect.x, grave.rect.y)
                    grave.kill()
                    dead_raised = False

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

    tiles_group.draw(screen)
    grave_group.draw(screen)
    skill_group.draw(screen)
    ghost_group.draw(screen)
    enemy_group.draw(screen)
    hero_group.draw(screen)

    for sprite in (*enemy_group, *vertical_borders, *horizontal_borders):
        player.collisions(sprite)

    player.count()

    pygame.display.flip()
    clock.tick(fps)
