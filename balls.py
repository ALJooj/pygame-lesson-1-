import pygame

size = w, h = (300, 300)
screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())


def circles(src, x, y):
    pygame.draw.circle(src, (255, 255, 255), (x, y), 10)


clock = pygame.time.Clock()
running = True
x, y = 0, 0
fps = 50
v = 100
coords = []
vs = []
ks = []
kx, ky = 1, 1

while running:
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            coords.append([x, y])
            vs.append(v)
            ks.append([kx, ky])

    for i, elem in enumerate(coords):
        temp_v = -vs[i]
        x = coords[i][0]
        y = coords[i][1]
        xk = ks[i][0]
        yk = ks[i][1]
        circles(screen2, int(x), int(y))

        if int(x) < 0:
            ks[i][0] *= -1
            coords[i][0] += 5

        if int(x) > w:
            ks[i][0] *= -1
            coords[i][0] -= 5

        if int(y) < 0:
            ks[i][1] *= -1
            coords[i][1] += 5

        if int(y) > w:
            ks[i][1] *= -1
            coords[i][1] -= 5

        else:
            coords[i][0] += (xk * temp_v) / fps
            coords[i][1] += (yk * temp_v) / fps

    pygame.display.flip()

    clock.tick(fps)

pygame.quit()