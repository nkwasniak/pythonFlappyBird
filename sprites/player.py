"""
    player.py
    Represents player object
"""
import pygame as pg
from pygame.rect import Rect

from settings import WIDTH, HEIGHT, IMAGES_DIR, IMAGES, PLAYER_JUMP, PLAYER_GRAV, SOUNDS_DIR, SOUNDS

Vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """Class represents bird on bord
    """
    def __init__(self):
        """Initialise a Player instance.
        """
        pg.sprite.Sprite.__init__(self)
        self.rect = Rect(32, 32, 32, 32)
        self.pos = Vec(WIDTH / 2, HEIGHT / 2)
        self.vel = Vec(0, 0)
        self.img_wingup = pg.image.load(IMAGES_DIR + IMAGES['bird-wing-up'])
        self.img_wingdown = pg.image.load(IMAGES_DIR + IMAGES['bird-wing-down'])
        self.mask_wingup = pg.mask.from_surface(self.img_wingup)
        self.mask_wingdown = pg.mask.from_surface(self.img_wingdown)

    def jump(self):
        """Player jump by space or KEY_UP or mouse click
        """
        self.vel.y = -PLAYER_JUMP
        pg.mixer.Sound(SOUNDS_DIR + SOUNDS['jump']).play()

    def update(self):
        """Update the player's position.
        """
        self.vel += Vec(0, PLAYER_GRAV)
        self.pos += self.vel + 0.5 * Vec(0, PLAYER_GRAV)

        self.rect.midbottom = self.pos

    @property
    def image(self):
        """Get a Surface containing this bird's image.
        """
        if pg.time.get_ticks() % 500 >= 250:
            return self.img_wingup
        return self.img_wingdown

    @property
    def mask(self):
        """Get a bitmask for use in collision detection.
        """
        if pg.time.get_ticks() % 500 >= 250:
            return self.mask_wingup
        return self.mask_wingdown
