import pygame
from pygame.math import Vector2
import random

block_types = {
    "space": pygame.Color("black"),
    "wall": pygame.Color("dimgray"),
    "gunner": pygame.Color("blue"),
    "entrance": pygame.Color("gold"),
    "exit": pygame.Color("red"),
    "neighbour": pygame.Color("pink"),
    "menu": pygame.Color("darkgrey"),
    "enemy": pygame.Color("red"),
}


class Block(pygame.sprite.Sprite):
    size = 16

    def __init__(self, t, x, y):
        super().__init__()
        self.image = pygame.Surface([self.size - 1, self.size - 1])

        self.type = t

        self.rect = self.image.get_rect()
        self.rect.x = x / self.size * self.size
        self.rect.y = y / self.size * self.size

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, t):
        if t not in block_types:
            raise (ValueError, "Expected a valid Block type.")
        self.__type = t
        if t == "neighbour":
            rcolour = random.choice(
                [pygame.Color("pink"), pygame.Color("plum"), pygame.Color("lightpink")]
            )
            self.image.fill(rcolour)
        else:
            self.image.fill(block_types[t])


class Gunner(Block):
    def __init__(self, x, y):
        super().__init__("gunner", x, y)
        self.bullets = pygame.sprite.Group()

    def draw_vectors(self, screen):
        scale = 1.5
        # vel
        if self.bullets:
            bullet = self.bullets.sprites()[0]
            pygame.draw.line(
                screen,
                pygame.Color("green"),
                self.rect.center,
                (self.rect.center + bullet.vel * scale),
                2,
            )


class Enemy(Block):
    MAX_SPEED = 1

    def __init__(self, x, y, waypoints):
        super().__init__("enemy", x, y)
        self.waypoints = waypoints
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0.1, 0)

    def update(self):
        goal = self.waypoints[0].rect.center
        self.acc = (goal - self.pos).normalize() * 0.8
        self.vel += self.acc
        if self.vel.length() > self.MAX_SPEED:
            self.vel.scale_to_length(self.MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos

        # check if should stop
        SIZE = 1
        should_stop = goal - self.pos
        if -SIZE < should_stop.x < SIZE and -SIZE < should_stop.y < SIZE:
            self.waypoints.pop(0)
        if not self.waypoints:
            pygame.sprite.Sprite.kill(self)


class Bullet(pygame.sprite.Sprite):
    MAX_SPEED = 12
    BULLET_SIZE = 6

    def __init__(self, pos, pos_t=None):
        super().__init__()
        self.image = pygame.Surface((self.BULLET_SIZE, self.BULLET_SIZE))
        self.image.fill(pygame.Color("pink"))
        self.image.fill(pygame.Color("red"), self.image.get_rect().inflate(-2, -2))
        self.rect = self.image.get_rect()

        self.pos = Vector2(pos)
        self.target = pos_t

        self.vel = Vector2(0, 0)
        self.acc = Vector2(2, 0)

    def update(self):
        self.acc = (self.target - self.pos).normalize() * 0.8
        self.vel += self.acc
        if self.vel.length() > self.MAX_SPEED:
            self.vel.scale_to_length(self.MAX_SPEED)
        self.pos += self.vel
        self.rect.center = self.pos

        # check if should stop
        SIZE = 10
        should_stop = self.target - self.pos
        if -SIZE < should_stop.x < SIZE and -SIZE < should_stop.y < SIZE:
            pygame.sprite.Sprite.kill(self)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, tiles, menu_tiles):
        super().__init__(tiles, menu_tiles)
        self.hold = pygame.sprite.Group()
        self.groups = menu_tiles
        self.tiles = tiles

        # Image is displayed always
        self.image = pygame.Surface((15, 15))
        self.image.set_colorkey((43, 43, 43))
        self.image.fill((43, 43, 43))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color("red"), self.image.get_rect(), 1)

        # Image copy: selected version
        self.selected_image = self.image.copy()
        pygame.draw.rect(
            self.selected_image, pygame.Color("purple"), self.image.get_rect(), 1
        )

        # Image Copy: Unselected (starting image)
        self.base_image = self.image

    def update(self):

        left, middle, right = pygame.mouse.get_pressed()
        if left:
            # let's draw the rect on the grid, based on the mouse position
            pos = pygame.mouse.get_pos()
            self.image = self.selected_image

            for item in self.groups:
                if item not in self.hold:
                    if item.rect.collidepoint(pos):
                        self.rect = item.rect
                        if isinstance(item, Gunner):
                            self.hold.add(item)
                            item.type = "wall"

            if self.hold:
                for item in self.tiles:
                    if item.rect.collidepoint(pos):
                        self.rect = item.rect
                        if hasattr(item, "type"):
                            if item.type == "wall":
                                g = Gunner(item.rect.x, item.rect.y)
                                self.tiles.add(g)
                                item.kill()
                                self.hold.empty()

        else:
            self.image = self.base_image
