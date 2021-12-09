

class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialise the games settings"""
        #Widely used constants for color and size.
        BLACK = (30, 30, 30)
        CREAM = (230, 230, 230)
        DARK_GREY = (51, 51, 53)
        GREEN = (0, 255, 0)
        GREY = (60, 60, 60)
        LIGHT_BLUE = (241, 57, 29)
        PANEL_GREY = (119, 129, 138)
        WHITE = (255, 255, 255)

        SMALL_TEXT = 24
        MEDIUM_TEXT = 36
        LARGE_TEXT = 48

        #Text handling
        self.default_text_color = CREAM
        self.text_background_color = BLACK
        self.default_font_size = SMALL_TEXT
        self.text_start_offset_down = 10
        self.text_incremental_offset_down = self.default_font_size
        self.text_start_offset_right = self.default_font_size
        self.text_width = self.default_font_size * 5
        self.text_height = self.default_font_size + 2
        self.text_box_color = LIGHT_BLUE
        self.text_spare_width = 10
        self.text_max_width = self.default_font_size * 10
        self.text_extra_space = 5

        # Screen seetings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = CREAM
        self.dark_color = DARK_GREY

        #Ship settings
        self.ship_speed = 1.5
        self.full_screen = False
        self.ship_limit = 3
        
        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = GREY
        self.bullets_allowed = 3
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        #Lander settings
        self.lander_initial_vx = 0.03
        self.lander_initial_vy = 0.001
        self.lander_moon_acc = 0.00001
        self.lander_rocket_acc = -0.00003
        self.lander_thruster_acc = 0.00001
        self.lander_final_vx = 0.02
        self.lander_final_vy = 0.02
        self.lander_initial_fuel = 250
        self.lander_fuel_burn = 1000
        self.lander_height_offset = 584

        #Star settings
        self.star_color = WHITE
        self.star_width = 3
        self.star_height = 3
        self.star_number = 100

        #Sound settings
        self.squawk_fraction = 0.0001

        #Button settings
        self.button_width = 200
        self.button_height = 50
        self.button_color = GREEN
        self.button_text_color = WHITE
        self.button_text_size = LARGE_TEXT

        #score board settings
        self.scoreboard_text_color = BLACK
        self.scoreboard_font_size = LARGE_TEXT
        self.scoreboard_offset = 30
        self.alien_points = 50
        self.bullet_points = -5
        self.new_round_points = 0
        self.lander_base_score = 1000
        self.lander_fuel_multiplier = 20
        self.lander_vx_multiplier = 10000
        self.lander_vy_multiplier = 10000

        #instrument setting     
        self.instrument_default_text = BLACK
        self.instrument_font_size = MEDIUM_TEXT
        self.instrument_offset_down = 250
        self.instrument_offset_left = 180
        self.instrument_offset_text = 34
        self.instrument_background_color = PANEL_GREY
        self.instrument_vx_multiplier = 1000
        self.instrument_vy_multiplier = 1000
        self.lander_max_vx = self.lander_final_vx * self.instrument_vx_multiplier
        self.lander_max_vy = self.lander_final_vy * self.instrument_vy_multiplier
        self.lander_min_fuel = 50
        self.lander_max_height = 200

        #memory game settings
        self.memory_rows = 6
        self.memory_columns = 6
        self.memory_max_images = 18
        self.memory_shuffle = 200
        self.memory_image_width = 60
        self.memory_image_height = 60
        self.memory_image_offset = 30
        self.memory_background_color = CREAM
        self.memory_click_penalty = 10
        self.memory_success_bonus = 100
        self.memory_wait = 800


        


        



