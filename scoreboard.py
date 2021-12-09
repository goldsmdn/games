import pygame.font

class Scoreboard:
    """A call to report scoring information."""

    def __init__(self, ai_game):
        """Initialise scorekeeping attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.offset = self.settings.scoreboard_offset
        self.text_color = self.settings.scoreboard_text_color
        self.score_string = ''
        
        #Font settings for scoring information.
        self.font_size = self.settings.scoreboard_font_size
        self.font = pygame.font.SysFont(None, self.font_size)
        
        #Prepare the initial score image.
        self._prep_score()
        self._display_score()
        
    def _prep_score(self, final=False):
        """Turn the score into a rendered image."""
        self.score_str = str(self.stats.score)
        if final:
            self.score_str = "Final score is : " + self.score_str
        self.score_image = self.font.render(self.score_str, True,
                self.text_color, self.settings.bg_color)
    
    def _display_score(self, final=False):
        """Display the score at the top right of the screen, or in center"""
        self.score_rect = self.score_image.get_rect()    
        if final:
            self.score_rect.center = self.screen_rect.center
        else:
            self.score_rect.right = self.screen_rect.right - self.offset
            self.score_rect.top = 20

    def _show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)

    def _final_score_update(self):
        self._prep_score(final=True)
        self._display_score(final=True)
        self._show_score()
        #Make the score visible.
        pygame.display.flip()