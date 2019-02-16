import sys
import pygame
from script.bullet import Bullet
from script.alien import Alien
from script.barrier import Barrier

# utility that checks for keyboard events
def check_events(ai_settings, screen, ship, bullets, aliens):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Keydown events
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, aliens)
        # Keyup events
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ai_settings, screen, ship, bullets, aliens):
    # Moving left
    if event.key == pygame.K_d:
        ship.moving_right = True
    # Moving right
    elif event.key == pygame.K_a:
        ship.moving_left = True
    # Shoot
    elif event.key == pygame.K_SPACE and ship.is_clear_to_fire(ai_settings):
        ship.shoot_sound.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    # Pause
    elif event.key == pygame.K_p:
        ai_settings.game_paused = not ai_settings.game_paused

def check_keyup_events(event, ship):
    # Left movement stoppped
    if event.key == pygame.K_d:
        ship.moving_right = False
    # Right movement stopped
    elif event.key == pygame.K_a:
        ship.moving_left = False

# utility for creating alien fleets
def create_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_alien_number_x(ai_settings, alien.rect.width)
    number_aliens_y = get_alien_number_y(ai_settings, alien.rect.height)

    for i in reversed(range(number_aliens_y)):
        for j in range(number_aliens_x):
            if i == 0:
                create_alien(ai_settings, screen, aliens, i, j, 3)
            elif i == 1 or i == 2:
                create_alien(ai_settings, screen, aliens, i, j, 2)
            else:
                create_alien(ai_settings, screen, aliens, i, j)

def get_alien_number_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - ai_settings.side_margin_factor * alien_width
    number_aliens_x = int(available_space_x / (ai_settings.horizontal_spacing + alien_width))
    return number_aliens_x

def get_alien_number_y(ai_settings, alien_height):
    available_space_y = (ai_settings.screen_height -
                         ai_settings.upper_margin_factor * alien_height -
                         ai_settings.bottom_margin_factor * alien_height)
    number_aliens_y = int(available_space_y / (ai_settings.vertical_spacing_factor * alien_height))
    return number_aliens_y

def create_alien(ai_settings, screen, aliens, row_num, col_num, type = 1):
    alien = Alien(ai_settings, screen, type)
    offset = (ai_settings.alien_alignment_width - alien.rect.width)/2
    side_margin = ai_settings.alien_alignment_width * ai_settings.side_margin_factor
    alien.x = side_margin + (ai_settings.horizontal_spacing +
              ai_settings.alien_alignment_width) * col_num + offset
    alien.rect.x = alien.x
    upper_margin = ai_settings.alien_alignment_height * ai_settings.upper_margin_factor
    alien.rect.y = upper_margin + ai_settings.vertical_spacing_factor * \
                   ai_settings.alien_alignment_height * row_num
    aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.is_out_of_bound(ai_settings):
            return True
    return False

def check_bullet_aliens_collisions(ai_settings, screen, ship, aliens, bullets):
    # hit detection
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    for key in collisions.keys():
        for hit_alien in collisions[key]:
            ai_settings.score += ai_settings.alien_base_score * hit_alien.type
            hit_alien.place_corpse(ai_settings)
            ai_settings.kills += 1

    # if all aliens are eliminated
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens)

def check_alien_bullets_ship_collisions(ai_settings, ship, bullets, alien_bullets):
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        play_ship_death_scene(ai_settings, ship, bullets, alien_bullets)

def check_bullets_block_collisions(ai_settings, bullets, blocks):
    collisions = pygame.sprite.groupcollide(bullets, blocks, True, False)

    for key in collisions.keys():
        for hit_block in collisions[key]:
            hit_block.hit(ai_settings)
            if hit_block.hp <= 0:
                blocks.remove(hit_block)

def play_ship_death_scene(ai_settings, ship, bullets, alien_bullets):
    ai_settings.ship_hit = True
    ai_settings.ship_lives -= 1
    alien_bullets.empty()
    bullets.empty()
    ship.death_sound.play()
    # start the "death clock"
    ship.death_clock.tick()

