# Entry point for game
import sys
import pygame
import random
import config
from maze import Maze
from linkedlist import LL
from block import Gunner, Bullet, Enemy


def main(cfg):
    # create board / menu
    maze = Maze(cfg)

    # create pygame
    pygame.init()
    pygame.display.set_caption(cfg.caption)
    clock = pygame.time.Clock()

    # Build out screen w/ menu
    screen = pygame.display.set_mode((cfg.width, cfg.height + (4 * cfg.block_size)))

    # Find path through the maze and highlight it
    current = bfs(maze)
    highlights = highlight(current)
    if highlights:
        for item in highlights:
            item.type = "neighbour"
    while True:
        clock.tick(cfg.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waypoints = get_waypoints(current)
                e = Enemy(0, 0, waypoints)
                maze.enemies.add(e)

        # game logic here?


        # Only update dirty blocks to improve fps

        for tile in maze.tiles:
            if isinstance(tile, Gunner) and len(tile.bullets) == 0:
                # Target should be the enemies (highlights)
                if maze.enemies:
                    e = random.choice(maze.enemies.sprites())
                    b = Bullet(tile.rect.center, e.rect.center)
                    tile.bullets.add(b)
                    maze.bullets.add(b)

        screen.fill(pygame.Color("darkgrey"))

        maze.menu.update()
        maze.menu.draw(screen)

        maze.tiles.update()
        maze.tiles.draw(screen)
        for tile in maze.tiles:
            if isinstance(tile, Gunner) and tile.bullets:
                tile.draw_vectors(screen)



        maze.enemies.update()
        maze.enemies.draw(screen)

        maze.bullets.update()
        maze.bullets.draw(screen)

        pygame.display.flip()


def bfs(maze):
    # get the starting node - which will be the first green
    current = None
    start = maze.tiles.sprites()[0]

    # Get goal tile (Hardcoded the lower right pos)
    goal = None
    for x in maze.tiles:
        if x.rect.collidepoint((470, 468)):
            goal = x

    frontier = [LL(start)]
    visited = set()

    while frontier:
        current = frontier.pop(0)
        if current.state == goal:
            # could get here part way...
            break
        for n in maze.neighbours(current.state.rect):
            if n not in visited:
                frontier.append(LL(n, current))
                visited.add(n)

    return current


def get_waypoints(current):
    waypoints = list()

    while current is not None:
        s = current.state
        waypoints.insert(0, s)
        current = current.node

    return waypoints


def highlight(current):
    highlight_group = pygame.sprite.Group()

    while current is not None:
        s = current.state
        highlight_group.add(s)
        current = current.node

    return highlight_group


if __name__ == "__main__":
    settings = config.Config()
    settings.width = 480
    settings.height = 480
    settings.block_size = 16
    settings.caption = "Tower Defense"
    settings.fps = 60

    main(settings)
