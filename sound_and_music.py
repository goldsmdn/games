import pygame

class SoundAndMusic:
    def __init__(self):
        """Initialise sound directory"""
        self.sound_dictionary = {'bell': 'sounds/bell.wav',
                            'bullet':    'sounds/gun.wav',
                            'click':     'sounds/click.wav',
                            'harp' :     'sounds/harp.wav',
                            'rocket':    'sounds/rocket.wav',
                            'landed':    'sounds/landed.wav',
                            'explosion': 'sounds/explosion.wav',
                            'squawk':    'sounds/squawk.wav',
                            'thruster':  'sounds/thruster.wav'
                            }

    def make_sound(self, sound_type):
        """make a sound of type sound_type"""
        self.file_name = self.sound_dictionary[sound_type]
        self.sound = pygame.mixer.Sound(self.file_name)
        pygame.mixer.Sound.play(self.sound)