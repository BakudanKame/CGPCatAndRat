"""
Sprites used in the game: the rat and the pipe.
"""
import enum
import numpy as np
import math
import js2py

import pygame as pg

from settings import *
from os import path

js2py.translate_file('CGP.js', 'js.py')

from js import js


class MovableSprite(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = None

    def moveto(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y

    def moveby(self, dx=0, dy=0):
        self.rect.move_ip(dx, dy)


class Rat(MovableSprite):
    def __init__(self, game, image: pg.Surface, x, y, number):
        self._layer = 2  # required for pygame.sprite.LayeredUpdates: set before adding it to the group!
        super().__init__(game.all_sprites, game.rats)
        self._game = game
        self.image = image
        self.origin_image = self.image
        self.rect = image.get_rect(x=x, y=y)
        self.accel = 0
        self._vel_x = 0
        self._vel_y = 0
        self.score = 0
        self.number = number
        self.dt = (1/60)
        self.t = 0
        self.strat_force_x = 0
        self.strat_force_y = 0
        self.m = 1
        self.damping = 5
        self.flag = True


    def update(self, *args):
        # check whether the rat flies outside the boundary
        # whether it hits a pipe
        if self.score > 3600:
            self.kill()
            return
         
            
        posVelArray = js.rk4(self.rect.x, self.rect.y, self.strat_force_x, self.strat_force_y, self.damping, self._vel_x, self._vel_y)
        
        self.rect.x = posVelArray[0]
        self.rect.y = posVelArray[1]
        self._vel_x = posVelArray[2]
        self._vel_y = posVelArray[3]
        
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if self.rect.right > SCREEN_WIDTH:
        	self.rect.x = self.rect.x - SCREEN_WIDTH
        if self.rect.left < 0:
        	self.rect.x = SCREEN_WIDTH + self.rect.x
        if self.rect.top > SCREEN_HEIGHT:
        	self.rect.y = self.rect.y - SCREEN_HEIGHT
        if self.rect.bottom < 0:
        	self.rect.y = SCREEN_HEIGHT + self.rect.y
        
        if pg.sprite.spritecollideany(self, self._game.cats):
            if self.number == pg.sprite.spritecollideany(self, self._game.cats).number:
                self.flag = False
                self.kill()
                return

    
    @property
    def vel_x(self):
        return self._vel_x
    
    @property
    def vel_y(self):
        return self._vel_y
        
class Cat(MovableSprite):
    def __init__(self, game, image: pg.Surface, x, y, number):
        self._layer = 2  # required for pygame.sprite.LayeredUpdates: set before adding it to the group!
        super().__init__(game.all_sprites, game.cats)
        self._game = game
        self.image = image
        self.origin_image = self.image
        self.rect = image.get_rect(x=x, y=y)
        self.number = number
        self.accel = 0
        self._vel_x = 0
        self._vel_y = 0
        self.score = 0
        self.dt = (1/60)
        self.t = 0
        self.strat_force_x = 0
        self.strat_force_y = 0
        self.m = 1
        self.damping = -2
        self.flag = True

    def update(self, *args):
        # check whether the rat flies outside the boundary
        # whether it hits a pipe
        if self.score > 3600:
            self.kill()
            return
            
        posVelArray = js.rk4(self.rect.x, self.rect.y, self.strat_force_x, self.strat_force_y, self.damping, self._vel_x, self._vel_y)
        
        self.rect.x = posVelArray[0]
        self.rect.y = posVelArray[1]
        self._vel_x = posVelArray[2]
        self._vel_y = posVelArray[3]
        
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if self.rect.right > SCREEN_WIDTH:
        	self.rect.x = self.rect.x - SCREEN_WIDTH
        if self.rect.left < 0:
        	self.rect.x = SCREEN_WIDTH + self.rect.x
        if self.rect.top > SCREEN_HEIGHT:
        	self.rect.y = self.rect.y - SCREEN_HEIGHT
        if self.rect.bottom < 0:
        	self.rect.y = SCREEN_HEIGHT + self.rect.y
        	
        if pg.sprite.spritecollideany(self, self._game.cats):
            if self.number == pg.sprite.spritecollideany(self, self._game.cats).number:
                self.flag = False
                return
    
    @property
    def vel_x(self):
        return self._vel_x
    
    @property
    def vel_y(self):
        return self._vel_y


class AIRat(Rat):
    def __init__(self, game, image: pg.Surface, x, y, brain, number):
        super().__init__(game, image, x, y, number)
        self.brain = brain

    def kill(self):
        super().kill()
        self.brain.fitness = self.score

    def eval(self, v, h, g):
        return self.brain.eval(v, h, g)
        
    def save(self):
	    return self.brain.save()
        
class AICat(Cat):
    def __init__(self, game, image: pg.Surface, x, y, number):
        super().__init__(game, image, x, y, number)

    def kill(self):
        super().kill()




class Background(pg.sprite.Sprite):
    """
    Seamless background class.
    """
    def __init__(self, game, image):
        self._layer = 0
        super().__init__(game.all_sprites)
        # if the width of the given image < screen width, then repeat it until we get a wide enough one
        if image.get_width() < SCREEN_WIDTH:
            w = image.get_width()
            repeats = SCREEN_WIDTH // w + 1
            self.image = pg.Surface((w * repeats, image.get_height()))
            for i in range(repeats):
                self.image.blit(image, (i * w, 0))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        






