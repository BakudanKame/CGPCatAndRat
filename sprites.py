"""
Sprites used in the game: the rat and the pipe.
"""
import enum
import numpy as np
import math

import pygame as pg

from settings import *
from os import path


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
        self.damping = -5
        self.flag = True


    def update(self, *args):
        # check whether the rat flies outside the boundary
        # whether it hits a pipe
        if self.score > 3600:
            self.kill()
            return
         
            
        self.rk4_step()
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if self.rect.right > SCREEN_WIDTH:
        	self.rect.x = self.rect.x - SCREEN_WIDTH
        if self.rect.x < 0:
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


    def goRight(self):
        self.strat_force_x = 1100
    
    def goLeft(self):
	    self.strat_force_x = -1100
	    
    def goUp(self):
	    self.strat_force_y = 1100
		
    def goDown(self):
	    self.strat_force_y = -1100
	 
    def stopX(self):
        self.strat_force_x = 0
	
    def stopY(self):
        self.strat_force_y = 0

	    
    def vel_func(self, positions, velocities, time):
        velocities = np.array([self._vel_x, self._vel_y])
        return velocities

    def accel_func(self, positions, velocities, time):
        # potential_forces = self.environment.get_env_forces(positions)
        if self.strat_force_x != 0 and self.strat_force_y != 0:
            theta = math.atan2(self.strat_force_y, self.strat_force_x)
            self.strat_force_x = 1100 * math.cos(theta)
            self.strat_force_y = 1100 * math.sin(theta)
            print("HERE!")

        
        strategy_forces = np.array([self.strat_force_x, self.strat_force_y])
        damping_forces = self.damping * self.vel_func(positions, velocities, time)
        total_forces = strategy_forces + damping_forces
        magnitude = math.sqrt(total_forces[0]**2 + total_forces[1]**2)
        accelerations = total_forces / self.m
        return accelerations

    def rk4_step(self):
        current_positions = np.array([self.rect.x, self.rect.y])
        current_velocities = np.array([self._vel_x, self._vel_y])
        # numerics to calculate coefficients:
        pos_k1 = self.dt * self.vel_func(current_positions, current_velocities, self.t)
        vel_k1 = self.dt * self.accel_func(current_positions, current_velocities, self.t)
        pos_k2 = self.dt * self.vel_func(current_positions + (pos_k1 / 2), current_velocities + (vel_k1 / 2 ), self.t + (self.dt / 2))
        vel_k2 = self.dt * self.accel_func(current_positions + (pos_k1 / 2), current_velocities + (vel_k1 / 2), self.t + (self.dt / 2))
        pos_k3 = self.dt * self.vel_func(current_positions + (pos_k2 / 2), current_velocities + (vel_k2 / 2), self.t + (self.dt / 2))
        vel_k3 = self.dt * self.accel_func(current_positions + (pos_k2 / 2), current_velocities + (vel_k2 / 2), self.t + (self.dt / 2))
        pos_k4 = self.dt * self.vel_func(current_positions + pos_k3, current_velocities + vel_k3, self.t + self.dt)
        vel_k4 = self.dt * self.accel_func(current_positions + pos_k3, current_velocities + vel_k3, self.t + self.dt)
        # update according to rk4 formula:
        new_positions = current_positions + ((1/6) * (pos_k1 + 2*pos_k2 + 2*pos_k3 + pos_k4))
        new_velocites = current_velocities + ((1/6) * (vel_k1 + 2*vel_k2 + 2*vel_k3 + vel_k4))
        # load new values into instance attributes:
        self.rect.x, self.rect.y = new_positions[0], new_positions[1]
        self._vel_x = new_velocites[0]
        self._vel_y = new_velocites[1]
        self.t += self.dt

    
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
            
        self.rk4_step()
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if self.rect.right > SCREEN_WIDTH:
        	self.rect.x = self.rect.x - SCREEN_WIDTH
        if self.rect.x < 0:
        	self.rect.x = SCREEN_WIDTH + self.rect.x
        if self.rect.top > SCREEN_HEIGHT:
        	self.rect.y = self.rect.y - SCREEN_HEIGHT
        if self.rect.bottom < 0:
        	self.rect.y = SCREEN_HEIGHT + self.rect.y
        	
        if pg.sprite.spritecollideany(self, self._game.cats):
            if self.number == pg.sprite.spritecollideany(self, self._game.cats).number:
                self.flag = False
                return


    def goRight(self):
        self.strat_force_x = 800
    
    def goLeft(self):
	    self.strat_force_x = -800
	    
    def goUp(self):
	    self.strat_force_y = -800
		
    def goDown(self):
	    self.strat_force_y = 800
	    
    def stopX(self):
        self.strat_force_x = 0
	
    def stopY(self):
        self.strat_force_y = 0
		
	    
    def vel_func(self, positions, velocities, time):
        velocities = np.array([self._vel_x, self._vel_y])
        return velocities

    def accel_func(self, positions, velocities, time):
        # potential_forces = self.environment.get_env_forces(positions)
        if self.strat_force_x != 0 and self.strat_force_y != 0:
            theta = math.atan2(self.strat_force_y, self.strat_force_x)
            self.strat_force_x = 1100 * math.cos(theta)
            self.strat_force_y = 1100 * math.sin(theta)
            
        strategy_forces = np.array([self.strat_force_x, self.strat_force_y])
        damping_forces = self.damping * self.vel_func(positions, velocities, time)
        total_forces = strategy_forces + damping_forces
        magnitude = math.sqrt(total_forces[0]**2 + total_forces[1]**2)
        accelerations = total_forces / self.m
        return accelerations

    def rk4_step(self):
        current_positions = np.array([self.rect.x, self.rect.y])
        current_velocities = np.array([self._vel_x, self._vel_y])
        # numerics to calculate coefficients:
        pos_k1 = self.dt * self.vel_func(current_positions, current_velocities, self.t)
        vel_k1 = self.dt * self.accel_func(current_positions, current_velocities, self.t)
        pos_k2 = self.dt * self.vel_func(current_positions + (pos_k1 / 2), current_velocities + (vel_k1 / 2 ), self.t + (self.dt / 2))
        vel_k2 = self.dt * self.accel_func(current_positions + (pos_k1 / 2), current_velocities + (vel_k1 / 2), self.t + (self.dt / 2))
        pos_k3 = self.dt * self.vel_func(current_positions + (pos_k2 / 2), current_velocities + (vel_k2 / 2), self.t + (self.dt / 2))
        vel_k3 = self.dt * self.accel_func(current_positions + (pos_k2 / 2), current_velocities + (vel_k2 / 2), self.t + (self.dt / 2))
        pos_k4 = self.dt * self.vel_func(current_positions + pos_k3, current_velocities + vel_k3, self.t + self.dt)
        vel_k4 = self.dt * self.accel_func(current_positions + pos_k3, current_velocities + vel_k3, self.t + self.dt)
        # update according to rk4 formula:
        new_positions = current_positions + ((1/6) * (pos_k1 + 2*pos_k2 + 2*pos_k3 + pos_k4))
        new_velocites = current_velocities + ((1/6) * (vel_k1 + 2*vel_k2 + 2*vel_k3 + vel_k4))
        # load new values into instance attributes:
        self.rect.x, self.rect.y = new_positions[0], new_positions[1]
        self._vel_x, self._vel_y = new_velocites[0], new_velocites[1]
        self.t += self.dt

    

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
        






