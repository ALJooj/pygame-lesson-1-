import pygame

size = w, h = [int(i) for i in input().split()]
screen = pygame.display.set_mode(size)

def draw():
    red = pygame.Color('red')
    pygame.draw.rect(screen, red, (1, 1, w - 2, h - 2))


pygame.display.flip()

while pygame.event.wait().type != pygame.QUIT:
    draw()
    pygame.display.flip()

pygame.quit()