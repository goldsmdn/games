import pygame
#from sound_and_music import Sound


class Lander:
    """A class to manage the lander"""

    def __init__(self, ll_game):
        """Initialise the ship and set its starting properties."""
        self.screen = ll_game.screen
        self.settings = ll_game.settings
        self.screen_rect = self.screen.get_rect()

        # Load the lander image and get its rect.
        self.image = pygame.image.load('images/lander.bmp')
        self.rect = self.image.get_rect()

        #Store a decimal value for the lander's horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.fuel = self.settings.lander_initial_fuel
        self.height_offset = self.settings.lander_height_offset

    def start(self):
        """Start the lander at the top center of the screen."""
        self.rect.topleft = self.screen_rect.topleft

        #store the speed as the initial speed
        self.vx = float(self.settings.lander_initial_vx)
        self.vy = float(self.settings.lander_initial_vy)
        self.height = self.y - self.height_offset

        #rocket status
        self.rocket_down = 0
        self.rocket_lateral = 0

    def blitme (self):
        """Draw the lander at its current_location"""
        #print('blitme')
        self.screen.blit(self.image, self.rect)

    def update_crashed_image(self):
        """show explosion"""
        self.image = pygame.image.load('images/explosion.bmp') 
    
    def update_landed_image(self):
        """show normal lander"""
        self.image = pygame.image.load('images/lander.bmp')
    
    def update_image(self):
        """update the lander image based on flags set by key strokes"""
        if self.rocket_down == 0:
            if self.rocket_lateral == 1:
            #rocket moving to right, so pushed by jets on left
                self.image = pygame.image.load('images/lander_left.bmp')
            elif self.rocket_lateral == -1:
                self.image = pygame.image.load('images/lander_right.bmp')
            else:
                self.image = pygame.image.load('images/lander.bmp')
        elif self.rocket_down == 1:
            if self.rocket_lateral == 1:
            #rocket moving to right, so pushed by jets on left
                self.image = pygame.image.load('images/lander_below_left.bmp')
            elif self.rocket_lateral == -1:
                self.image = pygame.image.load('images/lander_below_right.bmp')
            else:
                self.image = pygame.image.load('images/lander_below.bmp')

    def update_position(self):
        """Update the landers's position based on the movement flag"""
        #update velocity based on acceleration from lunar gravity and thrusters. 
        if self.fuel > 0:
            self.thruster_acc = self.settings.lander_thruster_acc * self.rocket_lateral 
            self.rocket_acc = self.settings.lander_rocket_acc * self.rocket_down
        else:
            #if no fuel then no rockets or thrusters
            self.thruster_acc, self.rocket_acc = 0, 0
        self.vx += self.thruster_acc
        self.vy += (self.settings.lander_moon_acc + 
                    self.rocket_acc)
        self.x += self.vx
        self.y += self.vy
        self.height = - self.y + self.height_offset
        self.rect.x, self.rect.y = self.x, self.y

    def update_fuel(self):
        """update lander fuel"""
        if self.fuel > 0:
            self.fuel += (self.settings.lander_fuel_burn * (
                            self.rocket_acc - abs(self.thruster_acc)
                            )
                         )
        else:
            self.fuel = 0