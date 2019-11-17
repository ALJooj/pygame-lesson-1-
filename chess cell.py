import pygame

# cell, n = [int(i) for i in input().split()]
cell, n = 100, 5
size = cell * n, cell * n
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))


def draw():
    black = pygame.Color('black')
    for i in range(0, n, 2):
        for j in range(1, n, 2):
            pygame.draw.rect(screen, black, ((i - 1) * cell, j * cell, cell, cell))
    for i in range(0, n, 2):
        for j in range(1, n + 1, 2):
            pygame.draw.rect(screen, black, (i * cell, (j - 1) * cell, cell, cell))


while pygame.event.wait().type != pygame.QUIT:
    draw()
    pygame.display.flip()

pygame.quit()