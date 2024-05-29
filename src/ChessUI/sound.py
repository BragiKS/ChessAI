import os
import pygame


class Sound:
    @staticmethod
    def play_capture():
        pygame.mixer.music.load(os.path.join('../assets/sounds/capture.mp3'))
        pygame.mixer.music.play()

    @staticmethod
    def play_move():
        pygame.mixer.music.load(os.path.join('../assets/sounds/move.mp3'))
        pygame.mixer.music.play()

    @staticmethod
    def play_castle():
        pygame.mixer.music.load(os.path.join('../assets/sounds/castle.mp3'))
        pygame.mixer.music.play()

    @staticmethod
    def play_promote():
        pygame.mixer.music.load(os.path.join('../assets/sounds/promote.mp3'))
        pygame.mixer.music.play()

    @staticmethod
    def play_check():
        pygame.mixer.music.load(os.path.join('../assets/sounds/check.mp3'))
        pygame.mixer.music.play()

    @staticmethod
    def play_illegal():
        pygame.mixer.music.load(os.path.join('../assets/sounds/illegal.mp3'))
        pygame.mixer.music.play()
