import sys
import pygame
pygame.init()

size = width, height = 320, 240
speed = [4, 4]
black = 0, 0, 0
circle_size = 25
move = [circle_size, circle_size]
screen = pygame.display.set_mode(size)

circle_object = pygame.Surface
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    if move[0] < circle_size or move[0] > size[0] - circle_size:
        speed[0] *= -1
    if move[1] < circle_size or move[1] > size[1] - circle_size:
        speed[1] *= -1

    move[0] += speed[0]
    move[1] += speed[1]
    pygame.draw.circle(screen, [50, 250, 50], move, circle_size)
    pygame.display.flip()
