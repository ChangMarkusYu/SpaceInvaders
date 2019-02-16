import pygame
from pygame.sprite import Sprite
from script.spritesheet_functions import color_image


class Saucer(Sprite):
    def __init__(self, screen, ai_settings):
        self.screen = screen

        self.image = ai_settings.main_sprite_sheet.get_image(
            ai_settings.alien_sprite_data[0])
        self.image_death = ai_settings.main_sprite_sheet.get_image(
            ai_settings.alien_sprite_data[7])
        color_image(ai_settings.saucer_color, self.image, self.image_death)
        self.image_alive = self.image

        self.death_sound = pygame.mixer.Sound(ai_settings.saucer_death_sfx)
        self.death_sound.set_volume(ai_settings.volume)
        self.appear_sound = pygame.mixer.Sound(ai_settings.saucer_appear_sfx)
        self.appear_sound.set_volume(ai_settings.volume)

        self.rect = self.image.get_rect()
        self.rect.top = 36
        self.rect.right = 0
        self.x = float(self.rect.x)

        self.death_cycle = 0
        self.activated = False
        self.hit = False

    def update(self, ai_settings, bullets):
        if self.death_cycle >= 2:
            self.reset()
            return

        if self.activated and not self.hit:
            if pygame.sprite.spritecollideany(self, bullets):
                ai_settings.score += ai_settings.saucer_score
                self.image = self.image_death
                self.death_sound.play()
                self.hit = True
                self.activated = False
                return
            if self.rect.x >= ai_settings.screen_width:
                self.reset()
                return

            self.x += ai_settings.saucer_speed
            self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def reset(self):
        self.image = self.image_alive
        self.rect.right = 0
        self.x = float(self.rect.x)
        self.death_cycle = 0
        self.activated = False
        self.hit = False

    def activate(self):
        self.appear_sound.play()
        self.activated = True
