"""
    game.py
    Represents game board
"""
import pygame as pg

from settings import WIDTH, HEIGHT, TITLE, \
    PIPE_FREQUENCY, FONT_NAME, HS_FILE, FPS, WHITE, IMAGES, IMAGES_DIR, BG_COLOR, SOUNDS_DIR, SOUNDS
from sprites.pipe import PipePair
from sprites.player import Player

Vec = pg.math.Vector2

def get_high_score():
    """ Returns highscore from .txt file

    :return: high score
    """
    with open(HS_FILE, 'r') as file:
        try:
            return int(file.read())
        except IOError:
            return 0


class Game:
    """ Represents board, start
    and game-over screens
    """

    def __init__(self):
        """Initialise a new Game instance.
            initialize game window, sounds, font, images etc.
        """
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.pipes = None
        self.last_pipe = None
        self.playing = None
        self.all_sprites = None
        self.player = None
        self.score = None

    def new(self):
        """Create new game
        """

        self.all_sprites = pg.sprite.Group()  # 4
        self.score = 0  # 5
        self.pipes = pg.sprite.Group()  # 6
        self.player = Player()  # 7
        self.all_sprites.add(self.player)
        pipe = PipePair()
        self.all_sprites.add(pipe)
        self.pipes.add(pipe)
        self.last_pipe = pg.time.get_ticks()  # 8
        self.run()

    def run(self):
        """Represents a game loop
        """

        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """Update the player's position.
        """

        self.all_sprites.update()
        time_now = pg.time.get_ticks()
        if time_now - self.last_pipe > PIPE_FREQUENCY:
            pipe = PipePair()
            self.pipes.add(pipe)
            self.all_sprites.add(pipe)
            self.last_pipe = time_now

        pipe_collision = any(p.collides_with(self.player) for p in self.pipes)
        if pipe_collision or self.player.rect.y <= 0:
            pg.mixer.Sound(SOUNDS_DIR + SOUNDS['hit']).play()
            self.playing = False

        for pipe in self.pipes:
            if pipe.rect.x < -pipe.PIECE_WIDTH:
                pg.mixer.Sound(SOUNDS_DIR + SOUNDS['point']).play()
                self.score += 5
                pipe.kill()

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            pg.mixer.Sound(SOUNDS_DIR + SOUNDS['die']).play()
            self.playing = False

    def events(self):
        """Define events for game loop
        check for closing window and control the player
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    self.player.jump()
            if event.type == pg.MOUSEBUTTONUP:
                self.player.jump()

    def draw(self):
        """Drawing scene for game
        All sprites drawing on screen
        """

        for x_val in (0, WIDTH / 2):
            self.screen.blit(pg.image.load(IMAGES_DIR + IMAGES['background']), (x_val, 0))

        self.all_sprites.draw(self.screen)
        self.draw_text('Score: ' + str(self.score), 22, WHITE, Vec(WIDTH / 2, 15))

        pg.display.flip()

    def wait_for_key(self):
        """Represents part of start game element
        Wait for key at start
        """
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False

    def draw_text(self, text, size, color, position):
        """Represents an drawing text

        :param text: Message, wich will be display on screen.
        :param size: Size of font
        :param position: Tuple which contains left corner x,y position.
        :param color: Text's color
        """
        font_name = pg.font.match_font(FONT_NAME)
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (position.x, position.y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        """Represents a start panel in start screen
        """
        pg.mixer.music.load(SOUNDS_DIR + SOUNDS['intro'])
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, Vec(WIDTH / 2, HEIGHT / 4))
        self.draw_text("Click, KeyUP or Space to jump", 22, WHITE, Vec(WIDTH / 2, HEIGHT / 2))
        self.draw_text("Press a key to play", 22, WHITE, Vec(WIDTH / 2, HEIGHT * 3 / 4))
        self.draw_text("High Score: " + str(get_high_score()), 22, WHITE, Vec(WIDTH / 2, 15))
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        """Represents game-over and continue screen
        """

        if not self.running:
            return
        pg.mixer.music.load(SOUNDS_DIR + SOUNDS['intro'])
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, Vec(WIDTH / 2, HEIGHT / 4))
        self.draw_text("Score: " + str(self.score), 22, WHITE, Vec(WIDTH / 2, HEIGHT / 2))
        self.draw_text("Press a key to play again", 22, WHITE, Vec(WIDTH / 2, HEIGHT * 3 / 4))
        high_score = get_high_score()
        if self.score > high_score:
            high_score = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, Vec(WIDTH / 2, HEIGHT / 2 + 40))
            with open(HS_FILE, 'w') as file:
                file.write(str(high_score))
        else:
            self.draw_text("High Score: " + str(high_score), 22, WHITE,
                           Vec(WIDTH / 2, HEIGHT / 2 + 40))
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()
