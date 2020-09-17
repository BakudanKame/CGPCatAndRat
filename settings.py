"""
Define some constant parameters and program settings.
"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = 'Cat And Rat AI via Evolutionary Cartesian Genetic Programming'
FPS = 30
IMG_DIR = './img'
SND_DIR = './snd'
FONT_NAME = 'Arial'
FONT_SIZE = 20
WHITE = (255, 255, 255)

JUMP_SPEED = -3.5     # once the bird flaps, its speed becomes this value
GRAVITY_ACC = 0.35
BIRD_X_SPEED = 3   # the const horizontal speed of the bird
BIRD_MAX_Y_SPEED = 5    # the maximum downward speed

# horizontal space between two adjacent pairs of pipes


# parameters of cartesian genetic programming
MUT_PB = 0.015  # mutate probability
N_COLS = 500   # number of cols (nodes) in a single-row CGP
LEVEL_BACK = 500  # how many levels back are allowed for inputs in CGP

# parameters of evolutionary strategy: MU+LAMBDA
MU = 2
LAMBDA = 18
N_GEN = 200  # max number of generations

# if True, then additional information will be printed
VERBOSE = True
