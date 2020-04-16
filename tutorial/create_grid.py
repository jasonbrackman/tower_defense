import sys
import pygame
pygame.init()

size = width, height = 320, 240
screen = pygame.display.set_mode(size)

blk = 0, 0, 0
red = 195, 0, 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(blk)

    block_size = 1
    for y in range(height):
        for x in range(width):
            if y % 2 == 0 and x % 2 == 0:
                rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
                pygame.draw.rect(screen, red, rect)

    pygame.display.flip()
