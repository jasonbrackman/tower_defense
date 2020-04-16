import pygame
import sys

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255

canvas = pygame.display.set_mode([500, 600])
canvas.fill(GREEN)

red_block = pygame.Surface([50, 20])
red_block.fill(RED)
canvas.blit(red_block, [10, 10])

blue_block = pygame.Surface([20, 20])
blue_block.fill(BLUE)
canvas.blit(blue_block, [50, 50])
blue_rect = blue_block.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
