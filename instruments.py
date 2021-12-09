import pygame


class Instruments:
    def __init__(self, ll_game):
        self.screen = ll_game.screen
        self.settings = ll_game.settings
        self.screen_rect = ll_game.screen.get_rect()
        self.font_size = self.settings.instrument_font_size
        self.text_color = self.settings.instrument_default_text
        self.background_color = self.settings.instrument_background_color
        self.font = pygame.font.SysFont(None, self.font_size)
        self.offset_down = self.settings.instrument_offset_down
        self.offset_left = self.settings.instrument_offset_left
        self.texts = {'Fuel'  : 'Fuel  : ',
                      'Height': 'Height: ',
                      'VX'    : 'VX    : ',
                      'VY'    : 'VY    : '}
        self.reading_images = []

    def blitme (self):
        """Draw the readings in the panel"""
        count = 0
        for image in self.reading_images:        
            reading_rect = image.get_rect()
            reading_rect.left = self.screen_rect.right - self.offset_left
            reading_rect.top = self.offset_down + count * self.settings.instrument_offset_text
            count = count + 1
            self.screen.blit(image, reading_rect)

    def update_texts(self, fuel, height, vx, vy):
        self.reading_images = []
        for key, items in self.texts.items():
            check_max = True
            if key == 'Fuel':
                limit = self.settings.lander_min_fuel
                check_max = False
                reading = fuel
            elif key == 'Height':
                limit = self.settings.lander_max_height
                reading = height
            elif key == 'VX':
                limit = self.settings.lander_max_vx
                reading = vx * self.settings.instrument_vx_multiplier
            elif key == 'VY':
                limit = self.settings.lander_max_vy
                reading = vy * self.settings.instrument_vy_multiplier
            else:
                raise Exception('Incorrect text in instruments')
            self.set_color(reading, limit, check_max)
            self.text = items + str(int(reading))

            self.reading_image = self.font.render(self.text, True,
                    self.text_color, self.background_color)
            self.reading_images.append(self.reading_image)

    def set_color(self, reading, limit, check_max):
        DANGER_COLOR = (241, 57, 29)
        WARNING_COLOR = (241, 174, 29)
        DEFAULT_COLOR = (60, 210, 29)
        if abs(reading) < limit / 2:
            if check_max:
                self.text_color = DEFAULT_COLOR
            else:
            #logic reversed if checking for a minimum
                self.text_color = DANGER_COLOR
        elif abs(reading) < limit:
            if check_max:
                self.text_color = WARNING_COLOR
            else:
                self.text_color = WARNING_COLOR
        else:
            if check_max:
                self.text_color = DANGER_COLOR
            else:
                self.text_color = DEFAULT_COLOR