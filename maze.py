import pygame
import random
from block import Block, Cursor, Gunner


class Maze:
    def __init__(self, cfg):
        self.tiles = pygame.sprite.Group()
        self.menu = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.init_tiles(cfg)
        self.init_menu(cfg)

        Cursor(self.tiles, self.menu)

    def init_tiles(self, cfg):
        # create visual board for first time.
        for h in range(0, cfg.height, cfg.block_size):
            for w in range(0, cfg.width, cfg.block_size):
                if h == 0 == w:
                    block = Block("entrance", h, w)
                elif random.uniform(0, 1) > 0.7:
                    block = Block("wall", h, w)
                else:
                    block = Block("space", h, w)
                self.tiles.add(block)

    def init_menu(self, cfg):
        # create an extra two lines for a menu
        for index in range(4):
            for w in range(0, cfg.width, cfg.block_size):
                if index == 1 and w == 32:
                    self.menu.add(Gunner(w, cfg.height + (cfg.block_size * index)))
                else:
                    self.menu.add(Block("menu", w, cfg.height + (cfg.block_size * index)))
    @staticmethod
    def _add_positions(pos1, pos2):
        return pos1[0] + pos2[0], pos1[1] + pos2[1]

    def neighbours(self, pos):
        # Currently allowed to move in four directions
        neighbours = []

        for npos in [
            self._add_positions(pos, (16, 0)),
            self._add_positions(pos, (0, 16)),
            self._add_positions(pos, (-16, 0)),
            self._add_positions(pos, (0, -16)),
        ]:

            for t in self.tiles:
                if t.rect.collidepoint(npos):
                    if hasattr(t, "type") and t.type == "space":
                        neighbours.append(t)

        return neighbours


def main():
    global settings
    import config

    settings = config.Config()
    settings.width = 480
    settings.height = 480
    settings.block_size = 16
    settings.caption = "Tower Defense"
    m = Maze(settings)
    for n in m.neighbours((0, 0)):
        print(type(n))


if __name__ == "__main__":
    main()
