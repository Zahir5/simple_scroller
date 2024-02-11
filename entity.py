import pygame as pg
import math
import random

from settings import GROUND_POS, DISPLAY_WIDTH, LEVELS, DISPLAY_HEIGHT
from groups import all_sprite, session_sprite, active_enemies, active_sprite
from session import get_session


class Entity(pg.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, raw_image, position, width, height):
        # Call the parent class (Sprite) constructor
        pg.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height
        self.position = position
        self.speed = 5
        self.moving_right = False
        self.moving_left = False
        self.is_jump = False
        self.jump_count = 15
        self.gravity = 0.5
        self.image = raw_image
        self.health = 100
        self.collition_val = 50
        try:
            self.image = pg.transform.scale(
                self.image, (width, height)).convert_alpha()
        except:
            self.image = raw_image
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.ground_y = self.rect.y

    # def appear(self, session):
    #     session.screen.blit(self.image, self.rect)

    def update(self, *args, **kwargs) -> None:
        if self.moving_right:
            self.move_right()
        if self.moving_left:
            self.move_left()
        if self.is_jump:
            self.jump()

    def get_position(self):
        return self.rect

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def move_right(self):
        if self.is_jump:
            self.rect.x += math.ceil(self.speed*1.25)
        self.rect.x += self.speed

    def move_left(self):
        if self.is_jump:
            self.rect.x -= math.ceil(self.speed*1.25)
        self.rect.x -= self.speed

    def jump(self):

        if self.rect.y >= self.ground_y - 1000:
            self.rect.y -= self.jump_count
            self.jump_count -= 0.6
            if self.rect.y >= self.ground_y:
                self.is_jump = False
                self.jump_count = 15

    def set_hit(self):
        self.health -= self.collition_val

    def get_health(self):
        return self.health

    def set_collition(self, val):
        self.collition_val = val


class Player(Entity):
    def __init__(self):
        image = pg.image.load("assets/images/player.png")
        position = (100, GROUND_POS)
        width = 200
        height = 200

        super().__init__(image, position, width, height)

    def update(self, *args, **kwargs) -> None:

        if self.rect.x > DISPLAY_WIDTH:
            session = get_session()
            level = session.level + 1

            if level >= len(LEVELS):
                self.moving_right = False
            else:
                session.set_level(level)
                self.rect.x = 100
                session.reset_enemy_count()
                session.update()

        if self.rect.x < 100:
            self.moving_left = False

        self.render_stats()
        return super().update(*args, **kwargs)

    def render_stats(self):
        session = get_session()
        if session.level > -1:
            screen = session.get_screen()

            font = pg.font.Font(size=50)
            WHITE = 255, 255, 255

            stats = [
                {
                    "text": f"Health: {str(self.get_health())}",
                    "pos": (100, DISPLAY_HEIGHT-100)
                }
            ]

            for stat in stats:
                screen.blit(
                    pg.font.Font.render(font, stat.get("text"), 0, WHITE),
                    stat.get("pos")
                )


class Enemy(Entity):
    def __init__(self, image=None, width=200, height=200):
        if not image:
            image = pg.transform.flip(pg.image.load(
                "assets/images/enemy.png"), flip_x=True, flip_y=False)
        position = (DISPLAY_WIDTH, GROUND_POS)
        super().__init__(image, position, width, height)

        self.moving_left = True
        self.current_time = pg.time.get_ticks()
        self.next_step_time = self.current_time + 2000
        self.time_interval = random.choice([3000, 4000, 5000])

    def update(self, *args, **kwargs):
        # ramdom sooting by enemy
        self.current_time = pg.time.get_ticks()
        if self.current_time > self.next_step_time:
            self.next_step_time += self.time_interval
            self.shoot()

        # enemy move upto center of the screen
        if self.rect.x < DISPLAY_WIDTH/2:
            self.moving_left = False
        self.speed = 2
        session = get_session()
        if session.enemy_count:
            session.deploy_enemy()

        contact = pg.sprite.spritecollideany(self, active_enemies)
        if contact and contact.rect.x < DISPLAY_WIDTH / 2:
            self.moving_left = False

        self.render_stats()
        return super().update(*args, **kwargs)

    def render_stats(self):
        session = get_session()
        if session.level > -1:
            screen = session.get_screen()

            font = pg.font.Font(size=50)
            WHITE = 255, 255, 255

            stats = [
                {
                    "text": f"Health: {str(self.get_health())}",
                    "pos": (self.rect.x, self.rect.y - 10)
                }
            ]

            for stat in stats:
                screen.blit(
                    pg.font.Font.render(font, stat.get("text"), 0, WHITE),
                    stat.get("pos")
                )

    def shoot(self):
        from projectile import Projectile

        position = (self.rect.x - 5,
                    self.rect.y + self.rect.height/2)

        bullet = Projectile(position, dir=0)
        bullet.moving_left = True
        all_sprite.add(bullet)
