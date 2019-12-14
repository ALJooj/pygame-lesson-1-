import pygame

pygame.init()

size = w, h = 200, 200
screen = pygame.display.set_mode(size)


def draw():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(str(i), 1, (255, 0, 0))
    text_x = w // 2 - text.get_width() // 2
    text_y = h // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
        text_w + 20, text_h + 20), 1)


i = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == 17:
            i += 1
    draw()
    pygame.display.flip()

pygame.quit()