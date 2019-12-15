import pygame
import os

pygame.init()
size = width, height = (600, 300)
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


class YouLost(pygame.sprite.Sprite):
    gm_pic = load_image('unnamed.jpg', -1)

    def __init__(self, group):
        super().__init__(group)
        self.image = self.gm_pic
        self.image = pygame.transform.scale(self.image, (600, 300))

        self.rect = self.image.get_rect()
        self.rect.x = -600


    def update(self):
        if self.rect.x <= 0:
            self.rect = self.rect.move(4, 0)


running = True
screen.fill((255, 255, 255))
fps = 50
clock = pygame.time.Clock()
gm_pic = YouLost(all_sprites)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    gm_pic.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()