from lunar_lander import LunarLander
from alien_invasion import AlienInvasion
from handle_text import HandleText
from memory import Memory
from file import File


class Game:
    """Wrapper class to run the games and track scores"""
    def __init__(self):
        """Initialise the game, and create game resources"""
        self.file = File()
        self.score = 0
        self.history = self.file._load_user_info()
        self.response = ''
        self.quit = False

    def _run_games(self):
        """main loop"""
        while self.quit == False:
            self.user_name = self._get_user_name().lower()
            if self.user_name != '':
                self.user_game_history = self.history.get(self.user_name)
                self.response = self._get_game_choice().lower()
                if self.response in ['a', '3']:
                    ai = AlienInvasion()
                    self.score = ai._run_loop()
                    self._update_users('Alien Invasion')
                if self.response in ['l', '3']:
                    ll = LunarLander()
                    self.score = ll._run_loop()
                    self._update_users('Lunar Lander')
                if self.response in ['m', '3']:
                    mem = Memory()
                    self.score = mem._run_loop()
                    self._update_users('Memory game')
                if self.response == 'q':
                    self.quit = True
                if self.response == '':
                    self.quit = True
                self._print_scores()
            if self.user_name == '':
                self._check_quit()

    def _get_user_name(self):
        """prompt for user name"""
        self.prompt = []
        self.prompt.append("Welcome to the Games!")
        self.prompt.append("Please enter player's name: ")
        user_name = self._handle_text()
        return user_name

    def _update_users(self, game):
        """update users scores for a game"""
        if self.user_game_history == None:
            self.user_game_history = {}
            #simplifies handling null histories 
        if self.history == None:
            self.history = {}
        high_score = self.user_game_history.get(game)
        if high_score == None:
            self.user_game_history[game] = self.score
        else:
            if self.score > high_score:
                self.user_game_history[game] = self.score
        self.history[self.user_name] = self.user_game_history
        self.file._dump_user_info(self.history)

    def _get_game_choice(self):
        """prompt for games to play"""
        self.prompt = []
        if self.user_game_history == None:
            welcome = str("Welcome to the Games " + self.user_name.title())
        else:
            welcome = str("Welcome back " + self.user_name.title())
        self.prompt.append(welcome)
        self.prompt.append("Please enter which game you wish to play")
        self.prompt.append("   - enter 'a' for Alien Invasion")
        self.prompt.append("   - enter 'l' for Lunar Lander")
        self.prompt.append("   - enter 'm' for Memory Game")
        self.prompt.append("   - enter '3' for all")
        self.prompt.append("   - enter 'q' to quit")
        valid = False
        while valid == False:
            return_letter = self._handle_text().lower()
            if return_letter in ['a', 'l', 'm',  '3', 'q', '']:
                valid = True
                return return_letter

    def _print_scores(self):
        """prints the scoreboard"""
        self.prompt = []
        self.prompt.append("The current top scores are: ")
        for user, user_history in self.history.items():
            total_score = 0
            text = f"Player  {user.title()}"
            self.prompt.append(text)
            for game, score in user_history.items():
                text = f"   {game} : {score}"
                self.prompt.append(text)
                total_score += score
            text = f"   Total score for {user.title()} : {total_score}"
            self.prompt.append(text)
        self.prompt.append('')
        self.prompt.append('')
        self.prompt.append(" Press Return to continue")
        self.prompt.append('')
        self.prompt.append(" Press q and Return to quit")
        txt = HandleText(self.prompt)
        response = txt._run_loop()
        if response == 'q':
            self.quit = True

    def _handle_text(self):
        """prints a prompt and handles text input"""
        txt = HandleText(self.prompt)
        response = txt._run_loop()
        return response

    def _check_quit(self):
        """quicks that users really want to quit"""
        self.quit = False
        self.prompt = []
        self.prompt.append("Please confirm you would like to quit the game")
        self.prompt.append("")
        self.prompt.append("")
        self.prompt.append("Press q to quit, any other key to continue")
        txt = HandleText(self.prompt)
        response = txt._run_loop()
        if response == 'q':
            self.quit = True

if __name__ == '__main__':
#   make a game instance and run the game.
    game = Game()
    game._run_games()