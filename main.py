import pygame as pg

from entity import Player, Enemy
from projectile import Projectile
from groups import all_sprite, active_enemies, active_bullets, active_sprite, session_sprite
from settings import LEVELS, DIMS, DISPLAY_WIDTH, DISPLAY_HEIGHT
from session import get_session


def main():

    session = get_session()
    screen = session.get_screen()

    time_interval = 4000
    next_step_time = 2000

    player = Player()
    player.set_collition(25)

    all_sprite.add(player)
    active_sprite.add(player)

    while session.get_session():
        session.before_hook()
        current_time = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                session.set_session(False)
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_ESCAPE, pg.K_q]:
                    session.set_session(False)
                if event.key == pg.K_RIGHT:
                    player.moving_right = True
                if event.key == pg.K_LEFT:
                    player.moving_left = True
                if event.key == pg.K_SPACE:
                    player.is_jump = True
                if event.key == pg.K_s:
                    pos = player.get_position()
                    position = (pos.x + pos.width + 5, pos.y + pos.height/2)
                    bullet = Projectile(position)
                    bullet.moving_right = True
                    all_sprite.add(bullet)
                    active_bullets.add(bullet)

                if event.key == pg.K_RETURN:
                    if session.game_state in [0, 2]:
                        session.set_level(1)
                        session.update()
                    if session.game_state == 3:
                        player = Player()
                        player.set_collition(25)

                        all_sprite.add(player)
                        active_sprite.add(player)

                        session.set_level(1)
                        session.update()

            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    player.moving_right = False
                if event.key == pg.K_LEFT:
                    player.moving_left = False

        """ Game state logic
        0 = Intro
        1 = Running
        2 = Won
        3 = Game Over
        """
        if session.game_state == 0:
            session.game_intro()
        elif session.game_state == 1:
            if not len(active_sprite):
                session.game_state = 3
            if session.enemy_count:
                session.deploy_enemy()
            if session.level == 3 and not len(active_enemies):
                session.game_state = 2

        elif session.game_state == 2:
            session.game_won()
        elif session.game_state == 3:
            session.game_over()

        for active_entity in pg.sprite.Group.sprites(all_sprite):
            if isinstance(active_entity, Projectile):
                # bullet that moving toward player
                if active_entity.rect.x > DISPLAY_WIDTH or active_entity.rect.x < 0:
                    active_entity.kill()
                elif active_entity.moving_left:
                    contact = pg.sprite.spritecollideany(
                        active_entity, active_sprite)
                    if contact:
                        active_entity.kill()
                        contact.set_hit()
                        if contact.get_health() <= 0:
                            contact.kill()
                else:
                    contact = pg.sprite.spritecollideany(
                        active_entity, active_enemies)
                    if contact:
                        # remove bullet
                        active_entity.kill()
                        contact.set_hit()
                        if contact.get_health() <= 0:
                            contact.kill()

            if isinstance(active_entity, Enemy):
                contact = pg.sprite.spritecollideany(
                    active_entity, active_sprite)
                if isinstance(contact, Player):
                    contact.kill()
                if session.game_state == 3:
                    active_entity.kill()

        all_sprite.update()
        all_sprite.draw(screen)

        # session_sprite.update()
        session.after_hook()


if __name__ == "__main__":
    main()
