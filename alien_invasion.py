#import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullets import Bullet
from alien import Alien
from game_stats import GameStats
from sound_and_music import SoundAndMusic
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overal call to manage game assets and behaviour."""

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
        pygame.display.set_caption("Alien Invasion")   
        #Create an instance to store game statistics,
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound_and_music = SoundAndMusic()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #Flag to handle termination
        self.done = False
        # Make the Play button.
        self.play_button = Button(self, "Play")

    def _run_loop(self):
        """Start the main loop for the game"""
        pygame.mouse.set_visible(True)
        while True:
            self._check_events()
            self._check_alien_numbers()
            if self.stats.game_active:
                self.ship.update()           
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            if self.done:
                self.sb._final_score_update()
                #wait enough for player see score
                pygame.time.wait(2000)
                return self.stats.score

    def _check_alien_numbers(self):
        """If not aliens then finished"""
        if len(self.aliens) == 0:
            self.done = True

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                #sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            #Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #Move the ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.done = True
        elif event.key == pygame.K_ESCAPE:
            self.done = True
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

        if self.stats.game_active:
            #don't make bullets if game hasn't started
            if event.key == pygame.K_SPACE:
                self._fire_bullet()
                self._decrement_score()

    def _decrement_score(self):
        if self.stats.score > 0:
            self.stats.score += self.settings.bullet_points
        self.sb._prep_score()
        self.sb._display_score()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game(self):
        """Start a new game"""
        #Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sound_and_music.make_sound('bell')

        #Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        #Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisons()

    def _check_bullet_alien_collisons(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                points = self.settings.alien_points
                ships_left = self.stats.ships_left 
                factor = (1 + ships_left / (1 + self.settings.ship_limit))
                self.stats.score += int(points * len(aliens) * factor)
            self.sb._prep_score()
            self.sb._display_score()
            self.sound_and_music.make_sound('click')
            
        if not self.aliens:
            #destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
         then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        #Look for alien-ship collisions.
        self._check_ship_alien_collisons()
        #Look for aliens hitting bottom of screen.
        self._check_aliens_bottom()

    def _check_ship_alien_collisons(self):
        """Respond to ship-alien collisions."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.sound_and_music.make_sound('harp')
            self._ship_hit()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the score information.
        self.sb._show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        #Make the most recently drawn screen visible.
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.sound_and_music.make_sound('bullet')
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        self.stats.score = 0
        #Make an aliem.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens    
        for row_number in range(number_rows):  
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self.sound_and_music.make_sound('harp')
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left.
            self.stats.ships_left -= 1
            #Get rid of any remaing aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            #Update scoreboard
            self.stats.score += self.settings.new_round_points
            self.sb._prep_score()
            self.sb._show_score()
            #Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.done = True
            pygame.mouse.set_visible(True)