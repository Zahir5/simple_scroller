import pygame as pg

from settings import LEVELS, DIMS, DISPLAY_WIDTH, DISPLAY_HEIGHT
from groups import session_sprite, all_sprite, active_enemies, active_sprite


class Session(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        pg.init()
        pg.display.set_caption("Super Game!")

        self.level = 0
        self.clock = pg.time.Clock()
        self.game_running = True
        self.screen = pg.display.set_mode(DIMS)
        self.game_state = 0

        self.background = LEVELS[self.level]["bg"]
        self.enemy_count = 0

    def set_session(self, val: bool) -> None:
        self.game_running = val

    def get_session(self) -> bool:
        return self.game_running

    def set_level(self, level):
        self.level = level
        if level == 1:
            self.game_state = 1
            self.reset_enemy_count()
        if len(LEVELS) > level:
            self.background = LEVELS[self.level]["bg"]

            # reset player health
            player = active_sprite.sprites()[-1]
            player.health = 100
            player.set_collition(5*(5+level))

    def set_clock(self, val: int) -> None:
        self.clock.tick(val)

    def set_background(self, background):
        self.background = background

    def get_screen(self):
        return self.screen

    def before_hook(self):
        pass
        self.screen.blit(self.background, (0, 0))

    def after_hook(self):
        pg.display.flip()
        self.set_clock(60)

    def reset_enemy_count(self):
        self.enemy_count = LEVELS[self.level].get("enemy_count", 0)

    def update(self, *args, **kwargs):
        self.deploy_enemy()
        return super().update(*args, **kwargs)

    def deploy_enemy(self):
        from entity import Enemy
        enemies = active_enemies.sprites()
        if self.enemy_count:
            if len(enemies) > 0 and enemies[-1].rect.x > DISPLAY_WIDTH - 300:
                return

            self.enemy_count -= 1
            enemy = Enemy(LEVELS[self.level].get("enemy_img"))

            active_enemies.add(enemy)
            all_sprite.add(enemy)

    def game_over(self):
        WHITE = 255, 255, 255
        screen = self.get_screen()
        title = pg.font.Font.render(self.get_font(200), "GAME OVER", 0, WHITE)
        subtitle = pg.font.Font.render(self.get_font(
            50), "Press ENTER to restart", 0, WHITE)

        screen.blit(
            title,
            (DISPLAY_WIDTH/2 - title.get_width()/2,
             DISPLAY_HEIGHT/2 - title.get_height()/2)
        )

        screen.blit(
            subtitle,
            (DISPLAY_WIDTH/2 - subtitle.get_width()/2,
             DISPLAY_HEIGHT/1.5 - subtitle.get_height()/2)
        )

    def game_intro(self):
        WHITE = 255, 255, 255
        screen = self.get_screen()
        title = pg.font.Font.render(self.get_font(
            200), "Welcome to Super Game", 0, WHITE)
        subtitle = pg.font.Font.render(self.get_font(
            50), "Press ENTER to start", 0, WHITE)

        screen.blit(
            title,
            (DISPLAY_WIDTH/2 - title.get_width()/2,
             DISPLAY_HEIGHT/2 - title.get_height()/2)
        )

        screen.blit(
            subtitle,
            (DISPLAY_WIDTH/2 - subtitle.get_width()/2,
             DISPLAY_HEIGHT/1.5 - subtitle.get_height()/2)
        )

    def game_won(self):
        WHITE = 255, 255, 255
        screen = self.get_screen()
        title = pg.font.Font.render(self.get_font(
            200), "YEY! It's a WIN!", 0, WHITE)
        subtitle = pg.font.Font.render(self.get_font(
            50), "Press ENTER to restart", 0, WHITE)

        screen.blit(
            title,
            (DISPLAY_WIDTH/2 - title.get_width()/2,
             DISPLAY_HEIGHT/2 - title.get_height()/2)
        )

        screen.blit(
            subtitle,
            (DISPLAY_WIDTH/2 - subtitle.get_width()/2,
             DISPLAY_HEIGHT/1.5 - subtitle.get_height()/2)
        )

    def get_font(self, size):
        return pg.font.Font(size=size)


def get_session():
    if len(session_sprite) <= 0:
        session = Session()
        session_sprite.add(session)
        return session

    for session in session_sprite.sprites():
        if isinstance(session, Session):
            return session
