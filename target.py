import pygame

radius, n = [int(i) for i in input().split()]
# radius, n = 50, 3
size = (n + 1) * radius * 2, (n + 1) * radius * 2
screen = pygame.display.set_mode(size)


def draw_target():
    colors = [pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255)]
    for i, elem in enumerate(colors):
        hsv = elem.hsva
        colors[i].hsva = (hsv[0], hsv[1], 100, hsv[3])
    for i in range(n, -1, -1):
        pygame.draw.circle(screen, colors[i % 3], (size[0] // 2, size[1] // 2), radius * (1 + i), radius)
    pygame.draw.circle(screen, colors[0], (size[0] // 2, size[0] // 2), radius)


print(screen)
while pygame.event.wait().type != pygame.QUIT:
    draw_target()
    pygame.display.flip()

pygame.quit()