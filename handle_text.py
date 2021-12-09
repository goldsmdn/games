import pygame
from settings import Settings


class HandleText:
    """overall class to get text"""
    def __init__(self, prompt):
        """Initialise the screen, and create game resources"""
        self.prompt = prompt
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.Font(None, self.settings.default_font_size )
        pygame.display.set_caption("Festive games") 
        self.user_text = ''
        self.text_images = []
        self.done = False
        self.count = 0

        self.text_color = self.settings.default_text_color
        self.background_color = self.settings.text_background_color
        self.start_down = self.settings.text_start_offset_down
        self.inc_down = self.settings.text_incremental_offset_down
        self.start_right = self.settings.text_start_offset_right
        self.text_width = self.settings.text_width
        self.text_spare_width = self.settings.text_spare_width
        self.text_extra_space = self.settings.text_extra_space
        self.text_max_width = self.settings.text_max_width
        self.text_height = self.settings.text_height
        self.box_color = self.settings.text_box_color

    def _run_loop(self):
        """main program loop"""
        self._display_fixed_text()
        while True:
            self._check_events()
            self._display_input_box()
            self._update_screen()
            if self.done == True:
                return self.user_text

    def _check_events(self):
        """checks for relevant events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.user_text = ''
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.done = True
                else:
                    self.user_text += event.unicode

    def _display_fixed_text(self):
        """render text to an image"""
        for line in self.prompt:
            self.text = self.font.render(line, True,
                self.text_color, self.background_color)
            self.text_images.append(self.text)

    def _display_input_box(self):
        """display the text image"""
        x = self.screen_rect.left + self.start_right
        y = self.screen_rect.top + self.start_down + self.inc_down * self.count
        self.input_rect = pygame.Rect(x, y, self.text_width, self.text_height)
        self.text_surface = self.font.render(self.user_text, True,
                self.text_color, self.background_color)
        self.input_rect.w = max(
            self.text_surface.get_width() + self.text_spare_width, 
            self.text_max_width
            )

    def _update_screen(self):
        """update the screen for the images"""
        self.screen.fill(self.settings.text_background_color)
        pygame.draw.rect(self.screen, self.box_color, self.input_rect, 2)
        self.count = 0
        for image in self.text_images:         
            text_rect = image.get_rect()
            text_rect.left = self.screen_rect.left + self.start_right
            text_rect.top = self.screen_rect.top + self.start_down + self.inc_down * self.count
            self.count += 1
            self.screen.blit(image, text_rect)
        self.screen.blit(self.text_surface, 
                            (self.input_rect.x + self.text_extra_space, 
                             self.input_rect.y + self.text_extra_space
                             )
                         )
        pygame.display.flip()
        

            