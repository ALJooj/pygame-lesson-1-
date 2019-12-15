import pygame
import os
import random


pygame.init()
size = width, height = (600, 600)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png", -1)

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(width - 120)
        self.rect.y = random.randrange(height - 114)

    def update(self, *args):
        # self.image = load_image('boom.png', -1)
        # if args:
        #     print(args)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = load_image('boom.png', -1)


creature = Bomb(all_sprites)
running = True
r = 10
v = 10  # пикселей в секунду
fps = 60
clock = pygame.time.Clock()
screen.fill((0, 0, 255))

# x1, y1, w, h = 0, 0, 0, 0
for _ in range(20):
    Bomb(all_sprites)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

# завершение работы:
pygame.quit()