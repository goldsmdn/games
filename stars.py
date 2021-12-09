import pygame
from pygame.sprite import Sprite
from random import random

#from settings import Settings

class Stars(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ll_game):
        """~Create a star object at a random position"""
        super().__init__()
        self.screen = ll_game.screen
        self.settings = ll_game.settings
        self.color = self.settings.star_color
        self.screen_rect = self.screen.get_rect()
        
        #screen_center_x, screen_center_y = self.screen_rect.center
        self.rect = pygame.Rect(0, 0, self.settings.star_width, self.settings.star_height)
        #position in the middle of the screen
        self.rect.center = self.screen_rect.center
        #store star position as a decimal point
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        #move to a random position on the screen
        self.x *= 2 * random()
        self.y *= 2 * random()
        self.rect.x, self.rect.y = self.x, self.y

    def draw_star(self):
        """Draw the stars on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
    


