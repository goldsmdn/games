from random import random
import pygame
from scoreboard import Scoreboard
from settings import Settings
from lander import Lander
from game_stats import GameStats
from sound_and_music import SoundAndMusic
from surface import Surface
from stars import Stars
from panel import Panel
from instruments import Instruments

class LunarLander:
    """Overall call to manage game assets and behaviour."""
    def __init__(self):
        """Initialise the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Lunar Landing")   

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound_and_music = SoundAndMusic()
        self.lander = Lander(self)
        self.lander.start()
        self.surface_left = Surface(self, 'left')
        self.surface_site = Surface(self, 'site')
        self.surface_right = Surface(self, 'right')
        self.surfaces = [self.surface_left,
                    self.surface_site,
                    self.surface_right]
        self.stars = []
        for count in range(0, self.settings.star_number):
            #add stars at random places
            self.star = Stars(self)
            self.stars.append(self.star)
        self.panel = Panel(self)
        self.instrument = Instruments(self)
        self.has_landed = False
        self.has_crashed = False
        self.done = False
        self.score = 0

    def _run_loop(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if not self.has_crashed and not self.has_landed:    
                self.lander.update_position()
                self.lander.update_fuel()
                self.instrument.update_texts(self.lander.fuel, 
                                             self.lander.height, 
                                             self.lander.vx, 
                                             self.lander.vy
                                             )
                self._check_land() 
                self._check_crash()
                self._make_rocket_sounds()
                self._make_squawk()
            self._update_screen()
            if self.done:
                if self.has_landed:
                    self.score = self._calculate_score()
                    self.sb._final_score_update()
                    pygame.time.wait(6000)
                elif self.has_crashed:
                    self.score = 0
                    self.sb._final_score_update()
                    pygame.time.wait(6000)
                else:   
                    self.score = 0
                return self.score
            
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_crash(self):
        """detects crash"""  
        if not self.has_landed:
            #can't crash and land at the same time
            if self.lander.rect.colliderect(self.surface_right.rect):
                self._handle_crash()
            elif self.lander.rect.colliderect(self.surface_left.rect):
                self._handle_crash()

    def _check_land(self):
        """detects landed"""    
        if self.lander.rect.colliderect(self.surface_site.rect):
            if abs(self.lander.vx) < self.settings.lander_final_vx:
                if abs(self.lander.vy) < self.settings.lander_final_vy:
                    self._handle_land()
                else:
                    self._handle_crash()
            else:
                self._handle_crash()

    def _handle_crash(self):
        """shows crash image and makes crash sounds"""
        self.has_crashed = True
        self.lander.update_crashed_image()
        #wait for 200 ms for other noises to finish
        pygame.time.wait(200)
        self.sound_and_music.make_sound('explosion')
        self.done = True
        
    def _handle_land(self):
        """shows landing image and makes landing sounds"""
        self.has_landed = True
        self.lander.update_landed_image()
        #wait for 200 ms for other noises to finish
        pygame.time.wait(200)
        self.sound_and_music.make_sound('landed')
        self.done = True
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.dark_color)
        for self.star in self.stars:
            self.star.draw_star()
        self.panel.blitme()
        self.instrument.blitme()
        if not self.has_landed and not self.has_crashed:
            self.lander.update_image()
        self.lander.blitme()
        self.surface_left.blitme()
        self.surface_site.blitme()
        self.surface_right.blitme()
        #Make the most recently drawn screen visible.
        pygame.display.flip()

    def _make_rocket_sounds(self):
        """different sounds for main and thruster rockets"""
        if not self.has_crashed and not self.has_landed:
            if self.lander.rocket_down == 1: 
                self.sound_and_music.make_sound('rocket')
            elif self.lander.rocket_lateral == 1 or self.lander.rocket_lateral == -1:
                self.sound_and_music.make_sound('thruster')
    
    def _make_squawk(self):
        """generate a squawk a random fraction of the time"""
        if random() < self.settings.squawk_fraction:
            self.sound_and_music.make_sound('squawk')

    def _check_keydown_events(self, event):
        """acts on relevant for key presses"""
        if self.lander.fuel > 0:
            #can only fire rockets with fuel
            if event.key == pygame.K_RIGHT:
                #Fire rockets to the right
                self.lander.rocket_lateral = 1
            elif event.key == pygame.K_LEFT:
                #Fire rockets to the left
                self.lander.rocket_lateral = -1
            elif event.key == pygame.K_UP:
                #Fire rockets down
                self.lander.rocket_down = 1
            elif event.key == pygame.K_SPACE:
                #Fire rockets down
                self.lander.rocket_down = 1
        if event.key == pygame.K_q:
            self.done = True
        elif event.key == pygame.K_ESCAPE:
            self.done = True

    def _check_keyup_events(self, event):
        """acts on relevant for key releases"""
        if event.key == pygame.K_RIGHT:
            self.lander.rocket_lateral = 0
        elif event.key == pygame.K_LEFT:
            self.lander.rocket_lateral = 0
        elif event.key == pygame.K_UP:
            self.lander.rocket_down = 0
        elif event.key == pygame.K_SPACE:
            #Fire rockets down
            self.lander.rocket_down = 0

    def _calculate_score(self):
        """score depends on fuel and residual velocity"""
        base_score = self.settings.lander_base_score
        fuel_score = int(self.lander.fuel * self.settings.lander_fuel_multiplier)
        vx_score = int(self.lander.vx * self.settings.lander_vx_multiplier)
        vy_score = int(self.lander.vy * self.settings.lander_vy_multiplier)
        self.stats.score = base_score + fuel_score - vx_score - vy_score
        return self.stats.score
