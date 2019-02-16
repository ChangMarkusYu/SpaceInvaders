import pygame
from pygame.sprite import Sprite
from script.spritesheet_functions import color_image


class Ship(Sprite):
    def __init__(self, screen, ai_settings):
        self.screen = screen

        # crop the main sprite sheet
        self.image = ai_settings.main_sprite_sheet.get_image(
            ai_settings.ship_sprite_data)
        self.image_alive = self.image
        self.image_death_1 = ai_settings.main_sprite_sheet.get_image(
            ai_settings.ship_destoryed_1)
        self.image_death_2 = ai_settings.main_sprite_sheet.get_image(
            ai_settings.ship_destoryed_2)
        color_image(ai_settings.theme_color, self.image, self.image_alive,
                    self.image_death_1, self.image_death_2)

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # sound effects
        self.shoot_sound = pygame.mixer.Sound(ai_settings.ship_fire_sfx)
        self.shoot_sound.set_volume(ai_settings.volume)
        self.death_sound = pygame.mixer.Sound(ai_settings.ship_death_sfx)
        self.death_sound.set_volume(ai_settings.volume)

        # put the player at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - ai_settings.screen_bottom_border

        self.center = float(self.rect.centerx)

        # movement flags
        self.moving_left = False
        self.moving_right = False

        # flag for death animation and death clock
        self.flag = False
        self.death_clock = pygame.time.Clock()
        self.death_duration = 0.0

        # ammo limit
        self.ammo = ai_settings.ship_ammo

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, ai_settings):
        if ai_settings.ship_hit:
            self.death_animation(ai_settings)
            return
        # limit the ship's movement to the boundary of the screen
        if self.moving_left and self.rect.left > 0:
            self.center -= ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += ai_settings.ship_speed_factor

        # update center x position
        self.rect.centerx = self.center

    def death_animation(self, ai_settings):
        self.death_clock.tick()
        if self.death_duration >= ai_settings.ship_death_animation_duration:
            # player run out of lives
            if ai_settings.ship_lives <= 0:
                ai_settings.game_over = True
                return
            # restore ship and resume game
            ai_settings.ship_hit = False
            self.death_duration = 0.0
            self.restore_ship(ai_settings)
            self.center_ship()
            return
        self.death_duration += self.death_clock.get_time()

        if not self.flag:
            self.image = self.image_death_1
            self.flag = True
        else:
            self.image = self.image_death_2
            self.flag = False

    def is_clear_to_fire(self, ai_settings):
        return self.ammo > 0

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def restore_ship(self, ai_settings):
        self.image = self.image_alive
