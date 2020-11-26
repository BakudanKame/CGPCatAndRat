"""
The main flappy rat game.
"""
import random
from enum import Enum

import os.path
import os
import js2py

js2py.translate_file('proNav.js', 'proNav.py')

from proNav import proNav


import cgp
from sprites import *


class GameMode(Enum):
    PLAYER = 0
    GP = 1
    VS = 2  # human player vs. GP


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '200,300'
        pg.mixer.pre_init()
        pg.mixer.init()
        pg.init()
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self._clock = pg.time.Clock()
        self._is_paused = False
        self._fps = FPS
        self.music_on = False

        self._rat_image = None
        self._background_image = None
        self._cat_image = None


        self.all_sprites = pg.sprite.LayeredUpdates()
        self.rats = pg.sprite.Group()
        self.cats = pg.sprite.Group()
        self._load_images()
        self._human_rat = None

        self.running = True
        self.playing = False

        # CGP settings
        self.n_rats = MU + LAMBDA
        self.n_cats = self.n_rats
        self._max_score_so_far = 0  # max score so far in all the rounds since the game started
        self._max_score = 0  # max score of all the rats in this round (generation)
        self.current_generation = 0

        # create the initial population
        self.pop = cgp.create_population(self.n_rats)

    def reset(self):
        if VERBOSE:
            print(f'--------Generation: {self.current_generation}. Max score so far: {self._max_score_so_far}-------')
        self._max_score = 0
        self.current_generation += 1
        # empty all the current sprites if any
        for s in self.all_sprites:
            s.kill()
        # instantiate rats
        for i in range(self.n_rats):
            x = random.randint(1, 800)
            y = random.randint(1, 600)
            AIRat(self, self._rat_image, x, y, self.pop[i], i)
            AICat(self, self._cat_image, random.randint(1,800), random.randint(1,600), i)
        # instantiate the pipes
        # the first pipe with xas the baseline
        # create the background
        Background(self, self._background_image)

    def _load_images(self):
        """
        Load images
        """

        def _load_one_image(file_name):
            return pg.image.load(os.path.join(IMG_DIR, file_name)).convert_alpha()

        self._rat_image = _load_one_image('bird.png')
        self._cat_image = _load_one_image('cat.png')
        self._background_image = _load_one_image('background.png')
        self._blue_bird_image = _load_one_image('bluebird.png')


    def run(self):
        self.playing = True
        while self.playing:
            self._handle_events()
            self._update()
            self._draw()
            self._clock.tick(self._fps)
        if not self.running:
            return
        # one generation finished and perform evolution again
        # if current score is very low, then we use a large mutation rate
        pb = MUT_PB
        if self._max_score < 500:
            pb = MUT_PB * 3
        elif self._max_score < 1000:
            pb = MUT_PB * 2
        elif self._max_score < 2000:
            pb = MUT_PB * 1.5
        elif self._max_score < 5000:
            pb = MUT_PB * 1.2
        self.pop = cgp.evolve(self.pop, pb, MU, LAMBDA)

    def _pause(self):
        """
        Pause the game (ctrl + p to continue)
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.playing = False
                    self.running = False
                    return
                if event.type == pg.KEYDOWN:
                    pressed = pg.key.get_pressed()
                    ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
                    if ctrl_held and event.key == pg.K_p:
                        self._is_paused = False
                        return
                self._draw_text("Paused", x=SCREEN_WIDTH // 2 - 50, y=SCREEN_HEIGHT // 2 - 10,
                                color=WHITE, size=2 * FONT_SIZE)
                pg.display.update()
                pg.time.wait(50)


    def _handle_events(self):
        """
        Handle key events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                pressed = pg.key.get_pressed()
                ctrl_held = pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]
                if ctrl_held:
                    if event.key == pg.K_p:  # ctrl + p: pause the game
                        self._is_paused = True
                        self._pause()
                    elif event.key == pg.K_1:  # ctrl + 1 (2, 3): standard frame rate
                        self._fps = FPS
                    elif event.key == pg.K_2:
                        self._fps = 2 * FPS
                    elif event.key == pg.K_3:
                        self._fps = 3 * FPS
                    
        for rat in self.rats:
            if rat is not self._human_rat:
                self.try_flap(rat)

        for cat in self.cats:
            self.chaseRat(cat)





    def _checkToroidalDistance(self, cat, rat):
        separation = abs(cat.rect.x - rat.rect.x)
        if separation > 0.5 * SCREEN_WIDTH:
            separation = SCREEN_WIDTH - separation

        return separation

    def try_flap(self, rat):
        """
        Compute the rat angle if needed
        """
        # compute the three inputs: v, h, g
        for cat in self.cats:
            if cat.number == rat.number:
                nearestCat = cat

        try:
            
            x = nearestCat.rect.x - rat.rect.x
            y = nearestCat.rect.y - rat.rect.y

            if x > SCREEN_WIDTH/2:
                x = x - SCREEN_WIDTH
            elif x < -SCREEN_WIDTH/2:
                x = x + SCREEN_WIDTH

            if y > SCREEN_HEIGHT/2:
                y = y - SCREEN_HEIGHT
            elif y < -SCREEN_HEIGHT/2:
                y = y + SCREEN_HEIGHT

            angle = math.atan2(y, x) + math.pi


            xEval = rat.eval(x, y, angle)
            if rat.number ==1:
                print(rat.eval(x, y, angle))

            xEval = xEval % (2 * math.pi)

            if xEval < 0:
                xEval = xEval + 2 * math.pi

            rat.strat_force_x = 1100 * math.cos(xEval)
            rat.strat_force_y = 1100 * math.sin(xEval)


        except:
            return

    def chaseRat(self, cat):

        for rat in self.rats:
            if rat.number == cat.number:
                nearestRat = rat
                
        try:
            if cat.score == 0:
                thrustVectors = proNav.catStrat4(cat.rect.x, cat.rect.y, nearestRat.rect.x, nearestRat.rect.y, SCREEN_WIDTH, SCREEN_HEIGHT, nearestRat.strat_force_x, nearestRat.strat_force_y, 800, 10, 0, 1)
                global oldLOSAng
                oldLOSAng = thrustVectors[2]
                global oldLOSLen
                oldLOSLen = thrustVectors[3]
                
                cat.strat_force_x = thrustVectors[0]
                cat.strat_force_y = thrustVectors[1]
                
            else:
                thrustVectors = proNav.catStrat4(cat.rect.x, cat.rect.y, nearestRat.rect.x, nearestRat.rect.y, SCREEN_WIDTH, SCREEN_HEIGHT, nearestRat.strat_force_x, nearestRat.strat_force_y, 800, oldLOSAng, oldLOSLen, 2)
                oldLOSAng = thrustVectors[2]
                oldLOSLen = thrustVectors[3]
                
                cat.strat_force_x = thrustVectors[0]
                cat.strat_force_y = thrustVectors[1]

        
            
            
            
        except:
            cat.strat_force_x = 0
            cat.strat_force_y = 0
            cat._vel_x = 0
            cat._vel_y = 0
            cat.kill()






        return


    def _update(self):
        """
        Update the state (position, life, etc.) of all sprites and the game
        """
        self.all_sprites.update()

        # if all rats died, then game over
        if not self.rats:
            self.playing = False
            return
        # move the pipes backwards such that rats seem to fly


        # count the score: one point per frame
        for rat in self.rats:
            rat.score += 1  # when a rat dies, its score will be set to the CGP individual's fitness automatically

        self._max_score += 1
        self._max_score_so_far = max(self._max_score_so_far, self._max_score)
        # spawn a new pipe if necessary

    def _draw(self):
        self.all_sprites.draw(self._screen)
        # show score
        self._draw_text('Score: {}'.format(self._max_score), 10, 10)
        self._draw_text('Max score so far: {}'.format(self._max_score_so_far), 10, 10 + FONT_SIZE + 2)
        self._draw_text('Generation: {}'.format(self.current_generation), 10, 10 + 2 * (FONT_SIZE + 2))
        n_alive = len(self.rats)
        if self._human_rat is not None and self._human_rat.alive():
            n_alive -= 1
        self._draw_text('Alive: {} / {}'.format(n_alive, self.n_rats), 10, 10 + 3 * (FONT_SIZE + 2))
        pg.display.update()

    def _draw_text(self, text, x, y, color=WHITE, font=FONT_NAME, size=FONT_SIZE):
        font = pg.font.SysFont(font, size)
        text_surface = font.render(text, True, color)
        self._screen.blit(text_surface, (x, y))