def reset(ai_settings, screen, ship, aliens, bullets):
    bullets.empty()
    aliens.empty()
    ship.restore_ship(ai_settings)
    ship.center_ship()
    create_fleet(ai_settings, screen, aliens)

def disable_aliens(aliens):
    for alien in aliens.sprites():
        alien.disable()

def enable_aliens(aliens):
    for alien in aliens.sprites():
        alien.enable()

# utility for creating the barrier
def create_barriers(ai_settings, screen, barriers):
    barrier = Barrier(ai_settings, screen, (0,0))
    num_barriers = int((ai_settings.screen_width - ai_settings.barrier_side_margin) \
                   /ai_settings.barrier_spacing)

    for i in range(num_barriers):
        pos_x = ai_settings.barrier_side_margin + i * ai_settings.barrier_spacing
        pos_y = ai_settings.barrier_upper_margin
        new_barrier = Barrier(ai_settings, screen, (pos_x, pos_y))
        barriers.add(new_barrier)


# display utility
def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update(ai_settings)
    # delete bullets that are out of the screen
    for bullet in bullets.sprites():
        if bullet.rect.bottom <= ai_settings.screen_upper_border:
            bullets.remove(bullet)
    # hit detection
    check_bullet_aliens_collisions(ai_settings, screen, ship, aliens, bullets)

def update_alien_bullets(ai_settings, screen, ship, bullets, aliens, alien_bullets):
    alien_bullets.update(ai_settings)
    # delete bullets that are out of the screen
    for alien_bullet in alien_bullets.sprites():
        if alien_bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)
    # hit detection
    check_alien_bullets_ship_collisions(ai_settings, ship, bullets, alien_bullets)

def update_aliens(ai_settings, screen, aliens, bullets, ship, alien_bullets, saucer):
    screen_rect = screen.get_rect()

    if saucer.hit:
        saucer.death_cycle += 1

    flag = check_fleet_edges(ai_settings, aliens)
    if flag:
        ai_settings.alien_direction *= -1
    # Move and shoot
    aliens.update(ai_settings, flag, screen, ship, aliens, alien_bullets)

    # speed up game
    if ai_settings.kills >= ai_settings.kills_to_speed_up:
        ai_settings.alien_speed_factor *= ai_settings.speed_up_factor
        ai_settings.kills_to_speed_up *= (2 * ai_settings.speed_up_factor)

    for alien in aliens.sprites():
        if alien.dead:
            alien.death_cycle += 1

        if alien.death_cycle > ai_settings.death_cycle:
            aliens.remove(alien)
        elif pygame.sprite.collide_rect(ship, alien):
            play_ship_death_scene(ai_settings, ship, bullets, alien_bullets)

        elif alien.rect.bottom >= screen_rect.bottom - ai_settings.screen_bottom_border - 8:
            ai_settings.ship_lives = 0
            play_ship_death_scene(ai_settings, ship, bullets, alien_bullets)
            break

def update_saucer(ai_settings, saucer, bullets):
        if ai_settings.kills >= ai_settings.saucer_appear_kills:
            ai_settings.kills = 0
            saucer.activate()

        saucer.update(ai_settings, bullets)

def update_barriers(ai_settings, bullets, alien_bullets, barriers):
        for barrier in barriers:
            blocks = barrier.blocks
            check_bullets_block_collisions(ai_settings, bullets, blocks)
            check_bullets_block_collisions(ai_settings, alien_bullets, blocks)

def update_screen(ai_settings, screen, ship, aliens, bullets, alien_bullets, barriers, hud, saucer):
    # fill the screen with background color
    screen.fill(ai_settings.bg_color)

    # draw the ship
    ship.blitme()
    # draw the bullets
    bullets.draw(screen)
    # draw the aliens
    aliens.draw(screen)
    # draw aliens' bullets
    alien_bullets.draw(screen)
    # draw the barriers
    for barrier in barriers:
        barrier.blitme()
    # draw the hud
    hud.blitme(ai_settings)
    # draw the saucer
    saucer.blitme()
    # update the canvas
    pygame.display.flip()

def update_high_score(ai_settings):
    if ai_settings.score > ai_settings.high_score:
        ai_settings.write_hi_score()
