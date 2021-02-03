"""
    settings.py
    settings for game
"""

# game options
TITLE = "Flappy Bird"
WIDTH = 480
HEIGHT = 512
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"

# player settings
PLAYER_GRAV = 0.5
PLAYER_JUMP = 8
PIPE_FREQUENCY = 5000

# define colors
WHITE = (255, 255, 255)
BG_COLOR = (21, 98, 98)

# out files
IMAGES_DIR = 'images/'
IMAGES = {
    'background': 'background.png',
    'pipe-end': 'pipe_end.png',
    'pipe-body': 'pipe_body.png',
    'bird-wing-up': 'bird_wing_up.png',
    'bird-wing-down': 'bird_wing_down.png',
}

SOUNDS_DIR = 'sounds/'
SOUNDS = {
    'jump': 'wing.mp3',
    'intro': 'intro.ogg',
    'point': 'point.mp3',
    'die': 'die.mp3',
    'hit': 'hit.mp3'
}
