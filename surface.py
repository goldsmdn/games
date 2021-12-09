import pygame


class Surface:
    """A class to manage the surfaces"""

    def __init__(self, ll_game, type):
        """Initialise the three surfaces and set its starting properties."""
        self.screen = ll_game.screen
        self.settings = ll_game.settings
        self.screen_rect = ll_game.screen.get_rect()
        image_dictionary = {'left': 'images/lunar_left.bmp',
                            'site' : 'images/lunar_landing_site.bmp',
                            'right' : 'images/lunar_right.bmp',}
        self.image = pygame.image.load(image_dictionary[type])
        self.rect = self.image.get_rect()
        #print

        if type == 'left':
            self.rect.bottomleft = self.screen_rect.bottomleft
        if type == 'site':
            self.rect.midbottom = self.screen_rect.midbottom
        if type == 'right':
            self.rect.bottomright = self.screen_rect.bottomright
        
    def blitme (self):
        """Draw the surface at its current_location"""
        self.screen.blit(self.image, self.rect)