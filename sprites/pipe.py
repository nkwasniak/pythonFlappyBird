"""
    player.py
    Represents objects on the board
"""
from random import randint
import pygame as pg
from pygame.constants import SRCALPHA

from settings import WIDTH, HEIGHT, IMAGES_DIR, IMAGES

Vec = pg.math.Vector2


class PipePair(pg.sprite.Sprite):
    """Represents an obstacle.
    """
    PIECE_WIDTH = 80
    PIECE_HEIGHT = 32

    def __init__(self):
        """Initialises a new random PipePair.
        The new PipePair will automatically be assigned an x attribute of
        float(WIN_WIDTH - 1).
        """
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((PipePair.PIECE_WIDTH, HEIGHT), SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = float(WIDTH - 1)
        total_pipe_body_pieces = int(
            (HEIGHT -
             3 * 40 -
             2 * PipePair.PIECE_HEIGHT) /
            PipePair.PIECE_HEIGHT
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, HEIGHT - i * PipePair.PIECE_HEIGHT)
            self.image.blit(pg.image.load(IMAGES_DIR + IMAGES['pipe-body']), piece_pos)
        bottom_pipe_end_y = HEIGHT - self.bottom_pieces * PipePair.PIECE_HEIGHT
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pg.image.load(IMAGES_DIR + IMAGES['pipe-end']), bottom_end_piece_pos)

        for i in range(self.top_pieces):
            self.image.blit(pg.image.load(IMAGES_DIR + IMAGES['pipe-body']),
                            (0, i * PipePair.PIECE_HEIGHT))
        top_pipe_end_y = self.top_pieces * PipePair.PIECE_HEIGHT
        self.image.blit(pg.image.load(IMAGES_DIR + IMAGES['pipe-end']), (0, top_pipe_end_y))

        self.top_pieces += 1
        self.bottom_pieces += 1

        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        """Update the PipePair's position.
        """
        self.rect.x -= 1

    def collides_with(self, bird):
        """Get whether the bird collides with a pipe in this PipePair.
        Arguments:
        bird: The Bird which can collides with PipePair.
        """
        return pg.sprite.collide_mask(self, bird)
