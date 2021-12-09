import pygame.font


class Button:

    def __init__(self, ai_game, msg):
        """Initialies the button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        #Set the dimensions and properties of the button.
        self.width = self.settings.button_width
        self.height = self.settings.button_height
        self.color = self.settings.button_color
        self.text_color = self.settings.button_text_color
        self.text_size = self.settings.button_text_size
        self.font = pygame.font.SysFont(None, self.text_size)
       
        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):    
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, 
            self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message"""
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)