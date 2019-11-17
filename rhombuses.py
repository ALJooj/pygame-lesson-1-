import pygame

diagonal = int(input())
size = w, h = 250, 500
screen = pygame.display.set_mode(size)
c = pygame.Color('yellow')
screen.fill(c)

def draw_rhombus(scr, x, y, dia):
    n = dia // 2
    color = pygame.Color('orange')
    pygame.draw.polygon(scr, color,(
        (x, y + n),
        (x + n, y),
        (2 * n + x, y + n),
        (x + n, 2 * n + y)
    ))


def draw():
    for x in range(0, w - diagonal, diagonal):
        for y in range(0, h - diagonal, diagonal):
            draw_rhombus(screen, x, y, diagonal)


while pygame.event.wait().type != pygame.QUIT:
    draw()
    pygame.display.flip()

pygame.quit()