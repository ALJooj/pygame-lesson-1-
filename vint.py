import pygame
from math import sqrt, pi, cos, sin, radians

screen = pygame.display.set_mode((201, 201))
screen2 = pygame.Surface(screen.get_size())

fps = 50
v = 51
running = True
clock = pygame.time.Clock()
xs = []
ys = []
xs1 = []
ys1 = []

x, y = 100, 100
r = 67.61481

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            v += 50
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            v -= 50

    for i in range(0, 360, v):
        pygame.draw.polygon(screen2, (255, 255, 255), (
            (100, 100),
            (int(r * cos(radians(i + 255)) + 100), int(r * sin(radians(i + 255))) + 100),
            (int(r * cos(radians(i + 285)) + 100), int(r * sin(radians(i + 285))) + 100)
        ))

        pygame.draw.polygon(screen2, (255, 255, 255), (
            (100, 100),
            (int(r * cos(radians(i + 15)) + 100), int(r * sin(radians(i + 15))) + 100),
            (int(r * cos(radians(i + 45)) + 100), int(r * sin(radians(i + 45))) + 100)
        ))

        pygame.draw.polygon(screen2, (255, 255, 255), (
            (100, 100),
            (int(r * cos(radians(i + 135)) + 100), int(r * sin(radians(i + 135))) + 100),
            (int(r * cos(radians(i + 165)) + 100), int(r * sin(radians(i + 165))) + 100)
        ))

        pygame.draw.circle(screen2, (255, 255, 255), (100, 100), 10)
        pygame.display.flip()
        screen.blit(screen2, (0, 0))
        screen2.fill(pygame.Color('black'))
        pygame.time.delay(v)


    # clock.tick(fps)
