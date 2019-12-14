import pygame

screen = pygame.display.set_mode((300, 300))
screen2 = pygame.Surface(screen.get_size())


def is_in_area(mouse_pos, r_pos):
    if rect_pos[0] <= mouse_pos[0] <= r_pos[2]:
        if rect_pos[1] <= mouse_pos[1] <= r_pos[3]:
            return True
    return False


fps = 50

clock = pygame.time.Clock()
running = True
dragged = False
side = 100
x1, y1 = 0, 0
x, y = 50, 50
rect_pos = [x, y , x + side, y + side]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_in_area(event.pos, rect_pos):
                dragged = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragged = False
        if event.type == pygame.MOUSEMOTION and dragged:
            # if is_in_area(event.pos, rect_pos):
            #     dragged = True
            x1 = event.pos[0]
            y1 = event.pos[1]
            # print(x1, y1)

        screen.blit(screen2, (0, 0))
        screen2.fill(pygame.Color('black'))

        pygame.draw.rect(screen, (0, 255, 0), ((rect_pos[0], rect_pos[1]), (side, side)))
        if dragged:
            # print(x1, y1, 'mouse')

            rect_pos[0] = x1 - (side - x1)
            rect_pos[1] = y1

            rect_pos = [rect_pos[0], rect_pos[1], rect_pos[0] + side, rect_pos[1] + side]
            pygame.draw.rect(screen, (0, 255, 0), ((rect_pos[0], rect_pos[1]), (side, side)))
            # print(x + side, y + side, 'corner')


        pygame.display.flip()



pygame.quit()