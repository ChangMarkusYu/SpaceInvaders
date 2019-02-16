import sys
import pygame
from script.spritesheet_functions import concatenate_surface_x, concatenate_surface_y

class Menu():
    def __init__(self, screen, ai_settings, hud):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.screen.fill(ai_settings.bg_color)
        # caption and prompt
        self.caption_text_image = ai_settings.main_sprite_sheet.generate_text(
                                  "space invaders", ai_settings)
        self.prompt_text_image = ai_settings.main_sprite_sheet.generate_text(
                                  "press start", ai_settings)

        self.caption_offset_x = (self.screen_rect.width -
                                 self.caption_text_image.get_width())/2
        self.caption_offset_y = ai_settings.text_height * 9

        self.prompt_offset_x = (self.screen_rect.width -
                                self.prompt_text_image.get_width())/2
        self.prompt_offset_y = self.caption_offset_y + \
                               self.caption_text_image.get_height() + \
                               ai_settings.text_height * 5

        # game over scene
        self.text_message_1 = ai_settings.main_sprite_sheet.generate_text(
                                  "game   over", ai_settings)
        self.message_1_offset_x = (self.screen_rect.width -
                                 self.text_message_1.get_width())/2
        self.message_1_offset_y = ai_settings.text_height * 14


        self.text_message_2 = ai_settings.main_sprite_sheet.generate_text(
                                  "press r to restart", ai_settings)
        self.message_2_offset_x = (self.screen_rect.width -
                                 self.text_message_2.get_width())/2
        self.message_2_offset_y = self.message_1_offset_y + \
                                  ai_settings.text_height * 5

        # score advance table
        self.table = self.__generate_table(ai_settings)
        self.table_copy = self.table

        self.table_offset_x = (self.screen_rect.width -
                               self.table.get_width())/2
        self.table_offset_y = self.prompt_offset_y + \
                              self.prompt_text_image.get_height() + \
                              ai_settings.text_height * 6

        self.cover = pygame.Surface((self.table.get_width(),
                                    self.table.get_height()))
        self.cover.fill(ai_settings.bg_color)

        # hide player lives - draw other parts of the hud
        ai_settings.ship_lives = 0

        self.__intro(ai_settings, hud)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return True
            elif event.type == pygame.QUIT:
                sys.exit()
        return False

    def display_end_game_scene(self, ai_settings, hud):
        self.screen.fill(ai_settings.bg_color)
        ai_settings.ship_lives = 0

        hud.reset(ai_settings)
        hud.blitme(ai_settings)
        self.screen.blit(self.text_message_1,
                        (self.message_1_offset_x, self.message_1_offset_y))
        self.screen.blit(self.text_message_2,
                        (self.message_2_offset_x, self.message_2_offset_y))
        pygame.display.flip()

    def replay_prompt(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True
            elif event.type == pygame.QUIT:
                sys.exit()
        return False


    # introduction animation
    def __intro(self, ai_settings, hud):
        offset = 0
        for i in range(5):
            self.screen.fill(ai_settings.bg_color)

            self.screen.blit(self.table,
                            (self.table_offset_x, self.table_offset_y))
            self.screen.blit(self.cover,
                            (self.table_offset_x, self.table_offset_y + offset))
            self.__draw_title(hud, ai_settings)

            offset += (ai_settings.alien_sprite_data[0][1] + 7)
            pygame.display.flip()
            pygame.time.wait(500)

    def __draw_title(self, hud, ai_settings):
        hud.blitme(ai_settings)
        self.screen.blit(self.caption_text_image,
                         (self.caption_offset_x, self.caption_offset_y))
        self.screen.blit(self.prompt_text_image,
                         (self.prompt_offset_x, self.prompt_offset_y))

    def __generate_table(self, ai_settings):
        row_list = []
        for i in range(4):
            if i == 0:
                string = " =?? points"
            else:
                string = " =" + str(ai_settings.alien_base_score * i) + " points"
            alien_image = ai_settings.main_sprite_sheet.get_image(
                          ai_settings.alien_sprite_data[i])
            aligned_surface = pygame.Surface((ai_settings.alien_sprite_data[0][0],
                               alien_image.get_height()))
            aligned_surface.blit(alien_image, (0,0))
            row_image = concatenate_surface_x(
                         [aligned_surface,
                         ai_settings.main_sprite_sheet.generate_text(
                         string, ai_settings)])
            row_list.append(row_image)
        return concatenate_surface_y(row_list, 7)
