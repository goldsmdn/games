import pygame

class Panel:
    """instrument panel for lander"""
    def __init__(self, ll_game):
        """initialise panel"""
        self.screen = ll_game.screen
        self.settings = ll_game.settings
        self.screen_rect = ll_game.screen.get_rect()
        self.image_file = 'images/panel.bmp'
        self.image = pygame.image.load(self.image_file)
        self.rect = self.image.get_rect()
        self.rect.topright = self.screen_rect.topright

    def blitme (self):
        """Draw the panel at its current_location"""
        self.screen.blit(self.image, self.rect)