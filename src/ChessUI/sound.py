import os
import pygame


class Sound:
    @staticmethod
    def load_capture():
        pygame.mixer.music.load(os.path.join('../assets/sounds/capture.mp3'))

    @staticmethod
    def load_move():
        pygame.mixer.music.load(os.path.join('../assets/sounds/move.mp3'))

    @staticmethod
    def load_castle():
        pygame.mixer.music.load(os.path.join('../assets/sounds/castle.mp3'))

    @staticmethod
    def load_promote():
        pygame.mixer.music.load(os.path.join('../assets/sounds/promote.mp3'))

    @staticmethod
    def load_check():
        pygame.mixer.music.load(os.path.join('../assets/sounds/check.mp3'))

    @staticmethod
    def play():
        pygame.mixer.music.play()
