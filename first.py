import pygame
import random
# инициализация Pygame:
pygame.init()
# размеры окна:
size = width, height = 800, 600
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
# формирование кадра:
# команды рисования на холсте
def draw():
    screen.fill((255,255,255))
    font = pygame.font.Font(None, 50)
    text = font.render("Hello, Pygame!", 1, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def draw_square():
    screen.fill((255, 255, 255))
    color = pygame.Color(50, 150, 50)
    # рисуем "тень"
    pygame.draw.circle(screen, color, (70, 70), 50, 0)
    # pygame.draw.rect(screen, color,
    #                  (20, 20, 100, 100), 0)
    hsv = color.hsva
    # увеличиваем параметр Value, который влияет на яркость
    color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
    # рисуем сам объект
    pygame.draw.rect(screen, color,
                     (10, 10, 100, 100), 0)


# смена (отрисовка) кадра:
# pygame.display.flip()
# ожидание закрытия окна:

while pygame.event.wait().type != pygame.QUIT:
    for i in range(10000):
        screen.fill(pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height, 1, 1))
    # draw_square()
    pygame.display.flip()
# завершение работы:
pygame.quit()