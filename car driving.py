import pygame
import os

pygame.init()

size = width, height = (600, 95)
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


class Car(pygame.sprite.Sprite):
    car = load_image('car.png', -1)
    car2 = pygame.transform.flip(car, True, False)

    def __init__(self, group):
        super().__init__(group)
        self.speed = 10
        self.image = self.car
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.nav = 1

    def drive(self):
        if self.rect.x + self.rect.width == width:
            self.nav = -1
            self.image = self.car2
        elif self.rect.x == 0:
            self.nav = 1
            self.image = self.car
        if self.nav == 1:
            self.rect = self.rect.move(self.speed, 0)
        elif self.nav == -1:
            self.rect = self.rect.move(-self.speed, 0)


car = Car(all_sprites)
running = True
fps = 60
clock = pygame.time.Clock()
screen.fill((255, 255, 255))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    car.drive()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)


pygame.quit()