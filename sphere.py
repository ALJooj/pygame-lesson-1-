import pygame

n = int(input())
size = (300, 300)
screen = pygame.display.set_mode(size)


def draw_sphere():
    color = pygame.Color('white')
    ed = 300 // (2 * n)
    for i in range(0, n):
        #                                     x    y      w    h
        pygame.draw.ellipse(screen, color, (0, ed * i, 300, 300 - (2 * ed * i)), 1)
    for i in range(0, n):
        #                                     x    y      w    h
        pygame.draw.ellipse(screen, color, (ed * i, 0 , 300 - (2 * ed * i), 300), 1)


while pygame.event.wait().type != pygame.QUIT:
    draw_sphere()
    pygame.display.flip()

pygame.quit()