import pygame
import os

pygame.init()
size = width, height = (500, 500)
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
platform_sprite = pygame.sprite.Group()
ladder_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    return image


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, ladder_sprite)
        self.image = pygame.Surface((10, 50))
        pygame.draw.rect(self.image, pygame.Color("red"), (pos[0], pos[1], 10, 50))
        self.rect = pygame.Rect((pos[0], pos[1], 10, 50))


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, platform_sprite)
        self.image = pygame.Surface((50, 30))
        pygame.draw.rect(self.image, pygame.Color("red"), (pos[0], pos[1], 50, 30))
        self.rect = pygame.Rect((pos[0], pos[1], 50, 30))


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites, hero_sprite)
        self.image = pygame.Surface((20, 20))
        #
        self.rect = pygame.Rect((pos[0], pos[1], 20, 20))
        pygame.draw.rect(self.image, (255, 0, 0), (pos[0], pos[1], 20, 20))

    def update(self):
        if not pygame.sprite.spritecollideany(self, platform_sprite) \
                and not pygame.sprite.spritecollideany(self, ladder_sprite):
            self.rect = self.rect.move(0, 4)

    def right(self):
        self.rect = self.rect.move(10, 0)

    def left(self):
        self.rect = self.rect.move(-10, 0)

    def up(self):
        self.rect = self.rect.move(0, -10)

    def down(self):
        self.rect = self.rect.move(0, 10)


fps = 60
clock = pygame.time.Clock()
running = True
hero = Hero((50, 50))
ctrl_pressed = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                hero.right()
            elif event.key == pygame.K_LEFT:
                hero.left()
            elif event.key == pygame.K_UP:
                hero.up()
            elif event.key == pygame.K_DOWN:
                if not pygame.sprite.spritecollideany(hero, platform_sprite):
                    hero.down()

        if event.type == pygame.KEYDOWN and event.key == 306:
            ctrl_pressed = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if ctrl_pressed:
                Ladder(event.pos)
            else:
                Platform(event.pos)

        if event.type == pygame.KEYUP:
            ctrl_pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            hero.kill()
            hero = Hero(event.pos)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()