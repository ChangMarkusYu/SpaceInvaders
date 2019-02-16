import pygame

class Music():
    def __init__(self, ai_settings):
        self.sound_array = []
        for sound in ai_settings.song_queue:
            sfx = pygame.mixer.Sound(sound)
            sfx.set_volume(0.2)
            self.sound_array.append(sfx)

        self.length = len(self.sound_array)
        self.cur = 0

    def play_music(self):
        if self.cur > 3:
            self.cur = 0
        self.sound_array[self.cur].play()
        self.cur += 1
