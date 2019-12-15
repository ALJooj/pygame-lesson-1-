import pygame
import os
import random

pygame.init()
size = width, height = (500, 500)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60
running = True


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


class Bomb(pygame.sprite.Sprite):
    bomb_pic = load_image('bomb.png', -1)
    boom_pic = load_image('boom.png', -1)

    def __init__(self, group, cords):
        super().__init__(group)
        self.image = self.bomb_pic
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]

    def update(self, *args):
        if pygame.sprite.spritecollide(self, all_sprites, True):
            return
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = load_image('boom.png', -1)


while len(all_sprites) < 10:
    Bomb(all_sprites, (random.randrange(width), random.randrange(height)))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.update(event)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()