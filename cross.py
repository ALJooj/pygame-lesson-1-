import pygame

pygame.init()

size = w, h = [int(i) for i in input().split()]
screen = pygame.display.set_mode(size)


def draw_lines():
    white = pygame.Color('white')
    pygame.draw.line(screen, white, (0, 0), (w, h), 5)
    pygame.draw.line(screen, white, (w, 0), (0, h), 5)


pygame.display.flip()

while pygame.event.wait().type != pygame.QUIT:
    draw_lines()
    pygame.display.flip()

pygame.quit()