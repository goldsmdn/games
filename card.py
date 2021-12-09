import pygame


class Card:
    """defines cards with faces, backs and blanks """
    def __init__(self, mem, index=0, type='card'):
        """initialises the card"""
        self.screen = mem.screen
        if type == 'blank':
            # card has disappeared
            file_name = 'images\mem_blank.bmp'
        elif type == 'back':
            #back of card
            file_name = 'images\mem_back.bmp'
        elif type == 'card':
            #front of card
            file_name = str('images\mem' + str(index) + '.bmp')
        else:
            raise Exception('Incorrect card type')
        self.image = pygame.image.load(file_name)
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw the card at its current_location"""
        #print('blitme')
        self.screen.blit(self.image, self.rect)