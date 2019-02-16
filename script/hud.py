import pygame
from script.spritesheet_functions import color_image

class Hud():
    def __init__(self, screen, ai_settings):
        self.screen = screen

        self.fixed_bar = Fixed_bar(screen, ai_settings)
        self.score_board = Score_board(screen, ai_settings)
        self.player_area = Player_area(screen, ai_settings)

    def reset(self, ai_settings):
        self.player_area.reset(ai_settings)

    def blitme(self, ai_settings):
        self.fixed_bar.blitme()
        self.score_board.blitme(ai_settings)
        self.player_area.blitme(ai_settings)

class Fixed_bar():
    def __init__(self, screen, ai_settings):
        self.screen = screen

        self.image = ai_settings.main_sprite_sheet.generate_text \
                    ("score<1> hi-score score<2>", ai_settings)
        self.rect = self.image.get_rect()
        self.rect.x = ai_settings.text_side_margin
        self.rect.y = ai_settings.text_upper_margin

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Score_board():
    def __init__(self, screen, ai_settings):
        self.screen = screen
        self.high_score = ai_settings.high_score
        self.last_score = -1

        self.image = ai_settings.main_sprite_sheet.generate_text \
                    (self.score_to_text(self.high_score), ai_settings)
        self.rect = self.image.get_rect()
        self.rect.x = ai_settings.text_side_margin
        self.rect.y = ai_settings.text_upper_margin + ai_settings.text_height \
                      + ai_settings.line_spacing

    def blitme(self, ai_settings):
        score = ai_settings.score
        if self.last_score != score:
            score_text = self.score_to_text(self.high_score, score)
            self.image = ai_settings.main_sprite_sheet.generate_text \
                        (score_text, ai_settings)
            self.last_score = score

        self.screen.blit(self.image, self.rect)

    def score_to_text(self, high_score, current_score = 0):
        return "  " + str(current_score).rjust(4, '0') \
                    + "     " + str(high_score).rjust(4, '0')

class Player_area():
    def __init__(self, screen,ai_settings):
        self.screen = screen

        self.image = pygame.Surface((ai_settings.screen_width,
                       ai_settings.screen_bottom_border))

        self.text_image = ai_settings.main_sprite_sheet. \
                        generate_text("credit 00", ai_settings)
        self.ship_image = ai_settings.main_sprite_sheet.get_image(
                        ai_settings.ship_sprite_data)
        color_image(ai_settings.theme_color, self.ship_image)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = ai_settings.screen_height - ai_settings.screen_bottom_border \
        + 15

        self.last = -1
        self.offset = ai_settings.screen_width - self.text_image.get_rect().x - \
                      ai_settings.text_padding * 11

    def draw_ships_left(self, ai_settings):
        lives = ai_settings.ship_lives
        self.__draw_credits(ai_settings)

        if lives != self.last and lives > 0:
            width = ai_settings.ship_sprite_data[0] + 3
            offset = ai_settings.text_side_margin
            self.image.fill(ai_settings.bg_color)
            self.image.blit(ai_settings.main_sprite_sheet.
                            generate_text(str(lives), ai_settings), (offset, 2))
            offset += ai_settings.text_padding * 2
            self.__draw_border_line(ai_settings)

            for i in range(lives-1):
                self.image.blit(self.ship_image, (width * i + offset, 1))
            self.last = lives

    def __draw_credits(self, ai_settings):
        self.image.blit(self.text_image, (self.offset, 2))

    def __draw_border_line(self, ai_settings):
        pygame.draw.rect(self.image, ai_settings.theme_color,
                         pygame.Rect(0, 0, ai_settings.screen_width, 0))

    def blitme(self, ai_settings):
        self.draw_ships_left(ai_settings)
        self.screen.blit(self.image, self.rect)

    def reset(self, ai_settings):
        self.image.fill(ai_settings.bg_color)
