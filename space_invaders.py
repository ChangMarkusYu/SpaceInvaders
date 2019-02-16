import sys
import pygame
import script.game_functions as gf
from pygame.sprite import Group
from script.settings import Settings
from script.ship import Ship
from script.hud import Hud
from script.saucer import Saucer
from script.music import Music
from script.menu import Menu


def run_game():
    # initialize the game and create a screen/canvas object
    pygame.init()
    pygame.mouse.set_visible(False)
    FPSCLOCK = pygame.time.Clock()
    ai_settings = Settings()
    # set screen width, height and caption
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("SPACE INVADERS")
    hud = Hud(screen, ai_settings)
    menu = Menu(screen, ai_settings, hud)

    while not menu.update():
        continue

    while True:

        ai_settings = Settings()
        music = Music(ai_settings)
        ship = Ship(screen, ai_settings)
        hud = Hud(screen, ai_settings)
        saucer = Saucer(screen, ai_settings)
        aliens = Group()
        bullets = Group()
        alien_bullets = Group()
        barriers = Group()

        gf.create_fleet(ai_settings, screen, aliens)
        gf.create_barriers(ai_settings, screen, barriers)
        duration = 0.0

        # main loop of the game
        while not ai_settings.game_over:
            if not ai_settings.ship_hit and not ai_settings.game_paused:
                if duration >= ai_settings.alien_speed_factor:
                    gf.update_aliens(ai_settings, screen, aliens,
                                     bullets, ship, alien_bullets, saucer)
                    music.play_music()
                    duration = 0
                duration += FPSCLOCK.get_time()
                gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
                gf.update_alien_bullets(ai_settings, screen, ship, bullets,
                                        aliens, alien_bullets)
                gf.update_barriers(ai_settings, bullets,
                                   alien_bullets, barriers)
                gf.update_saucer(ai_settings, saucer, bullets)

            if not ai_settings.game_paused:
                ship.update(ai_settings)

            gf.check_events(ai_settings, screen, ship, bullets, aliens)
            gf.update_screen(ai_settings, screen, ship, aliens,
                             bullets, alien_bullets, barriers, hud, saucer)
            FPSCLOCK.tick(60)

        gf.update_high_score(ai_settings)
        menu.display_end_game_scene(ai_settings, hud)
        while not menu.replay_prompt():
            continue


run_game()
