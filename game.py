"""
The main flappy rat game.
"""
import random
from enum import Enum

import os.path
import os

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
            x = random.randint(20, 200)
            y = i * 50
            AIRat(self, self._rat_image, x, y, self.pop[i], i)
            AICat(self, self._cat_image, x+200, y, i)
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


            x = nearestCat.rect.x

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
            x = cat.rect.x - nearestRat.rect.x
            y = cat.rect.y - nearestRat.rect.y

            if x > 0.5 * SCREEN_WIDTH:
                x = x - SCREEN_WIDTH
            elif x < -0.5 * SCREEN_WIDTH:
                x = x + SCREEN_WIDTH

            if y > 0.5 * SCREEN_HEIGHT:
                y = y - SCREEN_HEIGHT
            elif y < -0.5 * SCREEN_HEIGHT:
                y = y + SCREEN_HEIGHT


            angleToTarget = math.atan2(y, x)
            cat.stopX()
            cat.stopY()


            #Pro Nav Code 
            
            Lx = SCREEN_WIDTH
            Ly = SCREEN_HEIGHT
            N = 0.5

            nsep = (math.pow(x,2)+math.pow(y,2))/Lx/Ly
           
            

            if  cat.score == 0:
                print("working 2")
                losAngleOld = angleToTarget
                losAngleNew =  losAngleOld
                losLengthOld = nsep
                losLengthNew = losLengthOld
                print("working 3")
            else:
                losAngleOld = losAngleNew
                losAngleNew = angleToTarget
                losLengthOld = losLengthNew
                losLengthNew = nsep
                

            lineOfSight_rate = losAngleNew - losAngleOld

            closingVelocity =  losLengthOld - losLengthNew

            n_T = math.sqrt(nearestRat.strat_force_x ** 2 + nearestRat.strat_force_y ** 2) * math.cos(losAngleNew + (0.5 * math.pi) - math.atan2(nearestRat.strat_force_y, nearestRat.strat_force_x))

            print("working 4")
            
            if math.atan2(nearestRat.strat_force_y, nearestRat.strat_force_x) > losAngleNew:
                lateralAccelerationX = (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5)) * math.cos(losAngleNew + math.pi*0.5)
                lateralAccelerationY = (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5)) * math.sin(losAngleNew + math.pi*0.5)
            else:
                lateralAccelerationX = (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5)) * math.cos(losAngleNew - math.pi*0.5)
                lateralAccelerationY = (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5)) * math.sin(losAngleNew - math.pi*0.5)

            print("working 5")

            if (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5)) < 1100:
                losAccelerationX = (1100 - (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5))) * math.cos(losAngleNew + math.pi)
                losAccelerationY = (1100 - (N * lineOfSight_rate * closingVelocity + (N * n_T * 0.5))) * math.sin(losAngleNew + math.pi)
            else:
                losAccelerationX = 0
                losAccelerationY = 0

            print("working 6")

            cat.strat_force_x = lateralAccelerationX + losAccelerationX

            cat.strat_force_y = lateralAccelerationY + losAccelerationY
            
            print("working 7")
            
            '''
            
            #CLOS CODE

            cat.strat_force_x = 800 * math.cos(angleToTarget)

            cat.strat_force_y = 800 * math.sin(angleToTarget)
            '''
      

            '''
            #Digitized CLOS Code
            if angleToTarget > math.pi * (1/8) and angleToTarget < math.pi * (3/8):
                cat.goUp()
                cat.goRight()
            elif angleToTarget > math.pi * (3/8) and angleToTarget < math.pi * (5/8):
                cat.goUp()
            elif angleToTarget > math.pi * (5/8) and angleToTarget < math.pi * (7/8):
                cat.goUp()
                cat.goLeft()
            elif angleToTarget < math.pi * (-1/8) and angleToTarget > math.pi * (-3/8):
                cat.goDown()
                cat.goRight()
            elif angleToTarget < math.pi * (-3/8) and angleToTarget > math.pi * (-5/8):
                cat.goDown()
            elif angleToTarget < math.pi * (-5/8) and angleToTarget > math.pi * (-7/8):
                cat.goDown()
                cat.goLeft()
            elif angleToTarget < math.pi * (1/8) and angleToTarget > math.pi * (-1/8):
                cat.goRight()
            else:
                cat.goLeft()

             '''

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
            if rat.score > self._max_score_so_far:
                rat.save()

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
