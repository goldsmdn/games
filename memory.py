import pygame
from random import randint

from settings import Settings
from card import Card
from sound_and_music import SoundAndMusic
from scoreboard import Scoreboard
from game_stats import GameStats


class Memory:
    """class for memory game"""
    def __init__(self):
        """initialisation"""
        pygame.init
        self.settings = Settings()
        if self.settings.full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Memory game")  
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sm = SoundAndMusic()
        self._read_settings()
        self._init_variables()
        max_images = self.settings.memory_max_images
        if self.squares / 2 > max_images:
            raise Exception(f"There are only {max_images} images supported")
        self._shuffle_cards()
        self._set_up_images()   
        
    def _run_loop(self):
        """Start the main loop for the game"""
        # mouse may be hidden by alien game.
        pygame.mouse.set_visible(True)
        while True:
            self._check_events()
            self._update_first_card()
            self._update_second_card()
            self._update_screen()
            self._check_cards_match()
            self._process_match()
            if self.done:
                self.sb._final_score_update()
                pygame.time.wait(2000)
                return self.stats.score

    def _init_variables(self):
        """called from initialisation"""
        self.done = False
        self.stats.score = 0
        self.card_index = 0
        self.first_card_clicked = False
        self.second_card_clicked = False
        self.card_index_first = -1
        self.card_index_second = -1
        self.possible_match = False
        self.match = False
        #set up an empty frame, and empty cards, backs and blanks
        self.cards, self.backs, self.blanks, self.frame =  [], [], [], []

    def _read_settings(self):
        """called from initialisation"""
        self.rows = self.settings.memory_rows
        self.columns = self.settings.memory_columns
        self.squares = self.rows * self.columns
        self.count_down = self.squares
        if self.squares % 2 == 1:
            raise Exception('must have an odd number of squares')
        self.image_width = self.settings.memory_image_width
        self.image_height = self.settings.memory_image_height
        self.offset = self.settings.memory_image_offset
        self.background_color = self.settings.memory_background_color
        self.click_penalty = self.settings.memory_click_penalty
        self.success_bonus = self.settings.memory_success_bonus
        self.wait = self.settings.memory_wait

    def _shuffle_cards(self):
        """Track cards at each place after shuffling"""
        self.card_tracker_old = [int(i/2) for i in range(self.squares)]
        #holds original card positions
        self.card_tracker_new = list(self.card_tracker_old)
        #holds updated card positions after shuffling
        for j in range(self.settings.memory_shuffle):
            k = randint(0, self.squares - 1)
            l = randint(0, self.squares - 1)
            for m in range(self.squares):
                if m == k:
                    self.card_tracker_new[l] = self.card_tracker_old[k]
                elif m == l:
                    self.card_tracker_new[k] = self.card_tracker_old[l]
                else:
                    self.card_tracker_new[m] = self.card_tracker_old[m]
            self.card_tracker_old = list(self.card_tracker_new)

    def _check_events(self):
        """Handle events including quit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.done = True
                elif event.key == pygame.K_ESCAPE:
                    self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_card_clicked(mouse_pos)

    def _check_card_clicked(self, mouse_pos):
        """find out of the card has been clicked for first or second time"""
        card_clicked = False
        count = 0
        for card in self.cards:
            card_clicked = card.rect.collidepoint(mouse_pos)
            if card_clicked:
                if self.first_card_clicked == False:
                    self.card_index_first = count
                    self.first_card_clicked = True
                elif self.second_card_clicked == False:
                    self.card_index_second = count
                    self.second_card_clicked = True
            count += 1
    
    def _set_up_images(self):
        """create all the cards"""
        for row_number in range(self.rows):  
            for column_number in range(self.columns):
                self._create_cards(column_number, (row_number))
            
    def _create_cards(self, column_number, row_number):
        """create card fronts, backs and disappeared cards"""
        card_index = column_number + row_number * self.columns
        image_index = self.card_tracker_new[card_index]
        card = Card(self, image_index)
        back = Card(self, type='back')
        blank = Card(self, type='blank')

        x = self.offset + column_number * (self.offset + self.image_width)
        y = self.offset + row_number * (self.offset + self.image_height)

        card.rect.x, back.rect.x, blank.rect.x = x, x, x
        card.rect.y, back.rect.y, blank.rect.y = y, y, y

        self.cards.append(card)
        self.backs.append(back)
        self.blanks.append(blank)
        self.frame.append(back)
        #start with backs in the frame.  This gets changed as
        # the game progresses.
 
    def _update_screen(self):
        """shows contents of the frame, also the score"""
        self.screen.fill(self.background_color)
        for item in self.frame:
            item.blitme()
        self.sb._show_score()
        pygame.display.flip()

    def _update_first_card(self):
        """actions for first card clicked"""
        if self.first_card_clicked and not self.second_card_clicked:
            #no action if cards have been matched
            if self.card_tracker_new[self.card_index_first] != -1:
            #turn over card
                self.frame[self.card_index_first] = self.cards[self.card_index_first]
            else:
                self.first_card_clicked = False
    
    def _update_second_card(self):
        """actions for second card clicked"""
        if self.first_card_clicked and self.second_card_clicked:
            if self.card_tracker_new[self.card_index_second] != -1:
                #no action if cards have been matched
                if self.card_index_first == self.card_index_second:
                    #reset to a back if click on first card twice
                    self.frame[self.card_index_first] = self.backs[self.card_index_first]
                    self._reset_click_flags()
                    self._decrement_score()
                    self.sb._prep_score()
                    self.sb._display_score()
                else:
                    self.frame[self.card_index_second] = self.cards[self.card_index_second]
            else:
                self.second_card_clicked = False
    
    def _process_match(self):
        """actions for successful or failed match"""
        if self.first_card_clicked and self.second_card_clicked:
            if self.match:
                #success
                self.sm.make_sound('bell')
                pygame.time.wait(self.wait)
                self.frame[self.card_index_first] = self.blanks[self.card_index_first]
                self.frame[self.card_index_second] = self.blanks[self.card_index_second]
                self.card_tracker_new[self.card_index_first] = -1
                self.card_tracker_new[self.card_index_second] = -1
                self.count_down -= 2
                self._increment_score()
                self.match = False
                if self.count_down == 0:
                    #game finished
                    self.done = True
                else:
                    self._reset_click_flags()
            else:
                #failed
                self.sm.make_sound('harp')
                pygame.time.wait(self.wait)
                self.frame[self.card_index_first] = self.backs[self.card_index_first]
                self.frame[self.card_index_second] = self.backs[self.card_index_second]
                self._reset_click_flags()
                self._decrement_score() 

    def _decrement_score(self):
        """removes click penalty from score and display new score"""
        if self.stats.score > 0:
            self.stats.score -= self.click_penalty
        self.sb._prep_score()
        self.sb._display_score()
  
    def _increment_score(self):
        """adds bonus to score and display new score"""
        self.stats.score += self.success_bonus
        self.sb._prep_score()
        self.sb._display_score()

    def _reset_click_flags(self):
        """forget first and second cards were clicked"""
        self.first_card_clicked = False
        self.second_card_clicked = False

    def _check_cards_match(self):
        """see if the cards matched using the tracker list"""
        if self.first_card_clicked and self.second_card_clicked:
            self.match = False
            card1 = self.card_tracker_new[self.card_index_first]
            card2 = self.card_tracker_new[self.card_index_second]
            if card1 == card2:
                self.match = True